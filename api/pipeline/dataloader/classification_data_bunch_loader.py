from ..fastai1.text import *
from .data_bunch_loader import DataBunchLoader


class ClassificationDataBunchLoader(DataBunchLoader):
    """Provide Databunch for Classification Model"""
    def __init__(self, df_train_set, df_val_set, text_col_name, label_col_name, vocab, is_backward=False, *args, **kwargs):
        super(ClassificationDataBunchLoader, self).__init__(*args, **kwargs)
        self.__df_train_set = df_train_set
        self.__df_val_set = df_val_set
        self.__text_col_name = text_col_name
        self.__label_col_name = label_col_name
        self.__is_backward = is_backward
        self.__vocab = vocab

    def load(self):
        """
        Returns databunch for Classification Model
        :rtype: object
        """
        self.__df_train_set[self.__label_col_name].value_counts().plot.bar(rot=30)

        data = TextClasDataBunch.from_df('.', train_df=self.__df_train_set, valid_df=self.__df_val_set, vocab=self.__vocab,
                                         bs=32, text_cols=self.__text_col_name, label_cols=self.__label_col_name,
                                         backwards=self.__is_backward)

        # Save checkpoints
        if self.__is_backward:
            data.save(f'{self._lang}_data_class_bwd.pkl')
        else:
            data.save(f'{self._lang}_data_class_fwd.pkl')

        return data