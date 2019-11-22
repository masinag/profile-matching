import os, json
from matcher import match
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def path_to_id(profile_path):
    """
    Convert the profile path to an id. 
    
    Args:
        profile_path: The path of the file containing the profile
    
    Returns:
        The file name without the '.json' extension
    """
    return profile_path.rstrip('.json').split('/')[-1]

# throws FileNotFoundError, IsADirectoryError, json.decoder.JSONDecodeError
def get_profile_by_file(profile_path):
    """
    Read the profile from the given file.

    A valid profile contains a dictionary where keys are topic names (in the form 
    of urls of Wikipedia categories) and values are the number of times the profile 
    has spoken about the respective topic.

    Args:
        profile_path: Path to a json file containing a profile.
                      
    Returns:
        A tuple with the file name (without the extension), which is meant to be
        the id of the profile, and the profile itself.
    """
    with open(profile_path) as f:
        profile = json.load(f)
    return path_to_id(profile_path), profile
    
def get_profiles_by_dir(profiles_dir):
    """
    Read the profiles in the given directory.

    Profiles are json files. A valid profile contains a dictionary where keys are 
    topic names (in the form of urls of Wikipedia categories) and values are the 
    number of times the profile has spoken about the respective topic.

    Args:
        profiles_dir: The path to the directory in which to look for profiles.

    Returns:
        A tuple with a list with the file names (without the extension), which are meant 
        to be the ids of the profiles, and a list with the profiles.
    """
    profiles = []
    ids = []
    for filename in os.listdir(profiles_dir):
        if filename.endswith('.json') and not filename.startswith('.'):
            profile_id, profile = get_profile_by_file(profiles_dir + filename)
            ids.append(profile_id)
            profiles.append(profile)

    return ids, profiles

def main(profile_path, cmp_profiles_dir, translate):
    """
    Print the id of the most similar profile to the given one among the ones to compare it with.

    Two algorithms are used to find the most similar profile, and the ids outputed by both are 
    printed.

    Args:
        profile_path: The path of the profile to compare with the existing ones (json)
        cmp_profiles_dir: The dir containing the existing profiles (json)
        translate (bool): If set to True, the topics in foreign laguages are translated
                          to English when possible.
    """
    try:
        _, profile = get_profile_by_file(profile_path)
        cmp_ids, cmp_profiles = get_profiles_by_dir(cmp_profiles_dir)
        results = match(profile, cmp_profiles, cmp_ids)
        for i, (id, match_values) in enumerate(results):
            print("Algorithm %d" % (i+1))
            for j in range(len(match_values)):
                print("Similarity with %s: %f" % (cmp_ids[j], match_values[j]))
            print("Most similar: %s\n" % id)
    except Exception as ex:
        print("An error occurred while doing the matching: %s" % str(ex))

if __name__ == "__main__":
    ap = ArgumentParser(description=
        """
        Evaluates the similarity of a profile against a set of existing 
        ones and returns the id of the most similar one.
        """,
        formatter_class=ArgumentDefaultsHelpFormatter)

    ap.add_argument('-t', '--translate', action='store_true', help = 
        """
        translate the category names to english when possible. Note that it 
        can take some time to translate.
        """
    )
    ap.add_argument('--cmp_profiles_dir', action='store', dest='cmp_profiles_dir', type = str, 
        default = 'tapoi_models/', 
        help=
        """
        directory with the files of the profiles used for the comparison. 
        The directory must contain only these files, and each file must be in 
        json format. See the example files in tapoi_models_exercise directory 
        for more infos.
        """
    )
    ap.add_argument('profile_path', type = str, help=
        """
        the json file containing profile which you want to compare with the existing ones.
        """
    )
    args = ap.parse_args()

   
    main(args.profile_path, args.cmp_profiles_dir, args.translate)