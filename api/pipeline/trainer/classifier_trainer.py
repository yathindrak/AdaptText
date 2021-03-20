from ..fastai1.text import *
from ..fastai1.basics import *
from ..fastai1.callbacks import SaveModelCallback, ReduceLROnPlateauCallback, OverSamplingCallback
from ..hyperparameter.tuner import HyperParameterTuner
from .trainer import Trainer
from ..optimizer.DiffGradOptimizer import DiffGrad
from ..evaluator.evaluator import Evaluator
import copy

class ClassifierTrainer(Trainer):
    def __init__(self, data, lm_fns, mdl_path, model_store_path, classifiers_store_path, task_id, is_backward=False, drop_mult=0.5, is_imbalanced=False, lang='si'):
        self.data = data
        self.lm_fns = lm_fns
        self.mdl_path = mdl_path
        self.model_store_path = model_store_path
        self.classifiers_store_path = classifiers_store_path
        self.task_id = task_id
        self.is_backward = is_backward
        self.drop_mult = drop_mult
        self.is_imbalanced = is_imbalanced
        self.lang = lang

    def retrieve_classifier(self, databunch: DataBunch, config: dict, drop_multi_val: float = 1.,
                            metrics=None) -> 'TextClassifierLearner':

        embedding_size = config['emb_sz']
        num_of_classes = databunch.c
        split_function = awd_lstm_clas_split
        back_propagation_through_time_val = 80
        max_input_sequence_length = 80 * 20
        padding_idx = 1
        vocab_size = len(databunch.vocab.itos)

        for dropout_key in config.keys():
            if dropout_key.endswith('_p'): config[dropout_key] *= drop_multi_val

        linear_features = [60]
        dropout_ps = [0.1] * len(linear_features)
        layers = [embedding_size * 3] + linear_features + [num_of_classes]
        dropout_ps = [config.pop('output_p')] + dropout_ps

        lstm_encoder = AWD_LSTM(vocab_size, **config)

        encoder = MultiBatchEncoder(back_propagation_through_time_val, max_input_sequence_length, lstm_encoder,
                                    pad_idx=padding_idx)
        model = SequentialRNN(encoder, PoolingLinearClassifier(layers, dropout_ps))

        learn = RNNLearner(databunch, model, split_func=split_function)

        return learn

    def train(self, grad_unfreeze=True):
        dropout_probs = dict(input=0.25, output=0.1, hidden=0.15, embedding=0.02, weight=0.2)
        size_of_embedding = 400
        num_of_hidden_neurons = 1550
        num_of_layers = 4

        config = dict(emb_sz=size_of_embedding, n_hid=num_of_hidden_neurons, n_layers=num_of_layers,
                      input_p=dropout_probs['input'], output_p=dropout_probs['output'],
                      hidden_p=dropout_probs['hidden'],
                      embed_p=dropout_probs['embedding'], weight_p=dropout_probs['weight'], pad_token=1, qrnn=False)

        learn = self.retrieve_classifier(self.data, config=config, drop_multi_val=self.drop_mult,
                                         metrics=[error_rate, accuracy])

        optar = partial(DiffGrad, betas=(.91, .999), eps=1e-7)
        learn.opt_func = optar

        if self.is_backward:
            learn.load_encoder(f'{self.lang}fine_tuned_enc_bwd')
        else:
            learn.load_encoder(f'{self.lang}fine_tuned_enc')
        learn.freeze()

        # Find LR
        tuner = HyperParameterTuner(learn)
        lr = tuner.find_optimized_lr()

        if self.is_imbalanced:
            learn.fit_one_cycle(12, lr, callbacks=[SaveModelCallback(learn), OverSamplingCallback(learn),
                                               ReduceLROnPlateauCallback(learn, factor=0.8)])
        else:
            learn.fit_one_cycle(12, lr, callbacks=[SaveModelCallback(learn),
                                                  ReduceLROnPlateauCallback(learn, factor=0.8)])

        # store model temporarily
        classifier_initial = copy.deepcopy(learn)

        evaluator = Evaluator()
        classifier_initial_accuracy = evaluator.get_accuracy(classifier_initial).item()

        print('Gradual Unfreezing..')

        if grad_unfreeze:
            if self.is_imbalanced:
                learn.freeze_to(-2)
                learn.fit_one_cycle(8, lr,
                                    callbacks=[SaveModelCallback(learn), OverSamplingCallback(learn),
                                               ReduceLROnPlateauCallback(learn, factor=0.8)])

                learn.freeze_to(-3)
                learn.fit_one_cycle(6, lr,
                                    callbacks=[SaveModelCallback(learn), OverSamplingCallback(learn),
                                               ReduceLROnPlateauCallback(learn, factor=0.8)])
            else:
                learn.freeze_to(-2)
                learn.fit_one_cycle(8, lr,
                                    callbacks=[SaveModelCallback(learn),
                                               ReduceLROnPlateauCallback(learn, factor=0.8)])

                learn.freeze_to(-3)
                learn.fit_one_cycle(6, lr,
                                    callbacks=[SaveModelCallback(learn),
                                               ReduceLROnPlateauCallback(learn, factor=0.8)])

        print('Completely Unfreezing..')

        learn.unfreeze()

        tuner = HyperParameterTuner(learn)
        lr = tuner.find_optimized_lr()

        if self.is_imbalanced:
            learn.fit_one_cycle(6, lr, callbacks=[SaveModelCallback(learn), OverSamplingCallback(learn),
                                                  ReduceLROnPlateauCallback(learn, factor=0.8)])
            learn.fit_one_cycle(6, lr / 2, callbacks=[SaveModelCallback(learn), OverSamplingCallback(learn),
                                                      ReduceLROnPlateauCallback(learn, factor=0.8)])
            learn.fit_one_cycle(8, lr,
                                callbacks=[SaveModelCallback(learn, every='improvement', monitor='accuracy'),
                                           OverSamplingCallback(learn),
                                           ReduceLROnPlateauCallback(learn, factor=0.8)])
        else:
            learn.fit_one_cycle(6, lr, callbacks=[SaveModelCallback(learn),
                                                  ReduceLROnPlateauCallback(learn, factor=0.8)])
            learn.fit_one_cycle(6, lr / 2, callbacks=[SaveModelCallback(learn),
                                                      ReduceLROnPlateauCallback(learn, factor=0.8)])
            learn.fit_one_cycle(8, lr,
                                callbacks=[SaveModelCallback(learn, every='improvement', monitor='accuracy'),
                                           ReduceLROnPlateauCallback(learn, factor=0.8)])

        print('Completely Unfreezing..')

        classifier_unfrozen_accuracy = evaluator.get_accuracy(learn).item()

        if classifier_unfrozen_accuracy < classifier_initial_accuracy:
            print('reverting back to initial model...')
            learn = classifier_initial
            print('The new accuracy is {0} %.'.format(classifier_initial_accuracy))

        if self.is_backward:
            # learn.save(f'{self.lang}_clas_bwd')
            pkl_name = self.classifiers_store_path[1] + self.task_id + ".pkl"
            learn.export(pkl_name)
        else:
            # learn.save(f'{self.lang}_clas')
            pkl_name = self.classifiers_store_path[0] + self.task_id + ".pkl"
            learn.export(pkl_name)

        return learn