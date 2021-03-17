from ..fastai1.text import *
from ..utils.dropbox_handler import DropboxHandler
from .base_data_bunch_loader import BaseDataBunchLoader


class LMDataBunchLoader(BaseDataBunchLoader):
    def __init__(self, df_train_set, df_val_set, text_col_name, label_col_name, splitting_ratio, app_root,
                 continuous_train=False, bs=128, is_backward=False, lang='si'):
        self.df_train_set = df_train_set
        self.df_val_set = df_val_set
        self.text_col_name = text_col_name
        self.label_col_name = label_col_name
        self.splitting_ratio = splitting_ratio
        self.continuous_train = continuous_train
        self.app_root = app_root
        self.bs = bs
        self.is_backward = is_backward
        self.lang = lang

    def load(self):
        if self.continuous_train:
            dropbox_handler = DropboxHandler(self.app_root)
            dropbox_handler.upload_text_file(self.df_train_set[self.text_col_name])

        tokenizer = Tokenizer(SpacyTokenizer, lang="xx")

        data = TextLMDataBunch.from_df('.', train_df=self.df_train_set, valid_df=self.df_val_set,
                                       text_cols=self.text_col_name, tokenizer=tokenizer, backwards=self.is_backward)

        if self.is_backward:
            data.save(f'{self.lang}_data_lm_bwd.pkl')
            # data = load_data('./', f'{lang}_data_lm_bwd.pkl')
        else:
            data.save(f'{self.lang}_data_lm_fwd.pkl')
            # data = load_data('./', f'{lang}_data_lm_fwd.pkl')
        return data
