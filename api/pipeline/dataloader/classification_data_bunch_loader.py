from ..fastai1.text import *
from .data_bunch_loader import DataBunchLoader


class ClassificationDataBunchLoader(DataBunchLoader):
    def __init__(self, df_train_set, df_val_set, text_col_name, label_col_name, vocab):
        self.__df_train_set = df_train_set
        self.__df_val_set = df_val_set
        self.__text_col_name = text_col_name
        self.__label_col_name = label_col_name
        # self.__bs = bs
        # self.__is_backward = is_backward
        self.__vocab = vocab
        # self.__lang = lang
        super().__init__(self)

    def load(self):
        item_counts = self.__df_train_set[self.__label_col_name].value_counts()
        print(item_counts)
        self.__df_train_set[self.__label_col_name].value_counts().plot.bar(rot=30)

        data = TextClasDataBunch.from_df('.', train_df=self.__df_train_set, valid_df=self.__df_val_set, vocab=self.__vocab,
                                         bs=32, text_cols=self.__text_col_name, label_cols=self.__label_col_name,
                                         backwards=self.__is_backward)

        if self.__is_backward:
            data.save(f'{self.__lang}_data_class_bwd.pkl')
            # data = load_data('./', f'{self.lang}_data_class_bwd.pkl')
        else:
            data.save(f'{self.__lang}_data_class_fwd.pkl')
            # data = load_data('./', f'{self.lang}_data_class_fwd.pkl', bs=64)

        return data