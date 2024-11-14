import string
import json
import nltk
nltk.data.path.append('/app/nltk_data')
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk import word_tokenize

visual_word_list = ['abide_by', 'absolved', 'abstemious', 'acquit', 'adage', 'alight', 'all_the_way', 'anatomy', 'angle', 'appear', 'appearance', 'appearing', 'arc', 'aspect', 'assoil', 'attend', 'attestant', 'attestator', 'attestor', 'audit', 'augury', 'aurora', 'authorise', 'authorize', 'await', 'batch', 'bear_witness', 'bet', 'black', 'bleak', 'bleary', 'bless', 'blind', 'blink', 'blink_of_an_eye', 'blur', 'blurred', 'blurry', 'bod', 'border', 'brassy', 'break', 'break_of_day', 'break_of_the_day', 'bright', 'brighten', 'brightness', 'brightness_level', 'brilliant', 'bring_in', 'bring_out', 'brumous', 'build', 'byword', 'calculate', 'calorie-free', 'cast', 'catch', 'celebrate', 'center', 'centering', 'centre', 'characterisation', 'characterization', 'chassis', 'cheap', 'check', 'clarity', 'clean', 'clean-cut', 'clear', 'clear-cut', 'clear_up', 'cleared', 'clearly', 'clearness', 'click', 'cockcrow', 'come_across', 'come_along', 'come_home', 'come_out', 'coming_into_court', 'compose', 'conceive_of', 'concenter', 'concentrate', 'concentre', 'conniption', 'construe', 'contract', 'coruscate', 'coruscation', 'couch', 'count', 'crystal', 'crystalise', 'crystalize', 'crystallise', 'crystallization', 'crystallize', 'dart', 'dash', 'date', 'dawn', 'dawning', 'daybreak', 'dayspring', 'dazed', 'decipherable', 'delineation', 'demo', 'demonstrate', 'dense', 'depend', 'depict', 'depiction', 'designate', 'detect', 'determine', 'dim', 'dimmed', 'dip', 'direction', 'discharge', 'disclose', 'discover', 'dismount', 'display', 'double', 'draw_up', 'dull', 'earn', 'effervesce', 'effigy', 'electric_arc', 'electric_discharge', 'elucidate', 'encounter', 'enlighten', 'ensnare', 'ensure', 'entrap', 'envisage', 'envision', 'epitome', 'escort', 'establish', 'evidence', 'evince', 'examine', 'exculpate', 'exculpated', 'exemplify', 'exhibit', 'exonerate', 'exonerated', 'expect', 'expectation', 'expose', 'exposure', 'express', 'expression', 'eyeshot', 'face', 'facial_expression', 'faint', 'fall', 'fall_into_place', 'fancy', 'fanfare', 'figure', 'figure_of_speech', 'film', 'find', 'find_out', 'fire_up', 'first_light', 'fish', 'fit', 'fizz', 'flare', 'flash', 'flash_bulb', 'flash_lamp', 'flashbulb', 'flashgun', 'flashing', 'flashy', 'flaunt', 'flesh', 'flick', 'flicker', 'flock', 'foam', 'focal_point', 'focalise', 'focalize', 'focus', 'focusing', 'focussing', 'fogged', 'foggy', 'follow', 'foresee', 'foretoken', 'form', 'form_bubbles', 'frame', 'frame_in', 'frame_of_reference', 'frame_up', 'framing', 'front', 'froth', 'fuzzy', 'gain', 'garish', 'gaudy', 'gestural', 'get_word', 'get_across', 'get_down', 'get_off', 'get_word', 'gimcrack', 'give_away', 'glint', 'glisten', 'glister', 'glitter', 'go_out', 'go_steady', 'go_through', 'good_deal', 'graphic', 'great_deal', 'groggy', 'hatful', 'hazy', 'heap', 'heartbeat', 'honor', 'honour', 'horizon', 'house', 'human_body', 'icon', 'ideate', 'idle', 'ignite', 'igniter', 'ignitor', 'ikon', 'illume', 'illuminate', 'illumination', 'illumine', 'illustrate', 'image', 'imagination', 'imaginativeness', 'imagine', 'impression', 'indicate', 'informant', 'inning', 'inspect', 'instance', 'instant', 'insure', 'intense', 'interpret', 'jiffy', 'keep_an_eye_on', 'ken', 'lean', 'lechatelierite', 'let_on', 'let_out', 'lifelike', 'light', 'light-colored', 'light-headed', 'light_source', 'light_up', 'lighter', 'lightheaded', 'lighting', 'lightly', 'lightness', 'lightsome', 'limpidity', 'linear_perspective', 'lite', 'logy', 'look', 'look-alike', 'look_at', 'look_on', 'look_out', 'looker', 'looking', 'looking_at', 'lookout', 'lookout_man', 'lot', 'loud', 'low-cal', 'lucidity', 'lucidness', 'luminance', 'luminosity', 'luminousness', 'mansion', 'mark', 'mass', 'material_body', 'mental_image', 'mental_picture', 'mentality', 'meretricious', 'mess', 'mickle', 'mind-set', 'mindset', 'mint', 'misty', 'morning', 'motion-picture_show', 'motion_picture', 'mountain', 'movie', 'moving-picture_show', 'moving_picture', 'muckle', 'muzzy', 'net', 'news_bulletin', 'newsbreak', 'newsflash', 'nidus', 'note', 'notice', 'obscure', 'observant', 'observative', 'observe', 'observing', 'obtuse', 'open', 'ostentate', 'ostentation', 'outlook', 'painting', 'panorama', 'paradigm', 'part', 'passel', 'peck', 'pellucidity', 'penetrate', 'perceive', 'perch', 'percipient', 'persona', 'perspective', 'persuasion', 'photo', 'photoflash', 'photograph', 'physical_body', 'physique', 'pic', 'pick_up', 'picket', 'pictorial', 'pictorial_matter', 'picture', 'picture_show', 'pile', 'planetary_house', 'plenty', 'point', 'polarity', 'pore', 'position', 'pot', 'power_saw', 'preindication', 'present', 'project', 'prospect', 'prototype', 'prove', 'proverb', 'pull_in', 'purview', 'put', 'quartz', 'quartz_glass', 'quite_a_little', 'raft', 'range_of_a_function', 'ratify', 'read', 'readable', 'record', 'redact', 'regard', 'register', 'render', 'respect', 'reveal', 'rivet', 'run_across', 'run_into', 'sack_up', 'saw', 'sawing_machine', 'scant', 'scene', 'scenery', 'scintillate', 'scintillation', 'scoot', 'scout', 'scrutinise', 'scrutinize', 'scud', 'search', 'see', 'see_to_it', 'seem', 'seen', 'sentiment', 'sentinel', 'sentry', 'set_off', 'set_up', 'setting', 'shadowy', 'shape', 'sharpen', 'shed_light_on', 'shew', 'shoot', 'short', 'shot', 'show', 'show_off', 'show_up', 'shown', 'sight', 'sign', 'sign-language', 'sign_of_the_zodiac', 'sign_on', 'sign_up', 'signal', 'signaling', 'signalise', 'signalize', 'signboard', 'signed', 'simulacrum', 'sink_in', 'skeletal_frame', 'skeletal_system', 'skeleton', 'slant', 'slew', 'slow', 'slur', 'sluttish', 'snap', 'snapshot', 'solve', 'soma', 'sort_out', 'spark', 'sparkle', 'sparkling', 'spate', 'spectator', 'spirit', 'split_second', 'spotter', 'spy', 'stack', 'star_sign', 'straighten_out', 'stress', 'stuporous', 'subscribe', 'sunrise', 'sunup', 'survey', 'swank', 'swooning', 'systema_skeletale', 'tacky', 'take_care', 'take_in', 'take_note', 'tantrum', 'tatty', 'tawdry', 'testify', 'thought', 'ticker', 'tidy_sum', 'tilt', 'tip', 'top', 'trashy', 'trice', 'trope', 'twinkle', 'twinkling', 'unaccented', 'unclouded', 'uncloudedness', 'unclutter', 'uncover', 'undefined', 'underframe', 'unhorse', 'unmortgaged', 'unveil', 'unwrap', 'usher', 'vague', 'video', 'view', 'viewer', 'vigil', 'vindicated', 'visible_light', 'visible_radiation', 'vision', 'visit', 'vista', 'visual_aspect', 'visual_modality', 'visual_sensation', 'visual_sense', 'visualise', 'visualize', 'vitreous_silica', 'vivid', 'wad', 'wakeful', 'watch', 'watch_crystal', 'watch_glass', 'watch_out', 'watch_over', 'watcher', 'weak', 'weight', 'well-defined', 'wink', 'winkle', 'wispy', 'witness', 'witnesser', 'word-painting', 'word_picture']

