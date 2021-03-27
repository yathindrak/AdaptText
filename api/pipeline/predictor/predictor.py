import pandas as pd
import numpy as np

class Predictor:
    def __init__(self, learn_clas_fwd, learn_clas_bwd, learn, classes):
        self.learn_classifier_fwd = learn_clas_fwd
        self.learn_classifier_bwd = learn_clas_bwd
        self.learn = learn
        self.classes = classes

    def predict(self, input_text):
        f_prediction = self.learn_classifier_fwd.predict(input_text)[2].numpy()
        b_prediction = self.learn_classifier_bwd.predict(input_text)[2].numpy()

        pred_fwd = pd.DataFrame([f_prediction], columns=list(self.classes)).add_prefix('fwd_')
        pred_bwd = pd.DataFrame([b_prediction], columns=list(self.classes)).add_prefix('bwd_')

        pred = (pred_fwd.join(pred_bwd))

        return str(self.learn.predict(np.squeeze(pred))[0])
