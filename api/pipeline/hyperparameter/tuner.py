from ..fastai1.basics import *


class HyperParameterTuner:
    def __init__(self, learn: Learner):
        self.learn = learn

    def find_optimized_lr(self):
        self.learn.lr_find()
        self.learn.recorder.plot(suggestion=True)
        lr = self.learn.recorder.min_grad_lr
        return lr
