from math import exp
from parser import get_parsed_profile, get_parsed_profiles
K = 100
def values_to_percentage(profile):
    """
    Converts values to percentage
    """

    coeff =  100 / sum(profile.values())
    for topic in profile:
        profile[topic] *= coeff

    # for (k, v) in sorted(profile.items(), key = lambda x : x[1], reverse=True)[:K]:
    #     print(k, v)

def get_similarity(value1, value2):
    K = 20
    diff = abs(value1-value2)
    return K * exp(-(diff**2) / 1000 ) * min(value1, value2)

def match_value(profile1, profile2):
    value = 0
    for topic, times1 in profile1.items():
        if topic in profile2:
            sim = get_similarity(times1, profile2[topic])
            if sim > 5:
                print(topic)
            value += sim
    return value

def match(profile, cmp_profiles, cmp_ids=None, translate=False):
    profile = get_parsed_profile(profile, translate)
    cmp_profiles = get_parsed_profiles(cmp_profiles, translate)
    #to do
    if cmp_ids and not len(cmp_ids) == len(cmp_profiles):
        raise ValueError("")
    values_to_percentage(profile)
    best_match_id = None
    best_match_value = 0

    for i, cmp_p in enumerate(cmp_profiles):
        # print("\n\n\n\nTop %d categories of %s" % (K, cmp_ids[i]))
        values_to_percentage(cmp_p)
        curr_match_value = match_value(profile, cmp_p)
        # to do
        print("Match with %s: %f" % (cmp_ids[i], curr_match_value))
        if curr_match_value > best_match_value:
            best_match_value = curr_match_value
            best_match_id = i
    return best_match_id if not cmp_ids else cmp_ids[best_match_id]