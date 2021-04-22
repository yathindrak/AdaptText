class Trainer:
    """Base Trainer"""
    def __init__(self, lang='si'):
        self._lang = lang

    def train(self):
        """
        train model
        """
        pass