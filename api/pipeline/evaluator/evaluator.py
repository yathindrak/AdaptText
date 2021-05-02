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
        preds, y, losses = learn.get_preds(with_loss=True)

        acc = accuracy(preds, y)
        logger.info('The accuracy is {0} %.'.format(acc))

        err = error_rate(preds, y)
        logger.info('The error rate is {0} %.'.format(err))

        # probs from log preds
        probs = np.exp(preds[:, 1])
        # Compute ROC curve
        fpr, tpr, thresholds = roc_curve(y, probs, pos_label=1)

        # Compute ROC area
        roc_auc = auc(fpr, tpr)
        logger.info('ROC area is {0}'.format(roc_auc))

        xlim = [-0.01, 1.0]
        ylim = [0.0, 1.01]

        roc_curve_fig = self.draw_roc_curve(xlim, ylim, fpr, tpr, roc_auc)
        roc_curve_fig_path = 'roc_curve_' + str(uuid.uuid4()) + '.png'
        roc_curve_fig.savefig(roc_curve_fig_path)

        interp = ClassificationInterpretation(learn, preds, y, losses)
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

        metrics_dict = {'acc': acc.item(), 'err': err.item(), 'xlim': xlim, 'ylim': ylim, 'fpr': fpr.tolist(),
                        'tpr': tpr.tolist(), 'roc_auc': roc_auc.item(),
                        'macro_f1': macro_f1, 'macro_precision': macro_precision, 'macro_recall': macro_recall,
                        'macro_support': macro_support, 'weighted_f1': weighted_f1,
                        'weighted_precision': weighted_precision, 'weighted_recall': weighted_recall,
                        'weighted_support': weighted_support, 'matthews_corr_coef': matthews_corr_coef,
                        'conf_matrix_fig_url': conf_matrix_fig_url, 'roc_curve_fig_url': roc_curve_fig_url}

        return metrics_dict

    def draw_roc_curve(self, xlim, ylim, fpr, tpr, roc_auc):
        """
        Draw ROC Curve
        :param xlim: x axis limits
        :type xlim: list
        :param ylim: y axis limits
        :type ylim: list
        :param fpr: false positive rate
        :type fpr: float
        :param tpr: true positive rate
        :type tpr: float
        :param roc_auc: Area under the curve
        :type roc_auc: float
        :return: figure
        :rtype: object
        """
        fig = plt.figure()
        plt.plot(fpr, tpr, color='darkorange', label='Ensemble Classifier : ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.xlabel('False Positive(FP) Rate')
        plt.ylabel('True Positive(TP) Rate')
        plt.title('Receiver operating characteristic')
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
        preds, y, losses = learn.get_preds(with_loss=True)

        acc = accuracy(preds, y)
        logger.info('The accuracy is {0} %.'.format(acc))

        return acc
