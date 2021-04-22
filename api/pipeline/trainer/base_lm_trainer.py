from ..fastai1.text import *
from ..fastai1.basics import *
from ..fastai1.callbacks import SaveModelCallback, ReduceLROnPlateauCallback
from .trainer import Trainer
from ..hyperparameter.tuner import HyperParameterTuner
from ..optimizer.DiffGradOptimizer import DiffGrad


class BaseLMTrainer(Trainer):
    """Trainer for Base LM"""
    def __init__(self, data, lm_fns, mdl_path, model_store_path, is_gpu=True, drop_mult=0.9, *args, **kwargs):
        super(BaseLMTrainer, self).__init__(*args, **kwargs)
        self.__data = data
        self.__lm_fns = lm_fns
        self.__mdl_path = mdl_path
        self.__model_store_path = model_store_path
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

        metrics = [accuracy]

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
            # print(pretrained_file_paths)
            data_path = learn.path
            model_path = learn.model_dir

            func_names = [data_path / model_path / f'{func_name}.{extension}' for func_name, extension in
                          zip(pretrained_paths, ['pth', 'pkl'])]

            learn = learn.load_pretrained(*func_names)
            learn.freeze()

        return learn

    def train(self):
        """
        Train the language model
        :rtype: object
        """
        if self.__is_gpu:
            learn = self.retrieve_lm().to_fp16()
        else:
            learn = self.retrieve_lm()

        optar = partial(DiffGrad, betas=(.91, .999), eps=1e-7)
        learn.opt_func = optar

        # Find LR
        tuner = HyperParameterTuner(learn)
        lr = tuner.find_optimized_lr()

        gc.collect()

        learn.unfreeze()
        learn.fit_one_cycle(10, lr, moms=(0.8, 0.7),
                            callbacks=[SaveModelCallback(learn), ReduceLROnPlateauCallback(learn, factor=0.8)])

        learn.to_fp32().save(self.__mdl_path / self.__lm_fns[0], with_opt=False)

        learn.data.vocab.save(self.__model_store_path)