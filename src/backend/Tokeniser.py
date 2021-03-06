import re
import nltk

from backend.FilesIO import FilesIO


"""

"""
class Tokeniser:

    io = FilesIO()
    stopwords = io.lineSeparatedToList('data/lists/stopwords.txt')
    stopstrings = io.lineSeparatedToList('data/lists/stopstrings.txt')
    nltk.download('wordnet')


    def splitByWord(self, text):
        """


        Arguments:
        text (string)
            --

        Returns:
        words ([string])
            --
        """
        text = self.__removeNewLines(text)
        text = self.__removePunctuation(text)
        words = text.split(' ')
        words = self.__lowerCaseWords(words)
        words = self.__removeStopstrings(words)
        words = list(self.__removeIntegers(words))
        words = self.__removeEmpties(words)
        words = self.__lemmatise(words)
        return words

    def splitBySentence(self, text):
        """


        Arguments:
        text (string)
            --

        Returns:
        senetences ([string])
            --
        """
        text = ''.join(i for i in text if not i.isdigit())
        sentenceBlocks = self.__separatingIntoSentenceBlocks(text)
        sentences = self.__removeEmpties(sentenceBlocks)
        return sentences

    def removeSentencesWithoutPhrases(self, phrases, sentences):
        """


        Arguments:
        phrases   ([string])
            --
        sentences ([string])
            --

        Returns:
        sentencesWithPhrases ([string])
            --
        """
        sentencesWithPhrases = []
        for sentence in sentences:
            cleanedSentence = self.__cleanSentence(sentence)
            for phrase in phrases:
                if cleanedSentence.rfind(phrase) is not -1:
                    sentencesWithPhrases.append(sentence)
                    break
        return sentencesWithPhrases


    def __removeNewLines(self, text):
        """


        Arguments:
        text (string)
            --

        Returns:
        text (string)
            --
        """
        text = text.replace('-\n', '')
        text = text.replace('\n', ' ')
        text = text.replace('\x0c', '')
        text = text.replace('—', ' ')
        return text

    def __removePunctuation(self, text):
        """


        Arguments:
        text (string)
            --

        Returns:
        text (string)
            --
        """
        punctuation = re.compile(r'[.?…!,¸_/"º`\'‘“””’%:;*()[\]<>{}0-9]')
        text = punctuation.sub("", text)
        return text


    def __lowerCaseWords(self, words):
        """


        Arguments:
        words ([string])
            --

        Returns:
        lowerCaseWords ([string])
            --
        """
        lowerCaseWords = []
        for w in words:
            if w[1:].islower():
                lowerCaseWords.append(w.lower())
        return lowerCaseWords

    def removeStopwords(self, words):
        """


        Arguments:
        words ([string])
            --

        Returns:
        wordsWOstops ([string])
            --
        """
        wordsWOstops = []
        for w in words:
            if w not in self.stopwords:
                wordsWOstops.append(w)
        return wordsWOstops

    def __removeStopstrings(self, words):
        """


        Arguments:
        words ([string])
            --

        Returns:
        wordsWOstops ([string])
            --
        """
        wordsWOstops = []
        for w in words:
            stopInW = False
            for string in self.stopstrings:
                if string in w:
                    stopInW = True
            if not stopInW:
                wordsWOstops.append(w)
        return wordsWOstops

    def __removeIntegers(self, words):
        """


        Arguments:
        words ([string])
            --
        """
        for w in words:
            try:
                int(w)
                continue
            except ValueError:
                yield w

    def __lemmatise(self, words):
        """


        Arguments:
        words ([string])
            --

        Returns:
        lemmatisedWords ([string])
            --
        """
        lemmatisedWords = []
        lemma = nltk.wordnet.WordNetLemmatizer()
        for w in words:
            l = lemma.lemmatize(w)
            lemmatisedWords.append(l)
        return lemmatisedWords


    def __removeEmpties(self, words):
        """


        Arguments:
        words ([string])
            --

        Returns:
        words ([string])
            --
        """
        while '' in words:
            words.remove('')
        return words

    def __separatingIntoSentenceBlocks(self, text):
        """


        Arguments:
        text (string)
            --

        Returns:
        sentences ([string])
            --
        """
        pars = text.split("\n\n")
        parsSplitBySentence = []
        for p in pars:
            if isinstance(p, str):
                pNoNewLines = self.__removeNewLines(p)
                parsSplitBySentence.append(pNoNewLines.split(". "))
                sentencesWempties = [sentence for sublist in parsSplitBySentence for sentence in sublist]
                sentences = [x for x in sentencesWempties if x]
        return sentences

    def __cleanSentence(self, sentence):
        """


        Arguments:
        sentence (string)
            --

        Returns:
        cleanedSentence (string)
            --
        """
        cleanedSentence = []
        sentence = self.__removeNewLines(sentence)
        sentence = self.__removePunctuation(sentence)
        words = sentence.split(' ')
        words = self.__lowerCaseWords(words)
        words = list(self.__removeIntegers(words))
        words = self.__removeEmpties(words)
        cleanedSentence = ' '.join(words)
        return cleanedSentence
