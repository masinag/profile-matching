import math

def get_similarity(value1, value2):
    K = 20
    diff = abs(value1-value2)
    return K * math.exp(-(diff**2) / 1000 ) * min(value1, value2)

def match_value(profile1, profile2):
    value = 0
    for topic, times1 in profile1.items():
        if topic in profile2:
            sim = get_similarity(times1, profile2[topic])
            value += sim
    return value
# Assign to each cmp_profile a score based on the similarity of the percentage
# with which every topic has been mentioned by the given profile and the
# cmp_profile
def match(profile, cmp_profiles):
    best_match_id = 0
    best_match_value = 0
    print("\nMatching 1")

    for i, cmp_p in enumerate(cmp_profiles):
        curr_match_value = match_value(profile, cmp_p)
        print("Match with %d: %f" % (i, curr_match_value))
        if curr_match_value > best_match_value:
            best_match_value = curr_match_value
            best_match_id = i
    return best_match_id