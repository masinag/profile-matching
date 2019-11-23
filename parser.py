"""
Contains functions to clean-up topic names for a profile and translate 
them if requested. Topic names are translated using the Wikipedia API.
"""
import json
import os
import urllib.parse
import requests
import itertools

_EN = 'en'


def values_to_percentage(profile):
    """
    Convert the times a certain topic has been discussed of to the 
    percentage on the total of discussions.

    Args:
        profile: profile with the topics whose values need to be 
            converted to percentage
    """
    coefficient = 100 / sum(profile.values())
    for topic in profile:
        profile[topic] *= coefficient


def url_to_topic(url):
    """
    Extract the topic from the given url. 

    Args:
        url: url of a Wikipedia category in any language

    Returns:
        the topic, i.e. the name of the category 
    """
    topic = urllib.parse.unquote(url).split('/wiki/')[-1]
    return topic[topic.find(':')+1:]


def url_to_lang(url):
    """
    Extract the language from the given url. 

    Args:
        url: url of a Wikipedia category in any language

    Returns:
        the language of the Wikipedia page
    """
    return urllib.parse.unquote(url).split('://')[1].split('.')[0]


def url_to_lang_topic(url):
    """
    Extract the language and the topic from the given url. 

    Args:
        url: url of a Wikipedia category in any language

    Returns:
        a tuple with the language and the topic of the Wikipedia 
        category
    """
    return (url_to_lang(url), url_to_topic(url))


def normalize_topic_string(topic_string):
    """
    Normalize a topic string. 

    Args:
        topic_string: the string to normalize. It should be in the
            format 'Category:Category name'. The word 'Category' could 
            be in any language, as long as it is followed by a colon

    Returns:
        the string normalized, i.e. the original string where spaces are 
        replaced by underscores and the 'Category:' prefix is removed 
    """
    return topic_string[topic_string.find(':')+1:].replace(' ', '_')


def get_topics(profile):
    """
    Create a new profile where urls are replaced by topic names.

    Args:
        profile: profile where topics are represented by urls of 
            Wikipedia categories

    Returns:
        a new profile where topics are the names of the categories and 
        values are the same as the input profile.
        If two or more urls refer to the same topic, their values are
        summed
    """
    topics = {}
    for url, times in profile.items():
        topic = url_to_topic(url)
        if not topic in topics:
            topics[topic] = times
        else:
            topics[topic] += times
    return topics


def translate_topics(lang, topics):
    """
    Translate topics from lang to English.

    Args:
        lang: language code from which the translation has to be done
        topics: list of topics (names of Wikipedia categories) which 
            have to be translated

    Returns:
        a dictionary where each tuple with the language code and the 
        name of a topic is associated to the name of the topic 
        translated to english, or with the name in the original language 
        if the translation is not available

    Raises:
        requests.exceptions.ConnectionError: if the API do not respond
    """
    # request to Wikipedia API
    TIMEOUT = 5  # raise an error after TIMEOUT sec without response
    topics_titles = 'Category:' + '|Category:'.join(topics)
    request_url = 'https://' + lang + '.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'titles': topics_titles,
        'prop': 'langlinks',
        'lllang': _EN,
        'lllprop': 'url',
        'format': 'json',
        'lllimit': 'max'
    }
    response = requests.get(request_url, params, timeout=TIMEOUT).json()

    # read and parse json response
    translated_dict = {}
    page_list = response['query']['pages']
    for page in page_list:
        page_info = page_list[page]
        topic = normalize_topic_string(page_info['title'])
        if 'langlinks' in page_info:
            translation = normalize_topic_string(
                page_info['langlinks'][0]['*'])
        else:
            translation = topic
        translated_dict[(lang, topic)] = translation

    return translated_dict


def get_translated_topics(to_translate):
    """
    Translate the topics from original languages to English.

    Args:
        to_translate: dictionary where keys are language codes and 
            values are lists of topic names (Wikipedia categories) 

    Returns:
        a dictionary where a tuple with the language code and the name 
        of a topic is associated to the name of the topic translated to 
        English, or with the name in original language if the 
        translation is not available
    """
    LIMIT = 50  # maximum number of queries per request for wikipedia
    translations = {}
    for lang in to_translate:
        for i in range(0, len(to_translate[lang]), LIMIT):
            translations.update(translate_topics(
                lang, itertools.islice(to_translate[lang], i, i+LIMIT)))
    return translations


def get_and_translate_topics(profile):
    """
    Create a profile with topic names translated instead of urls.

    The translation is done only if it is available via Wikipedia API.

    Args:
        profile: profile where topics are urls of Wikipedia categories

    Returns:
        a new profile obtained by replacing topic urls in the original 
        profile with the corresponding category names.
        If two or more urls refer to the same topic, their values are 
        summed
    """
    parsed_profile = {url_to_lang_topic(url): times
                      for url, times in profile.items()}
    to_translate = {}
    topics = {}
    for (lang, topic), times in parsed_profile.items():
        if not lang == _EN:
            if not lang in to_translate:
                to_translate[lang] = []
            to_translate[lang].append(topic)
        else:
            topics[topic] = topics.get(topic, 0) + times
    for original, translation in get_translated_topics(to_translate).items():
        topics[translation] = topics.get(
            translation, 0) + parsed_profile[original]
    return topics


def get_parsed_profile(profile, translate=False):
    """
    Create a profile with topic names instead of urls.

    Args:
        profile: profile where topics are urls to Wikipedia categories
        translated (optional): if set to True, topic names are 
            translated to English when the translation is available

    Returns:
        a new profile obtained by replacing topic urls in the original 
        profile with the corresponding category names.
        if two or more urls refer to the same topic, their values are 
        summed
    """
    get_topics_fn = get_and_translate_topics if translate else get_topics
    return get_topics_fn(profile)


def get_parsed_profiles(profiles, translate=False):
    """
    Create a list of profiles with topic names instead of urls.

    Args:
        profiles: list of profiles where topics are urls of Wikipedia 
            categories
        translated (optional): if set to True, topic names are 
            translated to English when the translation is available

    Returns:
        a list of new profiles obtained by replacing topic urls with the 
        corresponding category names in the original profiles.
        if two or more urls refer to the same topic, their values are 
        summed
    """
    return [get_parsed_profile(profile, translate) for profile in profiles]
