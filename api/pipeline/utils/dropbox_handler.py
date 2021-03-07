import time
import emoji
import os
from tqdm import tqdm
import dropbox
from dropbox.files import WriteMode

from ..fastai1.basics import *

class DropboxHandler:
    def __init__(self, app_root, lang='si'):
        self.lang = lang
        self.app_root = app_root
        self.access_token = 's95ugxFduIUAAAAAAAAAAczIv3XTjtvlZ5muMcYvfUKYHY__DKsx_qwzLCL5rPCf'
        self.dbx = dropbox.Dropbox(self.access_token)

    # Upload a df as a text file
    def upload_text_file(self, df):

        time_str_fname = self.app_root + "/" + time.strftime("%Y%m%d-%H%M%S") + ".txt"

        np.savetxt(time_str_fname, df.values, fmt='%d')

        file_to_upload = time_str_fname
        file_where_to = "/adapttext/articles/" + time_str_fname

        self.upload(file_to_upload, file_where_to)

    # Upload the zip file to the destination
    def upload_zip_file(self, local_zip_path, destination_path):
        # file_where_to = "/adapttext/models/" + file_name
        self.upload(local_zip_path, destination_path)

    def download_articles(self):
        articles_path = self.app_root + "/data/" + self.lang + "wiki/articles/"
        if not Path(articles_path).exists():
            raise Exception("Wiki articles are not downloaded..")

        response = self.dbx.files_list_folder("/adapttext/articles")
        files_list = []
        dest_file_paths = []
        for file in response.entries:
            file_name = "/adapttext/articles/" + file.name
            metadata, res = self.dbx.files_download(file_name)
            f_down_content = res.content

            dest_path = "/downloads/" + file.name
            files_list.append(dest_path)
            dest_file_paths.append(articles_path + file.name)

            with open("/downloads/" + file.name, "wb") as f:
                metadata, res = self.dbx.files_download(file_name)
                f.write(res.content)

        for source, destination in zip(files_list, dest_file_paths):
            shutil.move(source, destination)

    def download_pretrained_model(self, zip_file_name):
        file_from = f'/adapttext/models/{zip_file_name}'

        with open(zip_file_name, "wb") as f:
            metadata, res = self.dbx.files_download(file_from)
            f.write(res.content)

    # Upload the zip file to the destination
    def upload(self, file_to_upload, file_where_to):
        with open(file_to_upload, "rb") as f:
            file_size_to_upload = os.path.getsize(file_to_upload)
            chunk_size_to_upload = 4 * 1024 * 1024
            if file_size_to_upload <= chunk_size_to_upload:
                print(self.dbx.files_upload(f.read(), file_where_to, mode=WriteMode('overwrite')))
            else:
                with tqdm(total=file_size_to_upload, desc="Uploaded") as pbar:
                    # Start an upload session
                    dbx_upload_session_begin = self.dbx.files_upload_session_start(
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
                                self.dbx.files_upload_session_finish(
                                    f.read(chunk_size_to_upload), cursor, commit
                                )
                            )
                        else:
                            self.dbx.files_upload_session_append(
                                f.read(chunk_size_to_upload),
                                cursor.session_id,
                                cursor.offset,
                            )
                            cursor.offset = f.tell()
                        pbar.update(chunk_size_to_upload)