from ..fastai1.basics import *
from ..fastai1.callbacks import SaveModelCallback, ReduceLROnPlateauCallback, OverSamplingCallback
from ..hyperparameter.tuner import HyperParameterTuner
from .trainer import Trainer
from ..optimizer.DiffGradOptimizer import DiffGrad
from ..fastai1.tabular import *


class EnsembleTrainer(Trainer):
    """Trainer for Ensemble Classification Model"""
    def __init__(self, learn_clas_fwd, learn_clas_bwd, classes, classifiers_store_path, task_id, *args, **kwargs):
        super(EnsembleTrainer, self).__init__(*args, **kwargs)
        self.__learn_clas_fwd = learn_clas_fwd
        self.__learn_clas_bwd = learn_clas_bwd
        self.__classifiers_store_path = classifiers_store_path
        self.__task_id = task_id
        self.__classes = classes

    def retrieve_classifier(self):
        """
        Setup and Retrieve Ensemble Classification model
        :rtype: object
        """
        metrics = [error_rate, accuracy]
        prediction_tensors_fwd, prediction_tensors_target_fwd = self.__learn_clas_fwd.get_preds(DatasetType.Valid, ordered=True)
        prediction_tensors_bwd, prediction_tensors_target_bwd = self.__learn_clas_bwd.get_preds(DatasetType.Valid, ordered=True)

        fwd_df = pd.DataFrame(prediction_tensors_fwd.numpy())
        for idx in range(len(self.__classes)):
            fwd_df.rename(columns={idx: self.__classes[idx]}, inplace=True)

        bwd_df = pd.DataFrame(prediction_tensors_bwd.numpy())
        for idx in range(len(self.__classes)):
            bwd_df.rename(columns={idx: self.__classes[idx]}, inplace=True)

        preds_fwd = fwd_df.add_prefix('fwd_')
        preds_textm_bwd = bwd_df.add_prefix('bwd_')
        preds_actual_target_fwd = pd.DataFrame(prediction_tensors_target_fwd.numpy())

        ensemble_dataframe = (preds_fwd
                       .join(preds_textm_bwd)
                       .join(preds_actual_target_fwd).rename(columns={0: "target"})
                       )

        ensemble_dataframe["target"].replace(list(range(0, len(self.__classes))), self.__classes, inplace=True)

        column_names = ensemble_dataframe.columns.values.tolist()
        column_names.pop()

        tabular_processes = [Categorify, Normalize, FillMissing]

        embedding_layer_dropout_prob = 0.04
        layer_set = [1000, 500]
        dropout_probs = [0.001, 0.01]

        valid_percentage = 0.1

        ensemble_databunch = (TabularList
                         .from_df(ensemble_dataframe, cat_names=[], cont_names=column_names, procs=tabular_processes)
                         .split_by_rand_pct(valid_pct=valid_percentage, seed=42)
                         .label_from_df(cols="target")
                         .databunch())

        learn = tabular_learner(ensemble_databunch, layers=layer_set, ps=dropout_probs, metrics=metrics, emb_drop=embedding_layer_dropout_prob)

        return learn

    def train(self):
        """
        Train the Ensemble Classification model
        :rtype: object
        """
        learn = self.retrieve_classifier()

        # DiffGrad Optimization
        optar = partial(DiffGrad, betas=(.91, .999), eps=1e-7)
        learn.opt_func = optar

        # Find LR
        tuner = HyperParameterTuner(learn)
        lr = tuner.find_optimized_lr()

        learn.fit_one_cycle(8, lr, callbacks=[SaveModelCallback(learn),
                                              ReduceLROnPlateauCallback(learn)])

        learn.fit_one_cycle(8, lr / 2, callbacks=[SaveModelCallback(learn),
                                                  ReduceLROnPlateauCallback(learn)])

        learn.fit_one_cycle(8, lr / 2,
                            callbacks=[SaveModelCallback(learn, every='improvement', monitor='accuracy'),
                                       ReduceLROnPlateauCallback(learn)])

        # Save model
        pkl_name = self.__classifiers_store_path[2] + self.__task_id + ".pkl"
        learn.export(pkl_name)

        return learn
