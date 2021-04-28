import os
import emoji


class PreProcessor:
    """Preprocessing module"""
    def __init__(self, df, text_name):
        self.__df = df
        self.__text_name = text_name
        stopwords_path = os.path.join(os.path.dirname(__file__), 'sin-stop-words.txt')
        self.__stopwords = [l.strip() for l in open(stopwords_path)]

    def demojize_text(self, text):
        """
        Convert emojis into words
        @rtype: object
        """
        return emoji.demojize(text)

    def remove_stop_words(self, text):
        """
        Remove stop words
        @rtype: object
        """
        filtered_text = [word for word in text.split() if not word in self.__stopwords]
        filtered_text = (" ").join(filtered_text)
        return filtered_text

    def preprocess_text(self):
        """
        Preprocess dataframe
        @rtype: object
        """
        self.__df.dropna()
        self.__df[self.__text_name] = self.__df[self.__text_name].apply(self.remove_stop_words)
        self.__df[self.__text_name] = self.__df[self.__text_name].apply(self.demojize_text)

