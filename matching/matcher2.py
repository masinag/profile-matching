"""
Implements an algorithm to evaluate the similarity of a user profile 
against a set of existing ones.

Algorithm:

Let cmp_profiles be the set of existing profiles, and let profile be 
the profile of which we want to find the most similar one.

Each cmp_profile is assigned a match_value which represent the 
similarity with profile, and the one with the highest value is said the 
most similar.

When confronting two profiles, it builds a ranking of topics for each 
profile, where the score is represented by the percentage with which 
the topic has been discussed. 
Topics with a similar score belong to the same position in the ranking. 

The match_value of two profiles is computed by confronting the 
similarity of the position of each topic in the rankings of the two 
profiles. 
This value is multiplied by the lowest of the two percentages, so that 
if the two positions are very similar but the corresponding percentages 
are low, this does not contribute much to the match_value.
"""
import math


def get_ranking(profile):
    """
    Build a ranking for the given profile.

    Args:
        profile: The profile for which to build the ranking

    Returns:
        a dictionary where each profile is associated to its position in 
        the ranking
    """

    sorted_topics = sorted(
        profile, key=lambda topic: profile[topic],  reverse=True)
    # a set with the differences between the percentage of two
    # consecutive topics sorted by their percentage
    diffs = {round(profile[sorted_topics[i]]-profile[sorted_topics[i+1]], 3)
             for i in range(len(sorted_topics)-1)}

    # compute the average diff without the min and the max
    if len(diffs) > 2:
        avg_diff = (sum(diffs) - min(diffs) - max(diffs)) / (len(diffs)-2)
    else:
        avg_diff = sum(diffs) / len(diffs)

    # topics are grouped if the difference between the highest
    # percentage and the lowest is less than the average difference
    ranking = {}
    ranking_position = -1
    last_inserted_value = math.inf
    for topic in sorted_topics:
        if last_inserted_value - profile[topic] >= avg_diff:
            ranking_position += 1
            last_inserted_value = profile[topic]
        ranking[topic] = ranking_position
    return ranking, ranking_position + 1


def get_position_similarity(pos1, pos2):
    """
    Evaluate the similarity of positions of a topic in two rankings.

    Args:
        pos1: the position of the topic in the first ranking
        pos2: the position of the topic in the second ranking

    Returns:
        the similarity of the two positions
    """
    diff = abs(pos1-pos2)
    return math.exp(-((2*diff)**2))


def print_ranking(profile, profile_ranking):
    """
    Print the ranking of a profile.

    Args:
        profile: the profile for which to print the ranking.
        profile_ranking: a dictionary where each topic is associated 
            with its position in the profile's ranking
    """
    for t in sorted(profile_ranking, key=lambda x: profile[x], reverse=True):
        print("%d %s: %f" % (profile_ranking[t], t, profile[t]))


def match(profile, cmp_profiles):
    """
    Find the profile in cmp_profiles which is most similar to profile.

    Each cmp_profile is assigned a match_value which represent the 
    similarity with profile, and the cmp_profile with the highest value 
    is said the most similar.
    The algorithm builds a ranking of topics for each profile where the 
    score is represented by the percentage with which the topic has been 
    discussed. Topics with a similar score belong to the same position 
    in the ranking. 
    The match_value of two profiles is computed by confronting the 
    similarity of the position of each topic in the rankings of the two 
    profiles.

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

    profile_ranking, positions = get_ranking(profile)
    # print_ranking(profile, profile_ranking)
    best_match_id = None
    best_match_value = 0

    match_values = []
    for i, cmp_profile in enumerate(cmp_profiles):
        cmp_ranking, cmp_positions = get_ranking(cmp_profile)
        # print("\n\n\n\n")
        # print_ranking(cmp_profile, cmp_ranking)

        curr_match_value = 0
        for topic in profile:
            if topic in cmp_profile:
                pos = profile_ranking[topic] / positions
                cmp_pos = cmp_ranking[topic] / cmp_positions
                topic_value = get_position_similarity(pos, cmp_pos)
                topic_value *= min(profile[topic], cmp_profile[topic])
                curr_match_value += topic_value
        match_values.append(curr_match_value)

        if curr_match_value > best_match_value:
            best_match_value = curr_match_value
            best_match_id = i
    return best_match_id, match_values
