import sys
from parser import get_profile_by_file, get_profiles_by_dir
from matcher import match
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def main(args):
    _, profile = get_profile_by_file(args.profile_path)
    cmp_ids, cmp_profiles = get_profiles_by_dir(args.cmp_profiles_dir)
    print(match(profile, cmp_profiles, cmp_ids, args.translate))

if __name__ == "__main__":
    ap = ArgumentParser(description=
        """
        Evaluates the similarity of a user profile against a set of existing 
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
        the json file containing profile which you want to compare to the existing ones.
        """
    )
    args = ap.parse_args()

   
    main(args)