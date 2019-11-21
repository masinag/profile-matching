from math import exp

def values_to_percentage(profile):
    """
    Converts values to percentage
    """
    coeff =  100 / sum(profile.values())
    for topic in profile:
        profile[topic] *= coeff

def get_similarity(value1, value2):
    K = 20
    diff = abs(value1-value2)
    return K * exp(-(diff**2) / 1000 ) * min(value1, value2)

def match_value(profile1, profile2):
    value = 0
    for topic, times1 in profile1.items():
        if topic in profile2:
            value += get_similarity(times1, profile2[topic])
    return value

def match(profile, cmp_profiles, cmp_ids=None):
    #to do
    if cmp_ids and not len(cmp_ids) == len(cmp_profiles):
        raise ValueError("")
    values_to_percentage(profile)
    best_match_id = None
    best_match_value = 0

    for i, cmp_p in enumerate(cmp_profiles):
        values_to_percentage(cmp_p)
        curr_match_value = match_value(profile, cmp_p)
        # to do
        print("Match: %f" % (curr_match_value))
        if curr_match_value > best_match_value:
            best_match_value = curr_match_value
            best_match_id = i
    return best_match_id if not cmp_ids else cmp_ids[best_match_id]