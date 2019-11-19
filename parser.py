import json, os, urllib.parse

def path_to_id(profile_path):
    return profile_path.rstrip('.json').split('/')[-1]

def url_to_topic(url):
    topic = urllib.parse.unquote(url).split('/wiki/')[-1]
    return topic[topic.find(':')+1:].lower()

def get_topics(profile):
    topics = {}
    for url, times in profile.items():
        topic = url_to_topic(url)
        if not topic in topics:
            topics[topic] = times
        else:
            topics[topic] += times
    return topics

# throws FileNotFoundError, IsADirectoryError, json.decoder.JSONDecodeError
def get_profile_by_file(profile_path):
    with open(profile_path) as f:
        profile = json.load(f)
    return {
            'id' : path_to_id(profile_path),
            'topics' : get_topics(profile)
            }
def get_profiles_by_dir(profiles_dir):
    profiles = []
    for filename in os.listdir(profiles_dir):
        if filename.endswith('.json') and not filename.startswith('.'):
            profiles.append(get_profile_by_file(profiles_dir + filename))

    return profiles