auditory_word_list = ['accord', 'address', 'agree', 'anchor_ring', 'announce', 'annulus', 'annunciate', 'articulation', 'assure', 'at_variance', 'attune', 'audible', 'audience', 'audio', 'auditory_sensation', 'auricle', 'babble', 'babble_out', 'babbling', 'band', 'bang', 'bell', 'bell_shape', 'blab', 'blab_out', 'blather', 'blether', 'blither', 'blunt', 'body_politic', 'break', 'bruit', 'bubble', 'burble', 'busyness', 'buzz', 'buzzer', 'call', 'call_up', 'campana', 'candid', 'capitulum', 'chime', 'chord', 'closed_chain', 'comment', 'commonwealth', 'concord', 'consort', 'consultation', 'country', 'creak', 'deaf', 'deaf_as_a_post', 'deafen', 'declare', 'denote', 'differentiate', 'direct', 'disagreement', 'disclose', 'discordant', 'discrepant', 'disharmonious', 'dissension', 'dissonance', 'dissonant', 'distinguish', 'divulge', 'doorbell', 'doughnut', 'dulcet', 'dumb', 'ear', 'echo', 'effectual', 'engineer', 'enjoin', 'environ', 'euphony', 'express', 'fathom', 'find_out', 'fit_in', 'foretell', 'forthright', 'frank', 'free-spoken', 'gang', 'get_a_line', 'get_wind', 'get_word', 'give_away', 'gong', 'good', 'grizzle', 'guggle', 'gurgle', 'halo', 'harbinger', 'harmonise', 'harmonize', 'healthy', 'hear', 'hearable', 'heard', 'hearsay', 'heed', 'herald', 'honeyed', 'hoop', 'hum', 'humming', 'hush', 'hush_up', 'indifferent', 'inharmonic', 'input', 'intelligent', 'interpreter', 'interview', 'knell', 'lallation', 'land', 'lecture', 'legal', 'let_on', 'let_out', 'let_the_cat_out_of_the_bag', 'level-headed', 'levelheaded', 'listen', 'mastermind', 'medicine', 'mellifluous', 'mellisonant', 'mention', 'mind', 'mob', 'mouth', 'music', 'muteness', 'narrate', 'nation', 'noise', 'note', 'oral', 'oral_exam', 'oral_examination', 'orchestrate', 'order', 'organise', 'organize', 'outspoken', 'overtone', 'overtones', 'pack', 'partial', 'partial_tone', 'peach', 'peal', 'phonation', 'phone', 'pick_up', 'pinna', 'plainspoken', 'point-blank', 'point_out', 'posit', 'profoundly_deaf', 'province', 'public_lecture', 'put_forward', 'question', 'quiet', 'quieten', 'racket', 'reasoned', 'recall', 'recite', 'reconcile', 'recount', 'remark', 'repeat', 'replication', 'representative', 'res_publica', 'resonate', 'resound', 'reverberate', 'reverberation', 'ring', 'ringing', 'ripple', 'rumor', 'rumour', 'rustle', 'rustling', 'say', 'screak', 'screech', 'secern', 'secernate', 'secrecy', 'secretiveness', 'seethe', 'separate', 'severalise', 'severalize', "ship's_bell", 'shut_up', 'silence', 'sing', 'skirt', 'skreak', 'smatter', 'snap', 'snivel', 'sound', 'sound_reflection', 'speak', 'speech_sound', 'speechless', 'spike', 'spill', 'spill_the_beans', 'spokesperson', 'squeak', 'state', 'state_of_matter', 'stone-deaf', 'straight-from-the-shoulder', 'strait', 'submit', 'surround', 'susurration', 'sweet', 'take_heed', 'talk', 'talk_of_the_town', 'talking', 'tattle', 'telephone', 'tell', 'tell_apart', 'thrum', 'tintinnabulation', 'toll', 'tone', 'try', 'tune in', 'tune out', 'unhearing', 'unresolved', 'unwritten', 'utter', 'verbalise', 'verbalize', 'vibrate', 'viva', 'viva_voce', 'vocal', 'vocalisation', 'vocalise', 'vocalism', 'vocalization', 'vocalize', 'voice', 'voicelessness', 'vox', 'well-grounded', 'whimper', 'whine', 'whisper', 'whispering', 'yammer', 'yawp']

