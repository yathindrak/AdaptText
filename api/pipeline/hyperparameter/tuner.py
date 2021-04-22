from ..fastai1.basics import *


class HyperParameterTuner:
    """Hyper parameter tuner module"""
    def __init__(self, learn: Learner):
        self.__learn = learn

    def find_optimized_lr(self):
        """
        Find optimized Learning Rate
        :return: learning rate
        :rtype: float
        """
        self.__learn.lr_find()
        self.__learn.recorder.plot(suggestion=True)
        try:
            lr = self.__learn.recorder.min_grad_lr
        except:
            lr = None
        return lr
