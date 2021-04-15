import zipfile

from sklearn.model_selection import train_test_split

from .trainer.ensemble_trainer import EnsembleTrainer
from ..utils.logger import Logger
from ..connection.initializers import database
from ..models.task import Task
from ..websocket.pusher_publisher import PusherPublisher
from .utils.dropbox_handler import DropboxHandler
from .fastai1.basics import *
from .dataloader.base_lm_data_bunch_loader import BaseLMDataBunchLoader
from .dataloader.classification_data_bunch_loader import ClassificationDataBunchLoader
from .dataloader.lm_data_bunch_loader import LMDataBunchLoader
from .preprocessor.preprocessor import PreProcessor
from .trainer.base_lm_trainer import BaseLMTrainer
from .trainer.classifier_trainer import ClassifierTrainer
from .trainer.lm_trainer import LMTrainer
from .utils.wiki_handler import WikiHandler


class AdaptText:
    def __init__(self, lang, data_root, bs=128, splitting_ratio=0.1, continuous_train=True):
        self.__lang = lang
        self.__data_root = data_root
        self.__bs = bs
        self.__splitting_ratio = splitting_ratio
        self.__data_path = Path(data_root + '/data')
        self.__lang = 'si'
        self.__name = f'{lang}wiki'
        self.__path = self.__data_path / self.__name
        self.__base_lm_data_path = self.__path / 'articles'
        self.__mdl_path = self.__path / 'models'
        self.__lm_fns = [self.__mdl_path / f'{lang}_wt', self.__mdl_path / f'{lang}_wt_vocab']
        self.__lm_fns_bwd = [self.__mdl_path / f'{lang}_wt_bwd', self.__mdl_path / f'{lang}_wt_vocab_bwd']
        self.__lm_store_path = [f'{data_root}/data/{lang}wiki/models/si_wt_vocab.pkl',
                              f'{data_root}/data/{lang}wiki/models/si_wt.pth',
                              f'{data_root}/data/{lang}wiki/models/si_wt_vocab_bwd.pkl',
                              f'{data_root}/data/{lang}wiki/models/si_wt_bwd.pth']
        self.__lm_store_files = ['si_wt_vocab.pkl', 'si_wt.pth', 'si_wt_vocab_bwd.pkl', 'si_wt_bwd.pth']
        self.__classifiers_store_path = ["models/fwd-export", "models/bwd-export", "models/ensemble-export"]
        self.__continuous_train = continuous_train

        if not torch.cuda.is_available():
            self.is_gpu = False
            warnings.warn(
                'Note that CUDA support is not available for your instance, Hence training will be continued on CPU')
        else:
            self.is_gpu = True

    def setup_wiki_data(self):
        logger = Logger()
        # making required directories
        self.__path.mkdir(exist_ok=True, parents=True)
        self.__mdl_path.mkdir(exist_ok=True)

        wikihandler = WikiHandler(self.__lang)

        # Getting wiki articles
        wikihandler.retrieve_articles(self.__path)
        logger.info('Retrieved wiki articles')

        # Prepare articles
        base_lm_data_path = wikihandler.prepare_articles(self.__path)
        logger.info('Completed preparing wiki articles')
        return base_lm_data_path

    def add_external_text(self, txt_filename, filepath, url):
        headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
        r = requests.get(url, stream=True, headers=headers)
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(self.__data_root)

        shutil.move(self.__data_root + "/" + txt_filename, str(self.__base_lm_data_path / txt_filename))

    def prepare_base_lm_corpus(self):
        self.setup_wiki_data()
        # txt_filename = "test-s.txt"
        # filepath = Path(self.data_root + "/test-s.zip")
        # url = "https://www.dropbox.com/s/cnd985vl1bof50y/test-s.zip?dl=0"

        txt_filename = "half-si-dedup.txt"
        filepath = Path(self.__data_root + "/half-si-dedup.zip")
        url = "https://www.dropbox.com/s/alh6jf4rqxhhzow/half-si-dedup.zip?dl=0"

        self.add_external_text(txt_filename, filepath, url)

        dropbox_handler = DropboxHandler(self.__data_root)
        dropbox_handler.download_articles()

    def prepare_pretrained_lm(self, model_file_name):
        # models-test-s-10-epochs-with-cls.zip
        if (Path(f'{os.getcwd()}{self.__data_root}').exists()):
            shutil.rmtree(f'{os.getcwd()}{self.__data_root}')
        dropbox_handler = DropboxHandler(self.__data_root)
        dropbox_handler.download_pretrained_model(model_file_name)

        current_working_dir = os.getcwd()
        with zipfile.ZipFile(model_file_name, 'r') as archive:
            archive.extractall(current_working_dir)

        if os.path.exists(self.__mdl_path):
            shutil.rmtree(str(self.__mdl_path))
            os.mkdir(str(self.__mdl_path))
            os.mkdir(str(self.__base_lm_data_path))
        else:
            os.mkdir(str(self.__data_path))
            os.mkdir(str(self.__path))
            os.mkdir(str(self.__mdl_path))
            os.mkdir(str(self.__base_lm_data_path))

        for source in self.__lm_store_files:
            source = f'{os.getcwd()}{self.__data_root}/data/{self.__lang}wiki/models/{source}'
            shutil.move(source, self.__mdl_path)

    def build_base_lm(self):
        # if (not Path(self.base_lm_data_path).exists()):
        #     print("Base LM corpus not found, preparing the corpus...")
        self.prepare_base_lm_corpus()
        logger = Logger()

        web_socket = PusherPublisher()
        web_socket.publish_lm_progress(20)

        baseLMDataBunchLoader = BaseLMDataBunchLoader(self.__base_lm_data_path, self.__splitting_ratio)
        data_lm_fwd = baseLMDataBunchLoader.load()

        baseLMDataBunchLoader = BaseLMDataBunchLoader(self.__base_lm_data_path, self.__splitting_ratio,
                                                      is_backward=True)
        data_lm_bwd = baseLMDataBunchLoader.load()

        model_store_path = self.__mdl_path / Path(f'{self.__lang}_wt_vocab.pkl')
        model_store_path_bwd = self.__mdl_path / Path(f'{self.__lang}_wt_vocab_bwd.pkl')

        web_socket.publish_lm_progress(40)
        logger.info('Loaded BaseLM data...')

        # forward
        lmTrainer_fwd = BaseLMTrainer(data_lm_fwd, self.__lm_fns, self.__mdl_path, model_store_path, is_gpu=self.is_gpu)
        lmTrainer_fwd.train()

        web_socket.publish_lm_progress(70)
        logger.info('Trained forward BaseLM...')

        # backward
        lmTrainer_bwd = BaseLMTrainer(data_lm_bwd, self.__lm_fns_bwd, self.__mdl_path, model_store_path_bwd,
                                      is_gpu=self.is_gpu)
        lmTrainer_bwd.train()

        web_socket.publish_lm_progress(90)
        logger.info('Trained backward BaseLM...')

    def update_progress(self, task_id, progress):
        database.session.query(Task).filter_by(id=task_id).update({"progress": progress})
        database.session.commit()

    def build_classifier(self, df, text_name, label_name, task_id, grad_unfreeze: bool = True):
        logger = Logger()
        if (not Path(self.__mdl_path).exists()):
            logger.info('Pretrained LM not found, preparing...')

            # below the classifier hardcode wont be there for library
            # self.prepare_pretrained_lm("one-outta-three.zip")
            self.prepare_pretrained_lm("half_si_dedup.zip")

        df = df[[text_name, label_name]]
        func_names = [f'{func_name}.{extension}' for func_name, extension in zip(self.__lm_fns, ['pth', 'pkl'])]

        if not Path(func_names[0]).exists():
            return

        # custom_model_store_path = self.mdl_path / Path(f'{self.lang}_lm_wt_vocab.pkl')
        # custom_model_store_path_bwd = self.mdl_path / Path(f'{self.lang}_lm_wt_vocab_bwd.pkl')

        preprocessor = PreProcessor(df, text_name)
        preprocessor.preprocess_text()

        logger.info('Done preprocessing...')

        # item_counts = df[label_name].value_counts()

        df[label_name].value_counts().plot.bar(rot=30)

        df_trn, df_val = train_test_split(df, stratify=df[label_name], test_size=0.1, random_state=42)

        web_socket = PusherPublisher()
        web_socket.publish_classifier_progress(task_id, 3)
        self.update_progress(task_id, 3)

        # forward training
        lmDataBunchLoader = LMDataBunchLoader(df_trn, df_val, text_name, label_name,
                                              self.__data_root, continuous_train=self.__continuous_train)

        data_lm = lmDataBunchLoader.load()

        web_socket = PusherPublisher()
        web_socket.publish_classifier_progress(task_id, 7)
        self.update_progress(task_id, 7)

        lmDataBunchLoaderBwd = LMDataBunchLoader(df_trn, df_val, text_name, label_name,
                                                 self.__data_root, continuous_train=self.__continuous_train,
                                                 is_backward=True)
        data_lm_bwd = lmDataBunchLoaderBwd.load()

        web_socket = PusherPublisher()
        web_socket.publish_classifier_progress(task_id, 9)
        self.update_progress(task_id, 9)

        vocab = data_lm.train_ds.vocab

        classificationDataBunchLoader = ClassificationDataBunchLoader(df_trn, df_val, text_name, label_name, vocab)
        data_class = classificationDataBunchLoader.load()

        # data_class.show_batch()

        web_socket = PusherPublisher()
        web_socket.publish_classifier_progress(task_id, 11)
        self.update_progress(task_id, 11)

        classificationDataBunchLoaderBwd = ClassificationDataBunchLoader(df_trn, df_val, text_name, label_name,
                                                                         vocab, is_backward=True)
        data_class_bwd = classificationDataBunchLoaderBwd.load()

        # data_class_bwd.show_batch()

        classes = data_class.classes

        web_socket = PusherPublisher()
        web_socket.publish_classifier_progress(task_id, 13)
        self.update_progress(task_id, 13)

        logger.info('Loaded data for training...')

        lmTrainerFwd = LMTrainer(data_lm, self.__lm_fns, self.__mdl_path, False,
                                 is_gpu=self.is_gpu)
        languageModelFWD = lmTrainerFwd.train()

        web_socket = PusherPublisher()
        web_socket.publish_classifier_progress(task_id, 38)
        self.update_progress(task_id, 38)

        classifierTrainerFwd = ClassifierTrainer(data_class, self.__classifiers_store_path, task_id, False)
        classifierModelFWD = classifierTrainerFwd.train(grad_unfreeze)

        lmTrainerBwd = LMTrainer(data_lm_bwd, self.__lm_fns_bwd, self.__mdl_path, True,
                                 is_gpu=self.is_gpu)
        languageModelBWD = lmTrainerBwd.train()

        web_socket = PusherPublisher()
        web_socket.publish_classifier_progress(task_id, 63)
        self.update_progress(task_id, 63)

        classifierTrainerBwd = ClassifierTrainer(data_class_bwd, self.__classifiers_store_path, task_id, True)
        classifierModelBWD = classifierTrainerBwd.train(grad_unfreeze)

        web_socket = PusherPublisher()
        web_socket.publish_classifier_progress(task_id, 70)
        self.update_progress(task_id, 70)

        ensembleTrainer = EnsembleTrainer(classifierModelFWD, classifierModelBWD, classes, self.__classifiers_store_path, task_id)
        ensembleModel = ensembleTrainer.train()

        web_socket = PusherPublisher()
        web_socket.publish_classifier_progress(task_id, 75)
        self.update_progress(task_id, 75)

        classifier_zip_file_name = "classifier_" + task_id + ".zip"
        dropbox_classifier_zip_path = f'/adapttext/models/{classifier_zip_file_name}'

        zip_archive = zipfile.ZipFile(classifier_zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        for item in self.__classifiers_store_path:
            pkl_name = item + task_id + ".pkl"
            zip_archive.write(pkl_name)
        zip_archive.close()

        dropbox_handler = DropboxHandler(self.__data_root)
        dropbox_handler.upload_zip_file(classifier_zip_file_name, dropbox_classifier_zip_path)

        database.session.query(Task).filter_by(id=task_id).update({"model_path": dropbox_classifier_zip_path})
        database.session.commit()

        logger.info('Completed Training...')

        web_socket.publish_classifier_progress(task_id, 80)
        self.update_progress(task_id, 80)

        return classifierModelFWD, classifierModelBWD, ensembleModel, classes

    def store_lm(self, zip_file_name):
        # zip_file_name = "test.zip"
        zip_archive = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        for item in self.__lm_store_path:
            zip_archive.write(item)
        zip_archive.close()

        dropbox_handler = DropboxHandler(self.__data_root)
        dropbox_handler.upload_zip_file(zip_file_name, f'/adapttext/models/{zip_file_name}')

    # def download_classifier(self, zip_file_name):
    #     # zip_file_name = "test.zip"
    #     zip_archive = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    #     for item in self.classifiers_store_path:
    #         pkl_name = item + task_id + ".pkl"
    #         zip_archive.write(pkl_name)
    #     zip_archive.close()

    # response = make_response(zip_file_name.read())
    # response.headers.set('Content-Type', 'zip')
    # response.headers.set('Content-Disposition', 'attachment', filename='%s.zip' % os.path.basename(FILEPATH))
    # return response

    # dropbox_handler = DropboxHandler(self.data_root)
    # dropbox_handler.upload_zip_file(zip_file_name, f'/adapttext/models/{zip_file_name}')
