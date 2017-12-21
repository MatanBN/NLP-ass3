FUNCTION_WORDS = set(["the", ",", ".", "a", "an", "and", "or", "be", "who", "he", "she", "it", "is", "are", "of",
                      "in", "to", "'s", "with", "''", '``', "have", "has", "this", "that", "for",
                      "by", "his", "from", "their", "not", "it", "at", "her", "which", "on", "(", ")",
                      "without", "between", "anybody", "they", "my", "more", "much", "either", "neither",
                      "when", "while", "although", "am", "got", "do", "as",
                      "but", ";", "-", "this", "one", "also", "after", "therefore",
                      "could", "can"])


class ContextStrategy(object):
    def __init__(self):
        pass

    def get_context(self, sentence):
        """

        :param sentence: a list, containing strings of a single word in the Depparse format.
        :return: context: a 2d list, each ith list contains the context of the ith word.
        (according to the strategy).
        """
        raise NotImplementedError


class WindowContextWord(object):
    def __init__(self, window_size=2):
        self._window_size = window_size

    def get_context(self, sentence):
        """

        :param sentence: a list, containing strings of a single word in the Depparse format.
        :return: context: a 2d list, each ith list contains the words left and right to the ith word
        the number of words to the left and right is determined by the window_size variable
        (default is 2).
        """
        lemma_words = filter(lambda word: word not in FUNCTION_WORDS,
                             [current_sentence.split('\t')[2] for current_sentence in sentence])
        num_of_words = len(lemma_words)
        context = list()
        for i in range(0, num_of_words):
            context.append(lemma_words[max(0, i - self._window_size):i]
                           + lemma_words[i + 1: min(num_of_words, i + self._window_size + 1)])
        return lemma_words, context


class DependecyContextWord(object):
    def __init__(self):
        pass

    def get_context(self, sentence):

        """

        :param sentence: a list, containing strings of a single word in the Depparse format.
        :return: context: a 2d list, each ith list contains the dependency context of the ith word.
        """
        num_of_words = len(sentence)
        words = list()
        context = list()
        lemma_words = list()

        for word in sentence:
            parsed_word = word.split('\t')
            words.append(parsed_word)
            context.append(list())
            lemma_words.append(parsed_word[2])

        filtered_lemma_words = filter(lambda word: word not in FUNCTION_WORDS, lemma_words)
        for i in range(0, num_of_words):
            dependency_id = int(words[i][6]) - 1
            dependency_label = words[i][7]
            if dependency_id != -1:
                if lemma_words[dependency_id] not in FUNCTION_WORDS and lemma_words[i] not in FUNCTION_WORDS:
                    context[i].append(lemma_words[dependency_id] + " -> " + dependency_label)
                    context[dependency_id].append(lemma_words[i] + " <- " + dependency_label)
        context = [x for x in context if x != []]
        return filtered_lemma_words, context


class CoContextWord(object):
    def __init__(self):
        pass

    def get_context(self, sentence):
        """

        :param sentence: a list, containing strings of a single word in the Depparse format.
        :return: context: a list, containing strings that represent the context of the word in the given
        index. (according to the strategy).
        """

        lemma_words = [current_sentence.split('\t')[2] for current_sentence in sentence]
        lemma_words = filter(lambda word: word not in FUNCTION_WORDS, lemma_words)

        num_of_words = len(lemma_words)
        context = list()
        for i in range(0, num_of_words):
            current_context = lemma_words[:i] + lemma_words[i + 1:]
            context.append(current_context)
        return lemma_words, context


def CoContextStrategySimpleTest():
    ccw = CoContextWord()
    sentence = ["1\tThe\tthe\tIN\tIN\t_\t2\tsimpledet\t_\t_\r\n", "2\tdog\tdog\tNN\tNN\t_\t0\t_\t_\t_\r\n",
                "3\tate\teat\tVB\tVB\t_\t2\tpartmod\t_\t_\r\n",
                "4\tmy\tmy\tIN\tIN\t_\t5\tposs\t_\t_\r\n", "5\thomework\thomework\tNN\tNN\t_\t0\t_\t_\t_\r\n"]
    words, context = ccw.get_context(sentence)

    assert len(context) == 3
    assert len(words) == 3

    assert context[0] == ['eat', 'homework'] and words[0] == 'dog'
    print "Passed zero index test"
    assert context[1] == ['dog', 'homework'] and words[1] == 'eat'
    print "Passed first index test"
    assert context[2] == ['dog', 'eat'] and words[2] == 'homework'


def WindowContextWordSimpleTest():
    wcw = WindowContextWord(2)
    sentence = ["1\tThe\tthe\tIN\tIN\t_\t2\tsimpledet\t_\t_\r\n", "2\tdog\tdog\tNN\tNN\t_\t0\t_\t_\t_\r\n",
                "3\tate\teat\tVB\tVB\t_\t2\tpartmod\t_\t_\r\n",
                "4\tmy\tmy\tIN\tIN\t_\t5\tposs\t_\t_\r\n", "5\thomework\thomework\tNN\tNN\t_\t0\t_\t_\t_\r\n"]
    words, context = wcw.get_context(sentence)
    assert len(context) == 3
    assert len(words) == 3

    assert context[0] == ['eat', 'homework'] and words[0] == 'dog'
    print "Passed zero index test"
    assert context[1] == ['dog', 'homework'] and words[1] == 'eat'
    print "Passed first index test"
    assert context[2] == ['dog', 'eat'] and words[2] == 'homework'

    print "Passed window occurrence test"


def DependencyContextWordSimpleTest():
    # Still under construction.
    wcw = DependecyContextWord()
    sentence = ["1\tThe\tthe\tIN\tIN\t_\t2\tsimpledet\t_\t_\r\n", "2\tdog\tdog\tNN\tNN\t_\t0\t_\t_\t_\r\n",
                "3\tate\teat\tVB\tVB\t_\t2\tpartmod\t_\t_\r\n",
                "4\tmy\tmy\tIN\tIN\t_\t5\tposs\t_\t_\r\n", "5\thomework\thomework\tNN\tNN\t_\t0\t_\t_\t_\r\n"]
    words, context = wcw.get_context(sentence)

    assert len(context) == 2
    assert len(words) == 3
    assert context[0] == ["eat <- partmod"] and words[0] == 'dog'
    print "Passed zero index test"
    assert context[1] == ['dog -> partmod'] and words[1] == 'eat'
    print "Passed first index test"
    assert words[2] == 'homework'

    print "Passed dependency occurrence test"


if __name__ == "__main__":
    WindowContextWordSimpleTest()
    CoContextStrategySimpleTest()
    DependencyContextWordSimpleTest()
