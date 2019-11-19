import json, os, urllib.parse, requests

_EN = 'en'

def path_to_id(profile_path):
    return profile_path.rstrip('.json').split('/')[-1]

def url_to_topic(url):
    topic = urllib.parse.unquote(url).split('/wiki/')[-1]
    return topic[topic.find(':')+1:].lower()

def url_to_lang(url):
    return urllib.parse.unquote(url).split('://')[1].split('.')[0]

def url_to_lang_topic(url):
    return (url_to_lang(url), url_to_topic(url))

def normalize_topic_string(topic_string):
    return topic_string[topic_string.find(':')+1:].replace(' ', '_').lower()

def get_topics(profile):
    topics = {}
    for url, times in profile.items():
        topic = url_to_topic(url)
        if not topic in topics:
            topics[topic] = times
        else:
            topics[topic] += times
    return topics

def translate_topics(lang, topics):
    assert len(lang) == 2
    topics_titles = 'Category:' + '|Category:'.join(topics)
    request_url = 'https://' + lang + '.wikipedia.org/w/api.php'
    params = {
        'action' : 'query',
        'titles' : topics_titles,
        'prop' : 'langlinks',
        'lllang' : _EN,
        'format' : 'json',
        'lllimit' : 'max'
    }
    response = requests.get(request_url, params).json()

    translated_dict = {}
    page_list = response['query']['pages']
    for page in page_list:
        page_info = page_list[page]
        topic = normalize_topic_string(page_info['title'])
        assert topic in topics
        if 'langlinks' in page_info:
            translation = normalize_topic_string(page_info['langlinks'][0]['*'])
        else:
            translation = topic
        translated_dict[(lang, topic)] = translation
    assert len(lang) == 2
    
    return translated_dict

def get_translated_topics(to_translate):
    LIMIT = 50 # maximum number of queries per request for wikipedia
    translations = {}
    for lang in to_translate:
        for i in range(0, len(to_translate[lang]), LIMIT):
            translations.update(translate_topics(lang, to_translate[lang][i: i+LIMIT]))
    return translations

def get_and_translate_topics(profile):
    parsed_profile = {url_to_lang_topic(url) : times for url, times in profile.items()}
    to_translate = {}
    topics = {}
    for (lang, topic), times in parsed_profile.items():
        if not lang == _EN:
            if not lang in to_translate:
                to_translate[lang] = []
            to_translate[lang].append(topic)
        else:
            topics[topic] = topics.get(topic, 0) + times
    for (lang, topic), translation in get_translated_topics(to_translate).items():
            topics[translation] = topics.get(translation, 0) + parsed_profile[(lang, topic)]
    return topics

# throws FileNotFoundError, IsADirectoryError, json.decoder.JSONDecodeError
def get_profile_by_file(profile_path, translate):
    with open(profile_path) as f:
        profile = json.load(f)

    get_topics_fn = get_and_translate_topics if translate else get_topics

    return {
            'id' : path_to_id(profile_path),
            'topics' : get_topics_fn(profile)
            }
def get_profiles_by_dir(profiles_dir, translate):
    profiles = []
    for filename in os.listdir(profiles_dir):
        if filename.endswith('.json') and not filename.startswith('.'):
            profiles.append(get_profile_by_file(profiles_dir + filename, translate))

    return profiles