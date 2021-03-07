import os
import emoji


class TextPreProcessor:
    def __init__(self, df, text_name):
        self.df = df
        self.text_name = text_name
        stopwords_path = os.path.join(os.path.dirname(__file__), 'sin-stop-words.txt')
        self.stopwords = [l.strip() for l in open(stopwords_path)]

    def demojize_text(self, text):
        return emoji.demojize(text)

    def remove_stop_words(self, text):
        filtered_text = [word for word in text.split() if not word in self.stopwords]
        filtered_text = (" ").join(filtered_text)
        return filtered_text

    def preprocess_text(self):
        self.df.dropna()
        self.df[self.text_name] = self.df[self.text_name].apply(self.remove_stop_words)
        self.df[self.text_name] = self.df[self.text_name].apply(self.demojize_text)
        return self.df
