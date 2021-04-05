import os
import emoji


class PreProcessor:
    def __init__(self, df, text_name):
        self.__df = df
        self.__text_name = text_name
        stopwords_path = os.path.join(os.path.dirname(__file__), 'sin-stop-words.txt')
        self.__stopwords = [l.strip() for l in open(stopwords_path)]

    def demojize_text(self, text):
        return emoji.demojize(text)

    def remove_stop_words(self, text):
        filtered_text = [word for word in text.split() if not word in self.__stopwords]
        filtered_text = (" ").join(filtered_text)
        return filtered_text

    def preprocess_text(self):
        self.__df.dropna()
        self.__df[self.__text_name] = self.__df[self.__text_name].apply(self.remove_stop_words)
        self.__df[self.__text_name] = self.__df[self.__text_name].apply(self.demojize_text)
        return self.__df
