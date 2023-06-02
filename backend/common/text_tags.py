from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk import word_tokenize, Text, download


class TextTags:
    @staticmethod
    def _stopword_create():
        try:
            en_stopwords = stopwords.words('english')
        except LookupError:
            download('stopwords')
            en_stopwords = stopwords.words('english')

        en_stopwords += [',', '.', '“', 'I', ':', '’', '”', "''", '``', 'In', "'s", ')', '(', 'The']

        return en_stopwords

    def get_tags(self, text: str, number: int = 10):
        try:
            tokens = word_tokenize(text)
        except LookupError:
            download('punkt')
            tokens = word_tokenize(text)

        text_tokens = [token.strip() for token in tokens if token not in self._stopword_create()]
        text = Text(text_tokens)
        f_dist_sw = FreqDist(text)

        return f_dist_sw.most_common(number)
