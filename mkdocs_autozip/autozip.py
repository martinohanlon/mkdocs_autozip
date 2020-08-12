import mkdocs
import os
import re
import urllib
import unicodedata

from zipfile import ZipFile
from collections import namedtuple
from tempfile import TemporaryDirectory
from time import time

class AutoZipPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('source_zip_dir', mkdocs.config.config_options.Type(str, None)),
        ('source_zip_file_name', mkdocs.config.config_options.Type(str, default='source.zip')),
        ('download_images', mkdocs.config.config_options.Type(bool, default=False)),
        ('download_image_zip_dir', mkdocs.config.config_options.Type(str, default='images')),
        ('verbose', mkdocs.config.config_options.Type(bool, default=False)),
    )

    def on_config(self, config, **kwargs):
        print(self.config)
        # self._source_files = []
        self._source_files = {}
        
        # set source zip filename
        config['source_zip_file_name'] = "source.zip" if not self.config['source_zip_file_name'] else self.config['source_zip_file_name']

        # set source zip directory
        if "source_zip_dir" not in self.config.keys():
            config['source_zip_dir'] = config["site_dir"]
        elif self.config['source_zip_dir'] is None:
            config['source_zip_dir'] = config["site_dir"]
        else:
            config['source_zip_dir'] = os.path.join(config["site_dir"], self.config['source_zip_dir'])

        config['source_zip_file_path'] = os.path.join(config['source_zip_dir'], config['source_zip_file_name'])

        # set download images
        config['download_images'] = False if not self.config['download_images'] else self.config['download_images']

        # set download images zip directory
        config['download_image_zip_dir'] = "images" if not self.config['download_image_zip_dir'] else self.config['download_image_zip_dir']

        # verbose
        config['verbose'] = False if not self.config['verbose'] else self.config['verbose']

        return config

    def on_pre_build(self, config):
        pass

    def on_page_markdown(self, markdown, page, config, files):

        # print(markdown)
        # print(config)

        # source markdown files
        self._source_files[page.file.src_path] = page.file.abs_src_path

        # find source images
        pattern = re.compile(r'!\[(.*?)\]\((.*?)\)', flags=re.IGNORECASE)

        matches = pattern.findall(markdown)
        for match in matches:

            url = match[1]
            
            # is it a local file?
            if "://" not in url:
                self._source_files[url] = os.path.join(config['docs_dir'], match[1])

            # its an external file
            else:
                if config['download_images']:
                    self._source_files[os.path.join(config['download_image_zip_dir'], self._url_to_filename(url))] = url
                
    # def on_post_page(self, output, page, config):
    #     self._source_files.append(page.file)
        
    #     # print(page.file.abs_src_path)
    #     # print(page.file.src_path)
    #     # print(page.file.abs_dest_path)
    #     # print(page.file.dest_path)

    def on_post_build(self, config):

        # print(config)

        print("INFO    -  Writing source zip file to {}".format(config['source_zip_file_path']))

        # make the source directory if it doesn't exist
        if not os.path.exists(config["source_zip_dir"]):
            os.makedirs(config["source_zip_dir"])

        # create temp directory to download any files too
        download_dir = TemporaryDirectory()
    
        # output the source files to the zip
        with ZipFile(config['source_zip_file_path'], "w") as source_zip:
            for source_file in self._source_files.keys():
                
                file_location = self._source_files[source_file]

                # does the file need downloading?
                if "://" in self._source_files[source_file]:
                    self._print_message(config, "INFO    -  Downloading {}".format(file_location))
                    try:
                        file_location = self._download_image(download_dir.name, file_location)
                    except (urllib.request.HTTPError, urllib.error.URLError) as error:
                        self._print_message(config, "ERROR   -  Failed to download {} - {}".format(file_location, error))
                        file_location = None

                # write the file to the zip
                if file_location is not None:
                    try:
                        source_zip.write(file_location, source_file)
                    except FileNotFoundError:
                        self._print_message(config, "WARNING -  File not found when writing to zip - {}".format(file_location))
                    
    def _download_image(self, download_dir, url):

        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        # create file name based on the time
        file_path = os.path.join(download_dir, str(time()))

        # download the file
        urllib.request.urlretrieve(url, file_path)
        
        return file_path

    def _url_to_filename(self, url):
        """
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens.
        """
        
        filename = unicodedata.normalize('NFKD', url)
        filename = re.sub('[^\w\s-]', '', filename).strip().lower()
        filename = re.sub('[-\s]+', '-', filename)
        
        parsed_url = urllib.parse.urlparse(url)

        # add any extension onto the file name
        filename += os.path.splitext(parsed_url.path)[1]

        return filename

    def _print_message(self, config, message):
        if config["verbose"]:
            print(message)

