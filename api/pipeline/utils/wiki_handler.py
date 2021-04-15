from ..fastai1.basics import *
import emoji

class WikiHandler:
    def __init__(self, lang='si'):
        self.lang = lang
        self.lang_code = f'{lang}wiki'

    # Get wiki articles
    def retrieve_articles(self, path):
        if (path / self.lang_code).exists():
            print(f"{path / self.lang_code} wiki-data already exists...")
            return

        xml_path = f"{self.lang}wiki-latest-pages-articles.xml"
        zip_path = f"{xml_path}.bz2"

        # download wiki articles, if not exists
        if not (path / xml_path).exists():
            print("downloading articles...")
            # wiki_source_uri = f'https://dumps.wikimedia.org/{self.lang_code}/latest/{zip_path}'
            wiki_source_uri = 'https://dumps.wikimedia.org/siwiki/20210220/siwiki-20210220-pages-articles-multistream.xml.bz2'
            download_url(wiki_source_uri, path / zip_path)
            print("unzipping articles archive...")
            bunzip(path / zip_path)

        # change working dir to 'path'
        with working_directory(path):
            print("extracting wiki articles...")
            wiki_extraction_cmd = "python -m wikiextractor.WikiExtractor --processes 4 --no_templates " + f"--min_text_length 1800 --filter_disambig_pages --log_file log -b 100G -q {xml_path}"
            os.system(wiki_extraction_cmd)

        # Perform directory cleanup
        shutil.move(str(path / 'text/AA/wiki_00'), str(path / self.lang_code))
        shutil.rmtree(path / 'text')

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