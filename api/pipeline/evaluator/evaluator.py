import uuid

from ...utils.logger import Logger
from ...utils.image_storage import ImageStorage
from ..fastai1.basics import *
from sklearn.metrics import classification_report, matthews_corrcoef
from sklearn.metrics import roc_curve, auc


class Evaluator():
    """Provide evaluation metrics"""

    def __init__(self):
        pass

    def evaluate(self, learn):
        """
        Evaluate the ensemble model
        :rtype: dict
        """
        logger = Logger()
        ensemble_predictions, y_values, losses = learn.get_preds(with_loss=True)

        ensemble_accuracy = accuracy(ensemble_predictions, y_values)
        logger.info('Ensemble accuracy of AdaptText is {0} %.'.format(ensemble_accuracy))

        ensemble_error = error_rate(ensemble_predictions, y_values)
        logger.info('Error rate of AdaptText is {0} %.'.format(ensemble_error))

        # ROC_Curve Computation
        probabilities = np.exp(ensemble_predictions[:, 1])
        false_positive_rate, true_positive_rate, threshold_vals = roc_curve(y_values, probabilities, pos_label=1)

        # Compute ROC area
        roc_area = auc(false_positive_rate, true_positive_rate)
        logger.info('ROC_Area of AdaptText is {0}'.format(roc_area))

        xlim = [-0.01, 1.0]
        ylim = [0.0, 1.01]

        roc_curve_fig = self.draw_roc_curve(xlim, ylim, false_positive_rate, true_positive_rate, roc_area)
        roc_curve_fig_path = 'roc_curve_' + str(uuid.uuid4()) + '.png'
        roc_curve_fig.savefig(roc_curve_fig_path)

        interp = ClassificationInterpretation(learn, ensemble_predictions, y_values, losses)
        conf_matrix_fig = interp.plot_confusion_matrix(return_fig=True)

        conf_matrix_fig_path = 'conf_matrix_' + str(uuid.uuid4()) + '.png'
        conf_matrix_fig.savefig(conf_matrix_fig_path)

        img_utils = ImageStorage()
        conf_matrix_fig_url = img_utils.upload(conf_matrix_fig_path)
        roc_curve_fig_url = img_utils.upload(roc_curve_fig_path)

        pred_val = learn.get_preds(DatasetType.Valid)
        pred_val_l = pred_val[0].argmax(1)

        class_report = classification_report(pred_val[1], pred_val_l, output_dict=True)
        matthews_corr_coef = matthews_corrcoef(pred_val[1], pred_val_l)

        macro_f1 = class_report['macro avg']['f1-score']
        macro_precision = class_report['macro avg']['precision']
        macro_recall = class_report['macro avg']['recall']
        macro_support = class_report['macro avg']['support']

        weighted_f1 = class_report['weighted avg']['f1-score']
        weighted_precision = class_report['weighted avg']['precision']
        weighted_recall = class_report['weighted avg']['recall']
        weighted_support = class_report['weighted avg']['support']

        logger.info('Evaluation completed')

        metrics_dict = {'acc': ensemble_accuracy.item(), 'err': ensemble_error.item(), 'xlim': xlim, 'ylim': ylim, 'fpr': false_positive_rate.tolist(),
                        'tpr': true_positive_rate.tolist(), 'roc_auc': roc_area.item(),
                        'macro_f1': macro_f1, 'macro_precision': macro_precision, 'macro_recall': macro_recall,
                        'macro_support': macro_support, 'weighted_f1': weighted_f1,
                        'weighted_precision': weighted_precision, 'weighted_recall': weighted_recall,
                        'weighted_support': weighted_support, 'matthews_corr_coef': matthews_corr_coef,
                        'conf_matrix_fig_url': conf_matrix_fig_url, 'roc_curve_fig_url': roc_curve_fig_url}

        return metrics_dict

    def draw_roc_curve(self, xlim, ylim, false_positive_rate, true_positive_rate, roc_area):
        """
        Draw ROC Curve
        :param xlim: x axis limits
        :type xlim: list
        :param ylim: y axis limits
        :type ylim: list
        :param false_positive_rate: false positive rate
        :type false_positive_rate: float
        :param true_positive_rate: true positive rate
        :type true_positive_rate: float
        :param roc_area: Area_Under_the_Curve
        :type roc_area: float
        :return: figure
        :rtype: object
        """
        fig = plt.figure()

        # Add Graph Details
        plt.plot(false_positive_rate, true_positive_rate, color='darkorange', label='Ensemble Classifier : ROC curve (area = %0.2f)' % roc_area)
        plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
        plt.xlim(xlim)
        plt.ylim(ylim)
        # Add X and Y axes
        plt.xlabel('False Positive(FP) Rate')
        plt.ylabel('True Positive(TP) Rate')
        # Add Graph title
        plt.title('Receiver Operating Characteristic')
        # Add Graph legend
        plt.legend(loc="lower right")

        return fig

    def get_accuracy(self, learn):
        """
        Get model accuracy
        :param learn: model
        :type learn: object
        :return: accuracy
        :rtype: float
        """
        logger = Logger()
        model_predictions, y_vals, losses = learn.get_preds(with_loss=True)

        model_accuracy = accuracy(model_predictions, y_vals)
        logger.info('Accuracy of AdaptText is {0} %.'.format(model_accuracy))

        return model_accuracy
