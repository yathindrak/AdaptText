class DataBunchLoader:
    def __init__(self, bs=128, is_backward=False, seed=42, lang='si'):
        self._bs = bs
        self._is_backward = is_backward
        self._seed = seed
        self._lang = lang

    def load(self):
        pass