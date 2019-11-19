import sys
from parser import get_profile_by_file, get_profiles_by_dir

def main(profile_path, cmp_profiles_dir):
    profile_to_match = get_profile_by_file(profile_path)
    profiles_to_cmp = get_profiles_by_dir(cmp_profiles_dir)

    

if __name__ == "__main__":
    profile_path = sys.argv[1] or "tapoi_models/roger.json"
    cmp_profiles_dir = "tapoi_models/"
    main(profile_path, cmp_profiles_dir)