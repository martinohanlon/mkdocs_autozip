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
        ("source_zip_dir", mkdocs.config.config_options.Type(str, default="")),
        ("source_zip_file_name", mkdocs.config.config_options.Type(str, default="source.zip")),
        ("add_source_zip_to_nav", mkdocs.config.config_options.Type(bool, default=True)),
        ("source_zip_nav_description", mkdocs.config.config_options.Type(str, default="Documentation source (zip)")),
        ("download_images", mkdocs.config.config_options.Type(bool, default=False)),
        ("download_image_zip_dir", mkdocs.config.config_options.Type(str, default="images")),
        ("verbose", mkdocs.config.config_options.Type(bool, default=False)),
    )

    def on_config(self, config, **kwargs):
        """
        Setup the configuration
        """
        
        config["source_zip_file_name"] = "source.zip" if not self.config["source_zip_file_name"] else self.config["source_zip_file_name"]
        config["source_zip_dir"] = "" if not self.config["source_zip_dir"] else self.config["source_zip_dir"]
        config["add_source_zip_to_nav"] = False if not self.config["add_source_zip_to_nav"] else self.config["add_source_zip_to_nav"]
        config["source_zip_nav_description"] = "Documentation source (zip)" if not self.config["source_zip_nav_description"] else self.config["source_zip_nav_description"]
        config["download_images"] = False if not self.config["download_images"] else self.config["download_images"]
        config["download_image_zip_dir"] = "images" if not self.config["download_image_zip_dir"] else self.config["download_image_zip_dir"]
        config["verbose"] = False if not self.config["verbose"] else self.config["verbose"]

        return config

    def on_pre_build(self, config):
        """
        Setup the plugin.
        """

        self._source_files = {}
        
        # set source zip file path
        if config["source_zip_dir"] == "/":
            self._source_zip_file_path = os.path.join(config["site_dir"], config["source_zip_file_name"])
        else:
            self._source_zip_file_path = os.path.join(config["site_dir"], config["source_zip_dir"], config["source_zip_file_name"])

    def on_page_markdown(self, markdown, page, config, files):
        """
        Create a list of the source markdown files and any images they link too for inclusion in the source zip
        """

        # source markdown file
        self._source_files[page.file.src_path] = page.file.abs_src_path

        # find source images
        pattern = re.compile(r'!\[(.*?)\]\((.*?)\)', flags=re.IGNORECASE)
        matches = pattern.findall(markdown)
        for match in matches:

            url = match[1].lstrip()

            if len(url) > 0:
            
                # is it a local file?
                if "://" not in url:

                    # is the path absolute
                    if url[0] == "/":
                        self._source_files[url] = os.path.join(config["docs_dir"], url[1:])

                    # its a relative path
                    else:
                        self._source_files[os.path.join(os.path.dirname(page.file.src_path), url)] = os.path.join(os.path.dirname(page.file.abs_src_path), url)

                # its an external file
                else:
                    if config["download_images"]:
                        self._source_files[os.path.join(config["download_image_zip_dir"], self._url_to_filename(url))] = url

    def on_nav(self, nav, config, files):
        """
        Add the link to the source zip file to the navigation.
        """

        if config["add_source_zip_to_nav"]:
            source_zip_rel_link = os.path.join(config["source_zip_dir"], config["source_zip_file_name"])
            link_to_source = mkdocs.structure.nav.Link(config["source_zip_nav_description"], source_zip_rel_link)
            nav.items.append(link_to_source)
            self._print_message(config, "INFO    -  Added navigation - {} - {}".format(config["source_zip_nav_description"], source_zip_rel_link))
            
    def on_post_build(self, config):
        """
        Create the zip file.
        Download any external images (if required).
        """

        print("INFO    -  Writing source zip file to {}".format(self._source_zip_file_path))

        # make the directory for the source zip if it doesn't exist
        os.makedirs(os.path.dirname(self._source_zip_file_path), exist_ok=True)
        
        # create temp directory to download any files too
        download_dir = TemporaryDirectory()
    
        # output the source files to the zip
        with ZipFile(self._source_zip_file_path, "w") as source_zip:
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
        opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36")]
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
        
        filename = unicodedata.normalize("NFKD", url)
        filename = re.sub('[^\w\s-]', '', filename).strip().lower()
        filename = re.sub('[-\s]+', '-', filename)
        
        parsed_url = urllib.parse.urlparse(url)

        # add any extension onto the file name
        filename += os.path.splitext(parsed_url.path)[1]

        return filename

    def _print_message(self, config, message):
        if config["verbose"]:
            print(message)