kinesthetic_word_list = ['abide', 'abrasion', 'accommodate', 'accusation', 'accuse', 'ache', 'addle', 'addled', 'address', 'adjoin', 'adjudge', 'admit', 'advert', 'advertise', 'advertize', 'affect', 'afflictive', 'agitate', 'allude', 'aplomb', 'apply', 'appoint', 'appreciation', 'apprehend', 'apprehension', 'arduous', 'armorial_bearing', 'arrest', 'assuredness', 'at_large', 'backbreaking', 'balmy', 'bang', 'bear', 'bear_down', 'bear_on', 'bear_upon', 'bearable', 'bearing', 'becharm', 'bedevil', 'befuddle', 'befuddled', 'beg', 'beguile', 'belief', 'bemuse', 'bewilder', 'bewitch', 'big', 'bill', 'billing', 'bind', 'blame', 'bland', 'book', 'boot', 'break', 'brook', 'buck', 'budge', 'bug', 'bumble', 'burden', 'burster', 'bursting_charge', 'button', 'callous', 'calloused', 'cam_stroke', 'campaign', 'captivate', 'capture', 'care', 'careen', 'cargo_area', 'cargo_deck', 'cargo_hold', 'carry', 'cast', 'cast_off', 'catamenia', 'catch', 'catch_up_with', 'cathexis', 'cauterise', 'cauterize', 'chafe', 'change', 'change_over', 'charge', 'charge_up', 'charm', 'check', 'chemise', 'chill', 'clasp', 'clayey', 'clench', 'cloggy', 'clutch', 'clutches', 'collar', 'come_to', 'come_up', 'commission', 'commit', 'commove', 'compass', 'complaint', 'concentrated', 'concern', 'concrete', 'concur', 'confine', 'confound', 'confuse', 'consign', 'contact', 'contact_lens', 'contain', 'contrive', 'control', 'cool', 'cool_down', 'cool_off', 'coolheaded', 'course', 'cover', 'crowd', 'crusade', 'curb', 'current', 'cushy', 'custody', 'cutaneous_senses', 'dab', 'deal', 'decompress', 'deem', 'defend', 'defy', 'delay', 'delicate', 'dense', 'depression', 'detainment', 'detention', 'difficult', 'diffuse', 'diffused', 'dig', 'digest', 'direction', 'discombobulate', 'dislodge', 'displacement', 'disturb', 'do_by', 'drive', 'drop', 'duty_period', 'easygoing', 'effect', 'electric_charge', 'enamor', 'enamour', 'enceinte', 'enchant', 'endurable', 'endure', 'energy', 'enervate', 'entertain', 'entrance', 'equal', 'escaped', 'excite', 'excoriation', 'expectant', 'experience', 'exploit', 'explosive_charge', 'extend_to', 'fall', 'falter', 'fascinate', 'fault', 'faulting', 'faze', 'feed', 'feel', 'feeling', 'fight', 'file', 'find', 'finger', 'firm', 'firmly', 'flabby', 'flaccid', 'flavor', 'flavour', 'fleshy', 'flip', 'flow', 'flow_rate', 'flowing', 'fluent', 'fluid', 'flush', 'flux', 'force', 'fox', 'fracture', 'fray', 'free', 'fret', 'frightened', 'fuddle', 'gentle', 'gently', 'genuflect', 'geological_fault', 'get-up-and-go', 'get_hold_of', 'get_the_picture', 'get_through', 'ghost', 'gimmick', 'give', 'go_for', 'grab', 'grasp', 'grate', 'grave', 'gravid', 'great', 'grievous', 'grip', 'grok', 'grueling', 'gruelling', 'guard', 'guardianship', 'half-hearted', 'halfhearted', 'halt', 'handgrip', 'handle', 'hang', 'hang-up', 'harbor', 'harbour', 'hard', 'hardhearted', 'haul', 'have-to_doe_with', 'have_got', 'hearty', 'heavily', 'heavy', 'heraldic_bearing', 'hint', 'hit', 'hitch', 'hold', 'hold_back', 'hold_in', 'hold_on', 'hold_up', 'huffy', 'hurl', 'hurt', 'hydrant', 'idle', 'impact', 'impenetrable', 'impinging', 'impression', 'imprint', 'indulgent', 'indurate', 'informal', 'institutionalise', 'institutionalize', 'intemperate', 'intemperately', 'inter-group_communication', 'intercept', 'intuitive_feeling', 'itch', 'jot', 'keep', 'keep_back', 'kick', 'knock', 'knockout', 'kowtow', 'labor', 'labored', 'laborious', 'labour', 'laboured', 'large', 'lax', 'leaden', 'legato', 'lenient', 'let_loose', 'level', 'liaison', 'liberal', 'liberate', 'light', 'lightly', 'link', 'liquid', 'load', 'lodge', 'loose', 'loosen', 'loosen_up', 'lose', 'lowering', 'lukewarm', 'lumbering', 'lurch', 'mad', 'maintain', 'make', 'make_relaxed', 'mark', 'match', 'meet', 'menses', 'menstruate', 'menstruation', 'menstruum', 'mental_picture', 'middleman', 'mild', 'mission', 'misstep', 'mite', 'moderate', 'muddle', 'muddled', 'muzzy', 'nerveless', 'notion', 'nurse', 'obligate', 'oblige', 'obtain', 'on_the_loose', 'open', 'operose', 'overhear', 'overtake', 'overweight', 'pachydermatous', 'painful', 'palm', 'palpate', 'panic-stricken', 'panic-struck', 'panicked', 'panicky', 'partake', 'pat', 'period', 'pertain', 'physical_contact', 'piano', 'pick_up', 'pinch', 'pink', 'pitch', 'placid', 'plow', 'point', 'poise', 'polish', 'politic', 'ponderous', 'postponement', 'press', 'prevail', 'printing', 'project', 'promote', 'puddle', 'punishing', 'push', 'push_button', 'pushful', 'pushing', 'pushy', 'put_up', 'quiet', 'quietly', 'rap', 'rate_of_flow', 'raw', 'reach', 'refer', 'relate', 'relax', 'relaxed', 'release', 'reposition', 'reserve', 'restrain', 'retain', 'rival', 'rouse', 'rub', 'run', 'rush', 'sack', 'saddle', 'sang-froid', 'satisfying', 'savvy', 'scar', 'scrape', 'scrape_up', 'scraping', 'scratch', 'scratch_up', 'scratching', 'self-colored', 'self-coloured', 'send', 'sense', 'sense_of_touch', 'sensitive', 'severe', 'severely', 'shake_off', 'shed', 'shift', 'shift_key', 'shifting', 'shimmy', 'shine', 'shoot', 'shoot_down', 'signature', 'skin', 'skin_senses', 'slack', 'slack_up', 'slacken', 'slip', 'slip ', 'slip_up', 'slow_down', 'smell', 'smooth', 'smooth_out', 'smoothen', 'snag', 'snap', 'snatch', 'soft', 'softly', 'solicit', 'solid', 'solid_state', 'solidness', 'sonant', 'sonorous', 'sore', 'sound', 'soupcon', 'speck', 'spigot', 'spirit', 'spot', 'square', 'stagger', 'stamp', 'stand', 'stick_out', 'still', 'stir', 'stomach', 'stonyhearted', 'stop', 'storage_area', 'stream', 'strike', 'striking', 'stroke', 'strong', 'stumble', 'suave', 'subdued', 'substantial', 'suffer', 'sufferable', 'sullen', 'support', 'supportable', 'surd', 'sustain', 'switch', 'switching', 'tactile_property', 'tactile_sensation', 'tactual_sensation', 'take_for', 'take_hold', 'take_hold_of', 'take_in', 'taking_into_custody', 'tangency', 'tap', 'tapdance', 'tear', 'teddy', 'tender', 'tepid', 'terrified', 'thickened', 'threatening', 'thrill', 'throw', 'throw out', 'throw_away', 'throw_off', 'thrust', 'tilt', 'time_lag', 'tinct', 'tinge', 'tint', 'tip', 'toilsome', 'tolerate', 'tone', 'touch', 'touch_modality', 'touch_on', 'touch_sensation', 'touching', 'tough', 'trace', 'trance', 'tranquil', 'transfer', 'transformation', 'transmutation', 'treat', 'trip', 'trip-up', 'trip_up', 'tug', 'turn around', 'turn_on', 'tutelage', 'unaffixed', 'unanimous', 'unbend', 'unbudging', 'unfeeling', 'unlax', 'unleash', 'unloose', 'unloosen', 'unnerve', 'unruffled', 'unsettle', 'unsettles', 'unstrain', 'unvoiced', 'unwind', 'upstanding', 'view_as', 'voiced', 'voiceless', 'wait', 'wakeless', 'wanton', 'water_faucet', 'water_tap', 'weighed_down', 'weighty', 'whole', 'wield', 'wipe', 'wiretap', 'with_child', 'withstand', 'wobble', 'woolly', 'woolly-headed', 'wooly', 'wooly-minded', 'work_shift']

