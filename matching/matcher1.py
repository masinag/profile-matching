import math

def get_similarity(value1, value2):
    """
    Evaluate the similarity of two discussion percentages for the same topic.
    """
    diff = abs(value1-value2)
    return math.exp(-(diff**2) / 1000 ) * min(value1, value2)

def match_value(profile1, profile2):
    """
    Find a value which evaluates the similarity between the two profiles.

    Each topic which has been discussed by both profiles contributes to the match_value, 
    with a score which is proportional to the similarity of the discussion percentage of 
    the topic in the two profiles and to the lowest of the two percentages.
    """
    value = 0
    for topic, times1 in profile1.items():
        if topic in profile2:
            sim = get_similarity(times1, profile2[topic])
            value += sim
    return value

def match(profile, cmp_profiles):
    """
    Find the profile in cmp_profiles which is most similar to profile.

    Each cmp_profile is assigned a match_value which represent the similarity with profile,
    and the cmp_profile with the highest value is said the most similar.
    The value is computed by confronting the similarity of the percentages with wich each topic
    has been discussed the profiles.

    Args:
        profile: The profile foe which you want to find the most similar one. Each topic should
                 be associated with the percentage of discussions about it over all discussions.
        cmp_profiles: The profiles with which the comparison is done. For each profile, each topic should
                 be associated with the percentage of discussions about it over all discussions of that
                 profile.
    
    Returns:
        A tuple with the index of the cmp_profile most similar to profile and a list with the similarity
        values for each profile.
    """
    best_match_id = 0
    best_match_value = 0
    match_values = []

    for i, cmp_p in enumerate(cmp_profiles):
        curr_match_value = match_value(profile, cmp_p)
        match_values.append(curr_match_value)
        if curr_match_value > best_match_value:
            best_match_value = curr_match_value
            best_match_id = i
    return best_match_id, match_values