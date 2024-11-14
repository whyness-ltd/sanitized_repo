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

def translate_personality(personality):
    # transform mbti to binary vector
    # Pretrained count vectorizer & tfidf
    b_Pers = {'I': 0, 'E': 1, 'N': 0, 'S': 1, 'F': 0, 'T': 1, 'J': 0, 'P': 1}
    return [b_Pers[l] for l in personality]

def translate_back(personality):
    # transform binary vector to mbti personality
    # binarize MBTI score (and reverse)
    b_Pers_list = [{0: 'I', 1: 'E'}, {0: 'N', 1: 'S'}, {0: 'F', 1: 'T'}, {0: 'J', 1: 'P'}]

    s = ""
    for i, l in enumerate(personality):
        s += b_Pers_list[i][l]
    return s

# Preprocess input text data
def pre_process_data(data, remove_stop_words=True, remove_mbti_profiles=True):
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

        type_labelized = translate_personality(row[1].type)
        list_personality.append(type_labelized)
        list_posts.append(temp)

    list_posts = np.array(list_posts)
    list_personality = np.array(list_personality)
    return list_posts, list_personality


def predict_MBTI(input, IE_model, NS_model, FT_model, JP_model, cntizer, tfizer):

    mydata = pd.DataFrame(data={'type': ['INFJ'], 'posts': [input]})
    preprocessed_data, _ = pre_process_data(mydata, remove_stop_words=True)

    X_cnt = cntizer.transform(preprocessed_data)
    X_tfidf = tfizer.transform(X_cnt).toarray()


    result = []

    result.append(IE_model.predict(X_tfidf)[0])
    result.append(NS_model.predict(X_tfidf)[0])
    result.append(FT_model.predict(X_tfidf)[0])
    result.append(JP_model.predict(X_tfidf)[0])

    result = translate_back(result)
    result = [x for x in result]
    return result


# This will fail before pickles are downloaded
# Ensure pickles are downloaded then use this to update
base_dir = settings.BASE_DIR
download_dir = abspath("{}/mbti_data/".format(base_dir))
msg = "Downloading nltk modules to: {}".format(download_dir)
logger.debug(msg)
download_file = "{}/{}".format(download_dir, "pretrain_cnt.pickle")
cntizer = pickle.load(open(download_file, 'rb'))
download_file = "{}/{}".format(download_dir, "pretrain_tfidf.pickle")
tfizer = pickle.load(open(download_file, 'rb'))

download_file = "{}/{}".format(download_dir, "IE.pickle")
IE_model = pickle.load(open(download_file, 'rb'))
download_file = "{}/{}".format(download_dir, "NS.pickle")
NS_model = pickle.load(open(download_file, 'rb'))
download_file = "{}/{}".format(download_dir, "FT.pickle")
FT_model = pickle.load(open(download_file, 'rb'))
download_file = "{}/{}".format(download_dir, "JP.pickle")
JP_model = pickle.load(open(download_file, 'rb'))

input = "hello"

result = predict_MBTI(
    input,
    IE_model,
    NS_model,
    FT_model,
    JP_model,
    cntizer,
    tfizer
)
