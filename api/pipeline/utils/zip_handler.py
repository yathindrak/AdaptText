import zipfile
import emoji

from ..fastai1.basics import *

class ZipHandler:
    def __init__(self):
        pass

    # Get wiki articles
    def build_zip(self, zip_file_name, files_to_write):
        # zip_file_name = "sinhala-hate-speech-classifier.zip"
        zip_archive = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        for file_name in files_to_write:
            zip_archive.write(file_name)
        zip_archive.close()

    def unzip(self, file_name):
        current_working_dir = os.getcwd()
        with zipfile.ZipFile(file_name, 'r') as archive:
            archive.extractall(current_working_dir)

    def prepare_articles(self, path):
        base_lm_data_path = path / 'articles'
        if base_lm_data_path.exists():
            print(f"{base_lm_data_path} articles already exists")
            return base_lm_data_path

        base_lm_data_path.mkdir(exist_ok=True, parents=True)
        heading_regex = re.compile(
            rf'<doc id="\d+" url="https://{self.lang}.wikipedia.org/wiki\?curid=\d+" title="([^"]+)">')
        lines_list = (path / self.lang_code).open()
        f = None

        for index, line in enumerate(lines_list):
            if line.startswith('<doc id="'):
                heading = heading_regex.findall(line)[0].replace('/', '_')
                heading = ' '.join(heading.split()[:5])
                if len(heading) > 150: continue
                if f: f.close()
                f = (base_lm_data_path / f'{heading}.txt').open('w')
            else:
                f.write(emoji.demojize(line))

        f.close()

        return base_lm_data_path