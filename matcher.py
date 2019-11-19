from math import exp

def values_to_percentage(profile):
    coeff =  100 / sum(profile['topics'].values())
    for topic in profile['topics']:
        profile['topics'][topic] *= coeff

def get_similarity(value1, value2):
    K = 20
    diff = abs(value1-value2)
    return K * exp(-(diff**2) / 1000 ) * min(value1, value2)

def match_value(profile1, profile2):
    topics1, topics2 = profile1['topics'], profile2['topics']
    value = 0
    for topic, times1 in topics1.items():
        if topic in topics2:
            value += get_similarity(times1, topics2[topic])
    return value

def match(profile, cmp_profiles):
    values_to_percentage(profile)
    best_match_id = None
    best_match_value = 0

    for cmp_p in cmp_profiles:
        values_to_percentage(cmp_p)
        curr_match_value = match_value(profile, cmp_p)
        print("Match with %s: %f" % (cmp_p['id'], curr_match_value))
        if curr_match_value > best_match_value:
            best_match_value = curr_match_value
            best_match_id = cmp_p['id']
    return best_match_id