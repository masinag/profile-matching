import sys
from parser import get_profile_by_file, get_profiles_by_dir
from matcher import match

def main(profile_path, cmp_profiles_dir):
    translate = True
    profile = get_profile_by_file(profile_path, translate)
    cmp_profiles = get_profiles_by_dir(cmp_profiles_dir, translate)

    print(match(profile, cmp_profiles))

if __name__ == "__main__":
    profile_path = sys.argv[1]
    cmp_profiles_dir = "tapoi_models/"
    main(profile_path, cmp_profiles_dir)