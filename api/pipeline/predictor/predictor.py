class Predictor:
    def __init__(self, learn_clas_fwd, learn_clas_bwd, classes):
        self.learn_classifier_fwd = learn_clas_fwd
        self.learn_classifier_bwd = learn_clas_bwd
        self.classes = classes

    def predict(self, input_text):
        f_prediction = self.learn_classifier_fwd.predict(input_text)[2]
        b_prediction = self.learn_classifier_bwd.predict(input_text)[2]
        average_prediction = f_prediction + b_prediction

        max_value = average_prediction[0]
        max_index = 0

        for i, x in enumerate(average_prediction):
            if x > max_value:
                max_value = x
                max_index = i

        return self.classes[max_index], average_prediction
