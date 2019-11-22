import math

#todo manage len < 3
def get_ranking(profile):
    sorted_topics = sorted(profile, key = lambda topic : profile[topic],  reverse=True)
    # get diffs
    diffs = {round(profile[sorted_topics[i]]-profile[sorted_topics[i+1]], 3) for i in range(len(sorted_topics)-1)}
    if len(diffs) > 2:
        avg_diff = (sum(diffs) - min(diffs) - max(diffs)) / (len(diffs)-2) 
    else:
        avg_diff = sum(diffs) / len(diffs)
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
    diff = abs(pos1-pos2)
    return math.exp(-((2*diff)**2))

def print_ranking(profile, profile_ranking):
    for t in sorted(profile_ranking, key = lambda x : profile[x], reverse = True):
        print("%d %s: %f" % (profile_ranking[t], t, profile[t]))

# Group topics based on the percentage of how many times they have been mentioned.
# Create a ranking of grouped profiles and order them in descending order
# Assign a value to each profile: for each topic, assign a value based on the
# similarity of the position of the topic in the 2 profiles rankings
def match(profile, cmp_profiles):
    # categories are done based on if the difference between values is bigger or equal
    # than the average difference between two consecutive values
    profile_ranking, positions = get_ranking(profile)
    # print_ranking(profile, profile_ranking)
    best_match_id = None
    best_match_value = 0
    print("\nMatching 2:")
    for i, cmp_profile in enumerate(cmp_profiles):
        cmp_ranking, cmp_positions = get_ranking(cmp_profile)
        # print("\n\n\n\n")
        # print_ranking(cmp_profile, cmp_ranking)

        curr_match_value = 0
        for topic in profile:
            if topic in cmp_profile:
                topic_value = get_position_similarity(profile_ranking[topic]/ positions, cmp_ranking[topic] / cmp_positions)
                topic_value *= min(profile[topic], cmp_profile[topic])
                curr_match_value += topic_value
        print("Match with %d: %f" % (i, curr_match_value))
        if curr_match_value > best_match_value:
            best_match_value = curr_match_value
            best_match_id = i
    return best_match_id



