from ..fastai1.text import *
from ..fastai1.basics import *
from .base_data_bunch_loader import BaseDataBunchLoader


class BaseLMDataBunchLoader(BaseDataBunchLoader):
    def __init__(self, path, splitting_ratio, seed=42, bs=128, is_backward=False, lang='si'):
        self.path = path
        self.splitting_ratio = splitting_ratio
        self.seed = seed
        self.bs = bs
        self.is_backward = is_backward
        self.lang = lang

    def load(self):
        data = (TextList.from_folder(Path(self.path), processor=[OpenFileProcessor(), SPProcessor()])
                .split_by_rand_pct(self.splitting_ratio, seed=self.seed)
                .label_for_lm()
                .databunch(bs=self.bs, num_workers=1, backwards=self.is_backward))
        # Store data
        data.save(f'{self.lang}_databunch')
        print(len(data.vocab.itos), len(data.train_ds))
        # Load data
        # data = load_data(self.path, f'{self.lang}_databunch', bs=self.bs)
        return data
