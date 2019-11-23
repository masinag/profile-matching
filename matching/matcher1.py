"""
Implements an algorithm to evaluate the similarity of a user profile 
against a set of existing ones.

Algorithm:

Let cmp_profiles be the set of existing profiles, and let profile be 
the profile of which we want to find the most similar one.

Each cmp_profile is assigned a match_value which represent the 
similarity with profile, and the one with the highest value is said the 
most similar.

When confronting two profiles, each topic which has been discussed by 
both profiles contributes to the match_value with a score which is 
proportional to the similarity of the discussion percentage of the topic 
in the two profiles. 

This value is multiplied by the lowest of the two percentages, so that 
if the two percentages are very similar but they are very low, this does 
not contribute much to the match_value.
"""
import math


def get_similarity(value1, value2):
    """
    Evaluate the similarity of two discussion percentages for a topic.

    Args:
        value1: discussion percentage of the topic in the first profile
        value2: discussion percentage of the topic in the second profile

    Returns:
        A value representing the similarity of the two percentages.
    """
    diff = abs(value1-value2)
    return math.exp(-(diff**2) / 1000) * min(value1, value2)


def match_value(profile1, profile2):
    """
    Evaluate the similarity of two profiles.

    Each topic discussed by both profiles contributes to the match_value
    with a score proportional to the similarity of its discussion 
    percentages in the two profiles and to the lowest of the two values.

    Args:
        profile1: first profile to compare
        profile2: second profile to compare

    Returns:
        The match value which evaluates the similarity between the two 
        profiles
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

    Each cmp_profile is assigned a match_value which represents the 
    similarity with profile. The cmp_profile with the highest value is 
    said the most similar.
    The value is computed by confronting the the percentages with which 
    each topic has been discussed by the profiles.

    Args:
        profile: the profile for which to find the most similar one. 
            Each topic should be associated with its percentage of 
            discussions over all discussions
        cmp_profiles: list of profiles with which the comparison is 
            done. For each profile, each topic should be associated 
            with its percentage of discussion over all discussions of 
            the profile

    Returns:
        a tuple with the index of the cmp_profile most similar to 
        profile and a list with the similarity values for each profile
    """
    best_match_id = None
    best_match_value = 0
    match_values = []

    for i, cmp_p in enumerate(cmp_profiles):
        curr_match_value = match_value(profile, cmp_p)
        match_values.append(curr_match_value)
        if curr_match_value > best_match_value:
            best_match_value = curr_match_value
            best_match_id = i
    return best_match_id, match_values
