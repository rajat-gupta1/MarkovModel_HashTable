from hashtable import Hashtable
import math

HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    """
    This class creates objects with dictionary/hashtable to create a count of
    substrings of size k in the given text. Later, these counts can be used to
    find probability if this object and any other text are from the same source
    or same speaker using log_probability function
    """

    def __init__(self, k, text, use_hashtable):
        """
        Constructs a new k-order markov model using the text 'text'.
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

            # To keep a count of distinct occurences of letters in the string
            if letter not in self.dist_letters:
                self.dist_letters.add(letter)

            # Calling helper function to find the substring k and k+1 from the
            # current character
            k_letters, k1_letters = self.substr_k (text, i, n)
            
            # Incrementing the count if its present
            if k_letters in self.h:
                self.h[k_letters] += 1
            else:
                self.h[k_letters] = 1

            if k1_letters in self.h:
                self.h[k1_letters] += 1
            else:
                self.h[k1_letters] = 1

    def substr_k (self, string, i, n):
        """
        Helper function to find substrings of lengths k and k + 1 from the
        given index
        """

        if i + self.k + 1 >= n:
            # Rolling over to the start
            k1_letters = string[i:] + string[:self.k + 1 - n + i]
        else:
            k1_letters = string[i:i + self.k + 1]
        
        if i + self.k >= n:
            k_letters = string[i:] + string[:self.k - n + i]
        else:
            k_letters = string[i:i + self.k]
        return k_letters, k1_letters

    def log_probability(self, s):
        """
        Log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """

        S = len(self.dist_letters)
        n = len(s)

        prob = 0

        for i in range(n):
            k_letters, k1_letters = self.substr_k (s, i, n)

            try:
                M = self.h[k1_letters]
            # In case the key is not found, returning 0
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
    unidentified speaker (3), this function returns a tuple with the 
    *normalized* log probabilities of each of the speakers uttering that text 
    under a "order" order character-based Markov model, and a conclusion of 
    which speaker uttered the unidentified text based on the two probabilities.
    """

    s1 = Markov(k, speech1, use_hashtable)
    s2 = Markov(k, speech2, use_hashtable)

    n = len(speech3)

    # Finding the two probabilities and normalising them 
    prob1 = s1.log_probability (speech3) / n
    prob2 = s2.log_probability (speech3) / n

    if prob1 > prob2:
        return (prob1, prob2, 'A')
    return (prob1, prob2, 'B')