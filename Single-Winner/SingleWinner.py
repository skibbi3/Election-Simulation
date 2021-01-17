import math
import numpy as np

def base_vote(voters, candidates, limit=None, optional=False):
    """
    This function is the basic function for all voting systems. It calculates the distance of every candidate from
    every voter and ranks the candidates from closest to the voter to furthest.

    :param voters: a list of (x,y) tuples
    :param candidates: a dictionary with candidate names as key and (x,y) tuple as values
    :param limit: for approval voting and preferential, it limits how many candidates are ranked per voter
    :param random: a boolean value specifying if a random number of candidates per voter should be selected
        used for approval voting and (optional) preferential voting
    :return: list of tuples with candidate names ranked in ascending order of distance, with each line representing
        a voter
    """

    # A list with the order of candidates
    candidate_order = []

    # Orders the candidate by how close to voters
    for voter in voters:
        distances = []
        for candidate in candidates:
            distances.append(
                [math.sqrt((voter[0] - candidates[candidate][0]) ** 2 + (voter[1] - candidates[candidate][1]) ** 2),
                 candidate])
        distances = sorted(distances, key=lambda x: x[0])

        # Sets the vote number to the limit
        vote_number = limit

        # If no limit is given, set the vote number to the number of candidates
        if limit is None:
            vote_number = len(distances)
        
        # If optional voting is enabled, randomly generate a vote number with the old vote number (limit or all candidates) as maximum
        if optional:
            vote_number = np.random.randint(1, vote_number + 1)

        distances = distances[0:vote_number]
      

        candidate_order.append(list(zip(*distances))[1])

    return candidate_order


"""
Plurality voting methods: the winner of the vote is the one with the plurality of votes but not necessarily the
majority. There is only a single round of voting.
"""


def fptp(voters, candidates):
    """
    Replicates First Past the Post voting. Every voter has but one vote and the winner is the candidate with the most
    votes. This function is built on base_vote.

    :param voters: a list of (x,y) tuples representing voter co-ordinates.
    :param candidates: a dictionary of (x,y) tuples keyed by candidate names representing candidate positions.
    :return: a dictionary of candidate names and their vote count.
    """

    # Simply counts up the first entry of each row

    votes = base_vote(voters, candidates)
    candidate_vote = {}

    for vote in votes:

        try:
            candidate_vote[str(vote[0])] += 1
        except:
            candidate_vote[str(vote[0])] = 1

    candidate_vote = {k: candidate_vote[k] for k in sorted(candidate_vote)}

    return candidate_vote


def approval(voters, candidates, optional=False, limit=3):
    """

    :param voters: a list of (x,y) tuples representing voter co-ordinates.
    :param candidates: a dictionary of (x,y) tuples keyed by candidate names representing candidate positions.
    :param optional: a boolean value to allow disable/enable optional preferential (random)
    :param limit: an integer value limiting the amount of preferences
    :return:
    """
    votes = base_vote(voters, candidates, limit=limit, optional=optional)
    candidate_vote = {}

    for vote in votes:

        for i in range(0, len(vote)):
            try:
                candidate_vote[str(vote[i])] += 1
            except:
                candidate_vote[str(vote[i])] = 1

    candidate_vote = {k: candidate_vote[k] for k in sorted(candidate_vote)}
    return candidate_vote


"""
Majoritarian voting methods: uses at least two rounds to ensure the winner is the candidate with the majority of votes
in the final round. These systems use preferences to simulate multiple rounds.
"""


def supplementary_vote(voters, candidates):
    """
    Supplementary Vote simulates a two-round system. There are only two preferences. The top two ranked candidates
    move on to round 2 and only preferences directed to them are counted.

    :param voters: a list of (x,y) tuples representing voter co-ordinates.
    :param candidates: a dictionary of (x,y) tuples keyed by candidate names representing candidate positions.
    :return: a dictionary of candidate names and their vote count.
    """

    # Selecting only the 1st 2 votes per voter
    votes = base_vote(voters, candidates)
    limited_votes = []
    for vote in votes:
        limited_votes.append((vote[0:2]))

    # First round of voting
    candidate_vote = dict.fromkeys(candidates, 0)
    for vote in limited_votes:
        if str(vote[0]) in candidates:
            candidate_vote[str(vote[0])] += 1

    # Selecting the top two candidates
    top_two = sorted(candidate_vote.values(), reverse=True)[0:2]
    remaining_candidates = {}

    for candidate in candidates:
        if candidate_vote[candidate] in top_two:
            remaining_candidates[candidate] = 0

    # The second round of voting using only the two preferences
    remaining_vote = dict.fromkeys(remaining_candidates, 0)
    for vote in limited_votes:
        if str(vote[0]) in remaining_candidates:
            remaining_vote[str(vote[0])] += 1
        elif str(vote[1]) in remaining_candidates:
            remaining_vote[str(vote[1])] += 1

    remaining_vote = {k: remaining_vote[k] for k in sorted(remaining_vote)}

    return remaining_vote


def alternative_vote(voters, candidates, optional=False, limit=None):
    """
    Also known as the Instant Run-off Vote. Voters rank candidates by preference. Lowest ranked candidate is eliminated
    and preferences distributed until there are only two candidates left.

    :param voters: a list of (x,y) tuples representing voter co-ordinates.
    :param candidates: a dictionary of (x,y) tuples keyed by candidate names representing candidate positions.
    :param optional: a boolean value to allow disable/enable optional preferential (random)
    :param limit: an integer value limiting the amount of preferences
    :return: a list of dictionaries with vote total for candidates by round
    """
    remaining_candidates = candidates.copy()
    votes_by_round = []

    votes = base_vote(voters, candidates, limit=limit, optional=optional)

    # Pruning to remove votes based on preferentiality strictness

    # Simulating rounds of voting
    while len(remaining_candidates) > 1:
        candidate_vote = dict.fromkeys(remaining_candidates, 0)

        # Counting the votes
        for vote in votes:
            try:
                candidate_vote[str(vote[0])] += 1
            except IndexError:
                pass

        # Eliminating the least popular
        least_popular = min(candidate_vote, key=candidate_vote.get)
        remaining_candidates.pop(least_popular)
        votes = tuple([[j for j in list(votes[i]) if j != least_popular] for i in range(len(votes))])

        # Sorting candidates
        candidate_vote = {k: candidate_vote[k] for k in sorted(candidate_vote)}

        votes_by_round.append(candidate_vote)

    return votes_by_round