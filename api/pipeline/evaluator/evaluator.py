import uuid

from ...utils.logger import Logger
from ...utils.image_storage import ImageStorage
from ..fastai1.text import TextClassificationInterpretation
from ..fastai1.basics import *
from sklearn.metrics import classification_report, matthews_corrcoef
from sklearn.metrics import roc_curve, auc

class Evaluator():
    def __init__(self):
        pass

    def evaluate_ensemble(self, learn):
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
        roc_curve_fig_path = 'roc_curve_'+str(uuid.uuid4())+'.png'
        roc_curve_fig.savefig(roc_curve_fig_path)

        # use learn_clas_fwd for the ensemble to get close confusion matrix for the actual
        # interpretation = ClassificationInterpretation(learn_clas_fwd, preds, y, losses)
        # conf_matrix = interpretation.confusion_matrix()

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

        metrics_dict = {'acc': acc.item(), 'err': err.item(), 'xlim': xlim, 'ylim': ylim, 'fpr': fpr.tolist(), 'tpr': tpr.tolist(), 'roc_auc': roc_auc.item(),
                        'macro_f1': macro_f1, 'macro_precision': macro_precision, 'macro_recall': macro_recall,
                        'macro_support': macro_support, 'weighted_f1': weighted_f1,
                        'weighted_precision': weighted_precision, 'weighted_recall': weighted_recall,
                        'weighted_support': weighted_support, 'matthews_corr_coef': matthews_corr_coef,
                        'conf_matrix_fig_url': conf_matrix_fig_url, 'roc_curve_fig_url': roc_curve_fig_url}

        return metrics_dict

    # def evaluate(self, learn):
    #     preds, y, losses = learn.get_preds(with_loss=True)
    #
    #     acc = accuracy(preds, y)
    #     print('The accuracy is {0} %.'.format(acc))
    #
    #     err = error_rate(preds, y)
    #     print('The error rate is {0} %.'.format(err))
    #
    #     interp = ClassificationInterpretation(learn, preds, y, losses, return_fig=True)
    #     interp.plot_confusion_matrix()
    #
    #     pred_val = learn.get_preds(DatasetType.Valid, ordered=True)
    #     pred_val_l = pred_val[0].argmax(1)
    #
    #     print(classification_report(pred_val[1], pred_val_l))
    #
    #     # probs from log preds
    #     probs = np.exp(preds[:, 1])
    #     # Compute ROC curve
    #     fpr, tpr, thresholds = roc_curve(y, probs, pos_label=1)
    #
    #     # Compute ROC area
    #     roc_auc = auc(fpr, tpr)
    #     print('ROC area is {0}'.format(roc_auc))
    #
    #     xlim = [-0.01, 1.0]
    #     ylim = [0.0, 1.01]
    #
    #     plt.figure()
    #     plt.plot(fpr, tpr, color='darkorange', label='ROC curve (area = %0.2f)' % roc_auc)
    #     plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    #     plt.xlim(xlim)
    #     plt.ylim(ylim)
    #     plt.xlabel('False Positive Rate')
    #     plt.ylabel('True Positive Rate')
    #     plt.title('Receiver operating characteristic')
    #     plt.legend(loc="lower right")
    #
    #     interp2 = TextClassificationInterpretation.from_learner(learn)
    #     interp2.show_top_losses(10)
    #
    #     # print(interp2.show_intrinsic_attention(
    #     #     "ඉඩකඩ සම්බන්ධයෙන් මතු වූ ගැටලුව මහර බන්ධනාගාරයේ කලහකාරී තත්ත්වයට එකහෙළා බලපෑ බව, සිද්ධිය පිළිබඳව විමර්ශනය කිරීම සඳහා අධිකරණ අමාත්‍යවරයා පත්කළ කමිටුවේ අතුරු වාර්තාව පෙන්වා දී තිබේ."))
    #
    #     torch.argmax(preds[0])

    def draw_roc_curve(self, xlim, ylim, fpr, tpr, roc_auc):
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
        logger = Logger()
        preds, y, losses = learn.get_preds(with_loss=True)

        acc = accuracy(preds, y)
        logger.info('The accuracy is {0} %.'.format(acc))

        return acc


