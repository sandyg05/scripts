import numpy as np


# TODO A better algorithm than this.
def chain_words(mapping, word_count):
    """
    Chains words from the mapping.
    :param mapping: The mapping of prefixes and suffixes.
    :param word_count: How many words to chain.
    :return: Chained sentence.
    """

    # Caching every word that a sentence can start with.
    first_words = [word for word
                   in mapping.keys()
                   if word[0].isalpha() and word[0].isupper()]

    first_word = np.random.choice(first_words)
    chain = [first_word]

    for _ in range(word_count - 1):
        chain.append(np.random.choice(mapping[chain[-1]]))  # Adds a suffix mapped to the prefix

    return ' '.join(chain)
