import logging
import pickle
import pandas as pd
import numpy as np
import re

from os.path import abspath

from django.conf import settings

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

logger = logging.getLogger(__name__)

class MBTIPrediction(object):
    def __init__(self):
        base_dir = settings.BASE_DIR
        self.download_dir = abspath("{}/mbti_data/".format(base_dir))
        msg = "Downloading nltk modules to: {}".format(self.download_dir)
        logger.debug(msg)
        self._cntizer = None
        self._tfizer = None
        self._IE_model = None
        self._NS_model = None
        self._FT_model = None
        self._JP_model = None

    def load_pickle(self, datafile):
        """Load a pickly file from storage"""
        download_file = "{}/{}".format(self.download_dir, datafile)
        return pickle.load(open(download_file, 'rb'))

    def get_cntizer(self):
        if self._cntizer == None:
            self._cntizer = self.load_pickle("pretrain_cnt.pickle")
        return self._cntizer

    def get_tfizer(self):
        if self._tfizer == None:
            self._tfizer = self.load_pickle("pretrain_tfidf.pickle")
        return self._tfizer

    def get_IE_model(self):
        if self._cntizer == None:
            self._IE_model = self.load_pickle("IE.pickle")
        return self._IE_model

    def get_NS_model(self):
        if self._NS_model == None:
            self._NS_model = self.load_pickle("NS.pickle")
        return self._NS_model

    def get_FT_model(self):
        if self._FT_model == None:
            self._FT_model = self.load_pickle("FT.pickle")
        return self._FT_model

    def get_JP_model(self):
        if self._JP_model == None:
            self._JP_model = self.load_pickle("JP.pickle")
        return self._JP_model

    def translate_personality(self, personality):
        # transform mbti to binary vector
        # Pretrained count vectorizer & tfidf
        b_Pers = {'I': 0, 'E': 1, 'N': 0, 'S': 1, 'F': 0, 'T': 1, 'J': 0, 'P': 1}
        return [b_Pers[l] for l in personality]

    def translate_back(self, personality):
        # transform binary vector to mbti personality
        # binarize MBTI score (and reverse)
        b_Pers_list = [{0: 'I', 1: 'E'}, {0: 'N', 1: 'S'}, {0: 'F', 1: 'T'}, {0: 'J', 1: 'P'}]

        s = ""
        for i, l in enumerate(personality):
            s += b_Pers_list[i][l]
        return s

    # Preprocess input text data
    def pre_process_data(self, data, remove_stop_words=True, remove_mbti_profiles=True):
        list_personality = []
        list_posts = []
        len_data = len(data)
        i = 0

        stemmer = PorterStemmer()
        lemmatiser = WordNetLemmatizer()
        cachedStopWords = stopwords.words("english")

        unique_type_list = ['INFJ', 'ENTP', 'INTP', 'INTJ', 'ENTJ', 'ENFJ', 'INFP', 'ENFP',
                            'ISFP', 'ISTP', 'ISFJ', 'ISTJ', 'ESTP', 'ESFP', 'ESTJ', 'ESFJ']

        unique_type_list = [x.lower() for x in unique_type_list]

        for row in data.iterrows():
            i += 1
            # if (i % 500 == 0 or i == 1 or i == len_data):
            #     print("%s of %s rows" % (i, len_data))

            ##### Remove and clean comments
            posts = row[1].posts
            temp = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', posts)
            temp = re.sub("[^a-zA-Z]", " ", temp)
            temp = re.sub(' +', ' ', temp).lower()
            if remove_stop_words:
                temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ') if w not in cachedStopWords])
            else:
                temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ')])

            if remove_mbti_profiles:
                for t in unique_type_list:
                    temp = temp.replace(t, "")

            type_labelized = self.translate_personality(row[1].type)
            list_personality.append(type_labelized)
            list_posts.append(temp)

        list_posts = np.array(list_posts)
        list_personality = np.array(list_personality)
        return list_posts, list_personality


    def predict_MBTI(self, input):

        IE_model = self.get_IE_model()
        NS_model = self.get_NS_model()
        FT_model = self.get_FT_model()
        JP_model = self.get_JP_model()
        cntizer = self.get_cntizer()
        tfizer = self.get_tfizer()

        mydata = pd.DataFrame(data={'type': ['INFJ'], 'posts': [input]})
        preprocessed_data, _ = self.pre_process_data(mydata, remove_stop_words=True)

        X_cnt = cntizer.transform(preprocessed_data)
        X_tfidf = tfizer.transform(X_cnt).toarray()

        result = []

        result.append(IE_model.predict(X_tfidf)[0])
        result.append(NS_model.predict(X_tfidf)[0])
        result.append(FT_model.predict(X_tfidf)[0])
        result.append(JP_model.predict(X_tfidf)[0])

        result = self.translate_back(result)
        result = [x for x in result]
        return result
