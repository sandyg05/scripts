import scanner


class WordMapper:

    word_mappings = {}  # Prefixes and suffixes.

    def __init__(self):
        self.words = [word for word in scanner.scan() if word]  # Loads every word and stores them in the instance.

    def word_count(self):
        return len(self.words)

    def __make_pairs(self):
        """
        Generates tuple pairs of word and word after it.
        """
        for i in range(len(self.words) - 1):
            yield (self.words[i], self.words[i + 1])

    def map_words(self):
        """
        Updates word_mappings with prefixes and suffixes.
        """

        for word1, word2 in self.__make_pairs():
            WordMapper.word_mappings.setdefault(word1, []).append(word2)

    @staticmethod
    def stats():
        """
        Gets the total word extracted from every book file.
        :return: Count of keys in the word_mappings.
        """
        prefix_count = len(WordMapper.word_mappings.keys())

        suffix_count = 0
        for suffix in WordMapper.word_mappings.keys():
            suffix_count += len(suffix)

        return prefix_count, suffix_count
