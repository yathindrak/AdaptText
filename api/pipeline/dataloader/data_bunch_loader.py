class DataBunchLoader:
    def __init__(self, bs=128, is_backward=False, seed=42, lang='si'):
        self.__bs = bs
        self.__is_backward = is_backward
        self.__seed = seed
        self.__lang = lang

    def load(self):
        pass