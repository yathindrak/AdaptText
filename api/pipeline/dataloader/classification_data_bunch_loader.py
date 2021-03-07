from ..fastai1.text import *
from .base_data_bunch_loader import BaseDataBunchLoader


class ClassificationDataBunchLoader(BaseDataBunchLoader):
    def __init__(self, df_train_set, df_val_set, text_col_name, label_col_name, splitting_ratio, vocab, bs=128,
                 is_backward=False, lang='si'):
        self.df_train_set = df_train_set
        self.df_val_set = df_val_set
        self.text_col_name = text_col_name
        self.label_col_name = label_col_name
        self.splitting_ratio = splitting_ratio
        self.bs = bs
        self.is_backward = is_backward
        self.vocab = vocab
        self.lang = lang

    def load(self):
        item_counts = self.df_train_set[self.label_col_name].value_counts()
        print(item_counts)
        self.df_train_set[self.label_col_name].value_counts().plot.bar(rot=30)

        data = TextClasDataBunch.from_df('.', train_df=self.df_train_set, valid_df=self.df_val_set, vocab=self.vocab,
                                         bs=32, text_cols=self.text_col_name, label_cols=self.label_col_name,
                                         backwards=self.is_backward)

        if self.is_backward:
            data.save(f'{self.lang}_data_class_bwd.pkl')
            # data = load_data('./', f'{self.lang}_data_class_bwd.pkl')
        else:
            data.save(f'{self.lang}_data_class_fwd.pkl')
            # data = load_data('./', f'{self.lang}_data_class_fwd.pkl', bs=64)

        return data