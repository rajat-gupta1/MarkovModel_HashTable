
HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    def __init__(self, k, text, use_hashtable):
        """
        Construct a new k-order markov model using the text 'text'.
        """

    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """


def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """
