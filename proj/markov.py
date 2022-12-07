from hashtable import Hashtable
import math

HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    def __init__(self, k, text, use_hashtable):
        """
        Construct a new k-order markov model using the text 'text'.
        """
        self.k = k
        self.text = text
        self.use_hashtable = use_hashtable
        if use_hashtable:
            self.h = Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO)
        else:
            self.h = dict()

        self.dist_letters = set()
        n = len(text)
        for i, letter in enumerate(text):

            if letter not in self.dist_letters:
                self.dist_letters.add(letter)
            if i + k >= n:
                k_letters = text[i:] + text[:k - n + i]
            else:
                k_letters = text[i:i + k]

            if i + k + 1 >= n:
                k1_letters = text[i:] + text[:k + 1 - n + i]
            else:
                k1_letters = text[i:i + k + 1]
            
            if k_letters in self.h:
                self.h[k_letters] += 1
            else:
                self.h[k_letters] = 1

            if k1_letters in self.h:
                self.h[k1_letters] += 1
            else:
                self.h[k1_letters] = 1
            

    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """
        S = len(self.dist_letters)
        n = len(s)

        prob = 0

        for i in range(n):
            if i + self.k + 1 >= n:
                k1_letters = s[i:] + s[:self.k + 1 - n + i]
            else:
                k1_letters = s[i:i + self.k + 1]
            
            if i + self.k >= n:
                k_letters = s[i:] + s[:self.k - n + i]
            else:
                k_letters = s[i:i + self.k]

            try:
                M = self.h[k1_letters]
            except KeyError:
                M = 0
            try:
                N = self.h[k_letters]
            except KeyError:
                N = 0

            prob = prob + math.log((M + 1) / (N + S))
        return prob

def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """

    s1 = Markov(k, speech1, use_hashtable)
    s2 = Markov(k, speech2, use_hashtable)

    n = len(speech3)

    prob1 = s1.log_probability (speech3) / n
    prob2 = s2.log_probability (speech3) / n

    if prob1 > prob2:
        return (prob1, prob2, 'A')
    return (prob1, prob2, 'B')