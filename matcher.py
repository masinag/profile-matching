from parser import get_parsed_profile, get_parsed_profiles, values_to_percentage
from matching.matcher1 import match as match1
from matching.matcher2 import match as match2


def match(profile, cmp_profiles, cmp_ids=None, translate=False):
    """
    Find the most similar profile to the given one among cmp_profiles.

    The matching is done with two algorithms and both the results are returned.

    Args:
        profile: The profile foe which you want to find the most similar one.
        cmp_profiles: The profiles with which the comparison is done.
        cmp_ids (optional): The ids of the cmp_profiles
        translated(optional): If set to True, the topics of profiles are translated to 
                              English when the translation is available.
                            
    Returns:
        A list with a tuple for each of the algorithms.
        The tuple contains the id of the most similar profile returned by the 
        algoritm, and a list of similarity values computed by it.
    """
    profile = get_parsed_profile(profile, translate)
    cmp_profiles = get_parsed_profiles(cmp_profiles, translate)
    
    if cmp_ids and not len(cmp_ids) == len(cmp_profiles):
        raise ValueError("cmp_ids size and cmp_profiles size do not correspond")
    values_to_percentage(profile)

    # both matching algorithms are based on the percentage of the number of times
    # the profile has spoken about a topic on the total of times the profile has spoken
    # of something
    for cmp_p in cmp_profiles:
        values_to_percentage(cmp_p)
    
    best_match_id1, match_values1 = match1(profile, cmp_profiles)
    best_match_id2, match_values2 = match2(profile, cmp_profiles)

    if cmp_ids:
        best_match_id1 = cmp_ids[best_match_id1]
        best_match_id2 = cmp_ids[best_match_id2]
    
    return [(best_match_id1, match_values1), (best_match_id2, match_values2)]