import os
import json
import requests
from matcher import match
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def path_to_id(profile_path):
    """
    Convert the profile path to an id. 

    Args:
        profile_path: the path of the file containing the profile

    Returns:
        the file name without the '.json' extension
    """
    return profile_path.rstrip('.json').split('/')[-1]

# throws


def get_profile_by_file(profile_path):
    """
    Read the profile from the given file.

    A valid profile contains a dictionary where keys are topic names 
    (in the form of urls of Wikipedia categories) and values are the 
    number of times the profile has spoken about the respective topic.

    Args:
        profile_path: path to a json file containing a profile

    Returns:
        a tuple with the file name (without the extension), which is 
        meant to be the id of the profile, and the profile itself

    Raises:
        FileNotFoundError: the file is missing
        IsADirectoryError: the profile_path is a path to a directory
        json.decoder.JSONDecodeError: the given is not a valid json file
    """
    try:
        with open(profile_path) as f:
            profile = json.load(f)
    except json.decoder.JSONDecodeError as ex:
        raise json.decoder.JSONDecodeError(ex.msg, profile_path, ex.pos)
    return path_to_id(profile_path), profile


def get_profiles_by_dir(profiles_dir):
    """
    Read the profiles in the given directory.

    Profiles are json files. A valid profile contains a dictionary where 
    keys are topic names (in the form of urls of Wikipedia categories) 
    and values are the number of times the profile has spoken about the 
    respective topic.

    Args:
        profiles_dir: the path to the directory in which to look for 
            profiles

    Returns:
        a tuple with a list with the file names (without the extension), 
        which are meant to be the ids of the profiles, and a list with 
        the profiles

    Raises:
        IsADirectoryError: there is a subdirectory with '.json' 
            extension
        json.decoder.JSONDecodeError: there is a file with '.json' 
            extension which is not a valid json file
    """
    profiles = []
    ids = []
    if not profiles_dir.endswith('/'):
        profiles_dir += '/'
    for filename in os.listdir(profiles_dir):
        if filename.endswith('.json') and not filename.startswith('.'):
            profile_id, profile = get_profile_by_file(profiles_dir + filename)
            ids.append(profile_id)
            profiles.append(profile)

    return ids, profiles


def main(profile_path, cmp_profiles_dir, translate):
    """
    Print the id of the most similar profile to the given one among the 
    ones to compare it with.

    Two algorithms are used to find the most similar profile, and the 
    ids returned by both are printed. For each algorithm the evaluated 
    similarity values with each profile are also printed.

    Args:
        profile_path: the path of the profile to compare with the 
            existing ones (json)
        cmp_profiles_dir: the dir containing the existing profiles 
            (json)
        translate (bool): if set to True, the topics in foreign 
            languages are translated to English when possible
    """
    try:
        _, profile = get_profile_by_file(profile_path)
        cmp_ids, cmp_profiles = get_profiles_by_dir(cmp_profiles_dir)
        results = match(profile, cmp_profiles, cmp_ids, translate)
        for i, (id, match_values) in enumerate(results):
            print("Algorithm %d" % (i+1))
            for j in range(len(match_values)):
                print("Similarity with %s: %f" % (cmp_ids[j], match_values[j]))
            print("Most similar: %s\n" % id)
    except (FileNotFoundError, IsADirectoryError) as ex:
        print("Bad file name: %s" % (str(ex)))
    except (json.decoder.JSONDecodeError) as ex:
        print("Error while parsing %s: %s" % (ex.doc, str(ex)))
    except requests.exceptions.ConnectionError as ex:
        print("Error during the connection to Wikipedia API: %s" % (str(ex)))


if __name__ == "__main__":
    ap = ArgumentParser(description="""
        Evaluates the similarity of a profile against a set of existing 
        ones and returns the id of the most similar one.
        """, formatter_class=ArgumentDefaultsHelpFormatter)

    ap.add_argument('-t', '--translate', action='store_true', help="""
        translate the category names to english when possible. Note that 
        it can take some time to translate
        """)
    ap.add_argument('--cmp_profiles_dir', action='store',
        dest='cmp_profiles_dir', type=str, default='tapoi_models/',
        help="""
        directory with the files of the profiles used for the 
        comparison. The directory must contain only these files, and 
        each file must be in json format. See the example files in 
        tapoi_models directory for more infos
        """)
    ap.add_argument('profile_path', type=str, help="""
        the json file containing profile which you want to compare with 
        the existing ones
        """)
    args = ap.parse_args()

    main(args.profile_path, args.cmp_profiles_dir, args.translate)