auditory_digital_word_list = ['acknowledge', 'acquire', 'action', 'activate', 'actuate', 'adjudicate', 'advice', 'aerate', 'affair', 'agree', 'alter', 'alteration', 'appendage', 'architectural_plan', 'ascertain', 'be_after', 'be_intimate', 'bed', 'believe', 'bonk', 'bring_off', 'call_back', 'call_in', 'call_into_question', 'call_up', 'callback', 'care', 'carry_off', 'cerebrate', 'check', 'clear-cut', 'cogitate', 'cognise', 'cognitive_operation', 'cognitive_process', 'cognize', 'come_back', 'commemorate', 'commend', 'common_sense', 'commune', 'communicate', 'commute', 'comprehend', 'con', 'conceive', 'conceptualise', 'conceptualize', 'conscious', 'consider', 'contend', 'contrive', 'convert', 'convey', 'cope', 'count', 'create', 'deal', 'debate', 'decide', 'decided', 'deepen', 'deliberate', 'design', 'determine', 'discover', 'discrete', 'distinct', 'distinguishable', 'do', 'do_it', 'double', 'doubt', 'doubtfulness', 'dubiousness', 'duplicate', 'echo', 'eff', 'empathise', 'empathize', 'enquiry', 'exchange', 'experience', 'fair', 'fairish', 'feel', 'feeling', 'finagle', 'find_out', 'fuck', 'function', 'gestate', 'get_a_line', 'get_by', 'get_it_on', 'get_laid', 'get_wind', 'get_word', 'go_through', 'good_sense', 'grapple', 'guess', 'gumption', 'handle', 'hark_back', 'have_a_go_at_it', 'have_intercourse', 'have_it_away', 'have_it_off', 'have_sex', 'head', 'horse_sense', 'hump', 'imagine', 'incite', 'infer', 'ingeminate', 'inquiry', 'insensitive', 'instruct', 'intend', 'interchange', 'intercommunicate', 'interpret', 'interrogate', 'interrogation', 'interrogative', 'interrogative_sentence', 'interview', 'iterate', 'jazz', 'know', 'larn', 'lie_with', 'litigate', 'live', 'logic', 'logical_system', 'logically', 'look_at', 'love', 'make', 'make_do', 'make_love', 'make_out', "make_up_one's_mind", 'manage', 'map', 'mapping', 'march', 'mathematical_function', 'mean', 'memorise', 'memorize', 'mental_process', 'modification', 'modify', 'moot', 'mother_wit', 'motion', 'motivate', 'move', 'negotiate', 'occasion', 'office', 'officiate', 'operate', 'operation', 'opine', 'opinion', 'oppugn', 'outgrowth', 'oversee', 'pass_along', 'pass_on', 'perceive', 'physical_process', 'pick_up', 'plan', 'procedure', 'process', 'produce', 'profound', 'program', 'programme', 'project', 'prompt', 'propel', 'pull_off', 'purpose', 'put_across', 'query', 'question', 'read', 'realise', 'realize', 'reasonable', 'recall', 'recapitulate', 'receive', 'reckon', 'recognise', 'recognize', 'recollect', 'recollection', 'recur', 'reduplicate', 'regard', 'reiterate', 'remember', 'reminiscence', 'repetition', 'replicate', 'reprise', 'reprize', 'resolve', 'restate', 'retell', 'retrieve', 'return', 'role', 'roll_in_the_hay', 'routine', 'sane', 'screw', 'sensation', 'sense', 'sensible', 'sensory_faculty', 'sentience', 'sentiency', 'serve', 'settle', 'shift', 'signified', 'single-valued_function', 'sleep_together', 'sleep_with', 'smell_out', 'social_function', 'social_occasion', 'spark', 'spark_off', 'statistic', 'statistically', 'study', 'subprogram', 'subroutine', 'sue', 'summons', 'superintend', 'supervise', 'suppose', 'swear_out', 'switch', 'sympathise', 'sympathize', 'system_of_logic', 'take_over', 'teach', 'think', 'think_back', 'think_of', 'touch_off', 'transfer', 'translate', 'transmit', 'treat', 'trenchant', 'trigger', 'trigger_off', 'trip', 'turn_over', 'unconscious_process', 'understand', 'use', 'variety', 'vary', 'wangle', 'weigh', 'wield', 'withdraw', 'witting', 'wonder', 'work', 'work_on']

def rule_based_rs(input):

    output_dict = {"visual": 0, "auditory": 0, "kinesthetic": 0, "auditory_digital": 0}

    data = input
    # set case &
    data = data.lower().strip().replace("\n", "")

    # remove punctuation
    data = data.translate(str.maketrans('', '', string.punctuation))

    # word tokenisation
    data = word_tokenize(data)

    # stemming words
    data = [ps.stem(e) for e in data]

    for word in data:
        if word in visual_word_list:
            output_dict["visual"] += 1
        if word in auditory_word_list:
            output_dict["auditory"] += 1
        if word in kinesthetic_word_list:
            output_dict["kinesthetic"] += 1
        if word in auditory_digital_word_list:
            output_dict["auditory_digital"] += 1

    return json.dumps(output_dict)
