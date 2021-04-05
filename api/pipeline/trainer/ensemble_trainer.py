from ..fastai1.basics import *
from ..fastai1.callbacks import SaveModelCallback, ReduceLROnPlateauCallback, OverSamplingCallback
from ..hyperparameter.tuner import HyperParameterTuner
from .trainer import Trainer
from ..optimizer.DiffGradOptimizer import DiffGrad
from ..fastai1.tabular import *


class EnsembleTrainer(Trainer):
    def __init__(self, learn_clas_fwd, learn_clas_bwd, classifiers_store_path, task_id, *args, **kwargs):
        super(EnsembleTrainer, self).__init__(*args, **kwargs)
        self.__learn_clas_fwd = learn_clas_fwd
        self.__learn_clas_bwd = learn_clas_bwd
        self.__classifiers_store_path = classifiers_store_path
        self.__task_id = task_id
        # self.drop_mult = drop_mult
        # self.lang = lang
        # super().__init__(self)

    def retrieve_classifier(self):
        metrics = [error_rate, accuracy]
        pred_tensors_fwd, pred_tensors_target_fwd = self.__learn_clas_fwd.get_preds(DatasetType.Valid, ordered=True)
        pred_tensors_bwd, pred_tensors_target_bwd = self.__learn_clas_bwd.get_preds(DatasetType.Valid, ordered=True)

        preds_fwd = pd.DataFrame(pred_tensors_fwd.numpy()).add_prefix('fwd_')
        preds_textm_bwd = pd.DataFrame(pred_tensors_bwd.numpy()).add_prefix('bwd_')
        preds_target_fwd = pd.DataFrame(pred_tensors_target_fwd.numpy())

        ensemble_df = (preds_fwd
                       .join(preds_textm_bwd)
                       .join(preds_target_fwd).rename(columns={0: "target"})
                       )

        column_names = ensemble_df.columns.values.tolist()
        column_names.pop()

        tabular_processes = [FillMissing, Categorify, Normalize]

        data_ensemble = (TabularList
                         .from_df(ensemble_df, cat_names=[], cont_names=column_names, procs=tabular_processes)
                         .split_by_rand_pct(valid_pct=0.1, seed=42)
                         .label_from_df(cols="target")
                         .databunch())

        learn = tabular_learner(data_ensemble, layers=[200, 100], metrics=metrics)

        return learn

    def train(self):
        learn = self.retrieve_classifier(metrics=[error_rate, accuracy])

        optar = partial(DiffGrad, betas=(.91, .999), eps=1e-7)
        learn.opt_func = optar

        # Find LR
        tuner = HyperParameterTuner(learn)
        lr = tuner.find_optimized_lr()

        learn.fit_one_cycle(8, lr, callbacks=[SaveModelCallback(learn),
                                              ReduceLROnPlateauCallback(learn, factor=0.8)])

        pkl_name = self.__classifiers_store_path[2] + self.__task_id + ".pkl"
        learn.export(pkl_name)

        return learn
