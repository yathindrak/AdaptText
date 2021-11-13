import time
import emoji
import os
from tqdm import tqdm
import dropbox
from dropbox.files import WriteMode

from ..fastai1.basics import *

class DropboxHandler:
    """Handle Dropbox transactions"""
    def __init__(self, app_root, lang='si'):
        self.__lang = lang
        self.__app_root = app_root
        self.__access_token = 'ADD_DROPBOX_ACCESS_TOKEN_HERE'
        self.__dbx = dropbox.Dropbox(self.__access_token)

    def upload_text_file(self, df):
        """
        Upload dataframe as a text file
        """
        file_name = time.strftime("%Y%m%d-%H%M%S") + ".txt"

        time_str_fname = self.__app_root + "/" + file_name

        np.savetxt(time_str_fname, df.values, fmt='%5s')

        file_to_upload = time_str_fname
        file_where_to = "/adapttext/articles/" + file_name

        self.upload(file_to_upload, file_where_to)

    def upload_zip_file(self, local_zip_path, destination_path):
        """
        Upload the zip file to the destination
        :rtype: object
        """
        self.upload(local_zip_path, destination_path)

    def download_articles(self):
        """
        Download articles for the pretrained model
        """
        articles_path = self.__app_root + "/data/" + self.__lang + "wiki/articles/"
        if not Path(articles_path).exists():
            raise Exception("Wiki articles are not downloaded..")

        response = self.__dbx.files_list_folder("/adapttext/articles")
        files_list = []
        dest_file_paths = []
        for file in response.entries:
            file_name = "/adapttext/articles/" + file.name
            metadata, res = self.__dbx.files_download(file_name)
            f_down_content = res.content

            dest_path = "/downloads/" + file.name
            files_list.append(dest_path)
            dest_file_paths.append(articles_path + file.name)

            with open("/downloads/" + file.name, "wb") as f:
                metadata, res = self.__dbx.files_download(file_name)
                f.write(res.content)

        for source, destination in zip(files_list, dest_file_paths):
            shutil.move(source, destination)

    def download_pretrained_model(self, zip_file_name):
        """
        Download pretrained model
        """
        file_from = f'/adapttext/models/{zip_file_name}'

        with open(zip_file_name, "wb") as f:
            metadata, res = self.__dbx.files_download(file_from)
            f.write(res.content)

    def download_classifier_model(self, zip_file_name, destination):
        """
        Download classification model
        """
        file_from = f'/adapttext/models/{zip_file_name}'

        with open(zip_file_name, "wb") as f:
            metadata, res = self.__dbx.files_download(file_from)
            f.write(res.content)

        shutil.move(zip_file_name, destination)

    def upload(self, file_to_upload, file_where_to):
        """
        Upload file
        """
        with open(file_to_upload, "rb") as f:
            file_size_to_upload = os.path.getsize(file_to_upload)
            chunk_size_to_upload = 4 * 1024 * 1024
            if file_size_to_upload <= chunk_size_to_upload:
                print(self.__dbx.files_upload(f.read(), file_where_to, mode=WriteMode('overwrite')))
            else:
                with tqdm(total=file_size_to_upload, desc="Uploaded") as pbar:
                    # Start an upload session
                    dbx_upload_session_begin = self.__dbx.files_upload_session_start(
                        f.read(chunk_size_to_upload)
                    )
                    pbar.update(chunk_size_to_upload)
                    cursor = dropbox.files.UploadSessionCursor(
                        session_id=dbx_upload_session_begin.session_id,
                        offset=f.tell(),
                    )
                    commit = dropbox.files.CommitInfo(path=file_where_to)
                    while f.tell() < file_size_to_upload:
                        if (file_size_to_upload - f.tell()) <= chunk_size_to_upload:
                            print(
                                self.__dbx.files_upload_session_finish(
                                    f.read(chunk_size_to_upload), cursor, commit
                                )
                            )
                        else:
                            self.__dbx.files_upload_session_append(
                                f.read(chunk_size_to_upload),
                                cursor.session_id,
                                cursor.offset,
                            )
                            cursor.offset = f.tell()
                        pbar.update(chunk_size_to_upload)