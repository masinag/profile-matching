from parser import get_parsed_profile, get_parsed_profiles, values_to_percentage
from matching.matcher1 import match as match1
from matching.matcher2 import match as match2


def match(profile, cmp_profiles, cmp_ids=None, translate=False):
    profile = get_parsed_profile(profile, translate)
    cmp_profiles = get_parsed_profiles(cmp_profiles, translate)

    print(cmp_ids)
    #to do
    if cmp_ids and not len(cmp_ids) == len(cmp_profiles):
        raise ValueError("")
    values_to_percentage(profile)

    for cmp_p in cmp_profiles:
        values_to_percentage(cmp_p)
    
    best_match_id1 = match1(profile, cmp_profiles)
    best_match_id2 = match2(profile, cmp_profiles)
    if not cmp_ids:
        return best_match_id1, best_match_id2
    else:
        return cmp_ids[best_match_id1], cmp_ids[best_match_id2]