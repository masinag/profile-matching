"""
Contains the functions to do the comparison between the profile and the 
cmp_profiles and to get the most similar one. It uses functions defined 
in the matching package.
"""
from .parsing.parser import get_parsed_profile, get_parsed_profiles, \
    values_to_percentage
from .algorithm1 import match as match1
from .algorithm2 import match as match2


def match(profile, cmp_profiles, cmp_ids=None, translate=False):
    """
    Find the most similar profile to the given one among cmp_profiles.

    The matching is done with two algorithms and both the results are 
    returned.

    Args:
        profile: the profile for which you want to find the most similar 
            one
        cmp_profiles: the profiles with which the comparison is done
        cmp_ids (optional): the ids of the cmp_profiles
        translated(optional): if set to True, the topics of profiles are 
            translated to English when the translation is available

    Returns:
        a list with a tuple for each of the algorithms.
        Each tuple contains the id of the most similar profile returned 
        by the algorithm, and a list of similarity values computed by it
    """
    profile = get_parsed_profile(profile, translate)
    cmp_profiles = get_parsed_profiles(cmp_profiles, translate)

    if cmp_ids and not len(cmp_ids) == len(cmp_profiles):
        raise ValueError(
            "cmp_ids size and cmp_profiles size do not correspond")
    values_to_percentage(profile)

    # both matching algorithms are based on the percentage of the number
    # of times the profile has spoken about a topic on the total of
    # times the profile has spoken about something
    for cmp_p in cmp_profiles:
        values_to_percentage(cmp_p)

    best_match_id1, match_values1 = match1(profile, cmp_profiles)
    best_match_id2, match_values2 = match2(profile, cmp_profiles)

    if cmp_ids:
        best_match_id1 = cmp_ids[best_match_id1]
        best_match_id2 = cmp_ids[best_match_id2]

    return [(best_match_id1, match_values1), (best_match_id2, match_values2)]
