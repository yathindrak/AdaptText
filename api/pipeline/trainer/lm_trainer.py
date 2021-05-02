from ..fastai1.text import *
from ..fastai1.basics import *
from ..fastai1.callbacks import SaveModelCallback, ReduceLROnPlateauCallback
from ..hyperparameter.tuner import HyperParameterTuner
from .trainer import Trainer
from ..optimizer.DiffGradOptimizer import DiffGrad


class LMTrainer(Trainer):
    """Trainer for LM"""
    def __init__(self, data, lm_fns, mdl_path, is_backward=False, drop_mult=0.9, is_gpu=True, *args, **kwargs):
        super(LMTrainer, self).__init__(*args, **kwargs)
        self.__data = data
        self.__lm_fns = lm_fns
        self.__mdl_path = mdl_path
        self.__is_backward = is_backward
        self.__drop_mult = drop_mult
        self.__is_gpu = is_gpu

    def retrieve_lm(self, pretrained_paths: OptStrTuple = None) -> 'LanguageLearner':
        """
        Setup and Retrieve Language model
        :rtype: object
        """
        databunch = self.__data
        dropout_probs = dict(input=0.25, output=0.1, hidden=0.15, embedding=0.02, weight=0.2)
        size_of_embedding = 400
        num_of_hidden_neurons = 1550
        num_of_layers = 4

        config = dict(emb_sz=size_of_embedding, n_hid=num_of_hidden_neurons, n_layers=num_of_layers,
                      input_p=dropout_probs['input'], output_p=dropout_probs['output'],
                      hidden_p=dropout_probs['hidden'], embed_p=dropout_probs['embedding'],
                      weight_p=dropout_probs['weight'], pad_token=1, qrnn=False, out_bias=True)

        metrics = [error_rate, accuracy, Perplexity()]
        embedding_size = config['emb_sz']
        split_function = awd_lstm_lm_split
        for dropout_key in config.keys():
            if dropout_key.endswith('_p'): config[dropout_key] *= self.__drop_mult
        output_dropout_p, output_bias = map(config.pop, ['output_p', 'out_bias'])
        # Get list of words(itos) in vocab
        vocab_size = len(databunch.vocab.itos)
        lstm_encoder = AWD_LSTM(vocab_size, **config)
        enc_embedding = lstm_encoder.encoder
        lstm_decoder = LinearDecoder(vocab_size, embedding_size, output_dropout_p, tie_encoder=enc_embedding,
                                     bias=output_bias)
        model = SequentialRNN(lstm_encoder, lstm_decoder)
        learn = LanguageLearner(databunch, model, split_function, metrics=metrics)

        if pretrained_paths is not None:
            print(pretrained_paths)
            data_path = learn.path
            model_path = learn.model_dir

            func_names = [data_path / model_path / f'{func_name}.{extension}' for func_name, extension in
                          zip(pretrained_paths, ['pth', 'pkl'])]

            learn = learn.load_pretrained(*func_names)
            learn.freeze()

        return learn

    def train(self):
        """
        Train the Language model
        :rtype: object
        """
        lm_fn_1_fwd = self.__mdl_path / f'{self._lang}_wt.pth'
        lm_fn_1_bwd = self.__mdl_path / f'{self._lang}_wt_bwd.pth'

        if ((not self.__is_backward and lm_fn_1_fwd.exists()) or (self.__is_backward and lm_fn_1_bwd.exists())):
            if self.__is_gpu:
                learn = self.retrieve_lm(pretrained_paths=self.__lm_fns).to_fp16()
            else:
                learn = self.retrieve_lm(pretrained_paths=self.__lm_fns)
        else:
            if self.__is_gpu:
                learn = self.retrieve_lm().to_fp16()
            else:
                learn = self.retrieve_lm()

        # DiffGrad Optimization
        optar = partial(DiffGrad, betas=(.91, .999), eps=1e-7)
        learn.opt_func = optar

        # Find LR
        tuner = HyperParameterTuner(learn)
        lr = tuner.find_optimized_lr()

        learn.fit_one_cycle(2, lr, moms=(0.8, 0.7),
                            callbacks=[SaveModelCallback(learn), ReduceLROnPlateauCallback(learn)])
        # Completely unfreezing
        learn.unfreeze()
        learn.fit_one_cycle(8, lr, moms=(0.8, 0.7),
                            callbacks=[SaveModelCallback(learn), ReduceLROnPlateauCallback(learn)])

        learn.predict("මේ අතර", n_words=30)

        # Save checkpoints
        if self.__is_backward:
            learn.save(f'{self._lang}fine_tuned_bwd')
            learn.save_encoder(f'{self._lang}fine_tuned_enc_bwd')
        else:
            learn.save(f'{self._lang}fine_tuned')
            learn.save_encoder(f'{self._lang}fine_tuned_enc')