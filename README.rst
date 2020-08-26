mkdocs_autozip
==============

An mkdocs plugin to automatically zip the source files as part of the build process.

Background
----------

As part of my work on online courses for the Raspberry Pi foundation, I wanted to give people access to download a complete zip of the source content which made up our online courses.

We were already using mkdocs to provide a, free to access, mirror of all our course content, so I decided to create a plugin to automatically zip all the source files used in creating the site.

Many of the images used in the content are hosted externally, so the plugin also needed the ability to download external images and include them in the zip.

Install
-------

Install using pip ::

    pip3 install mkdocs-autozip

Usage
-----

Add the plugin into your `mkdocs.yml` file e.g. ::

    plugins:
        - search
        - autozip

The source zip file will be created on `mkdocs build` or `serve`.

By default the source zip file will:

+ be created in the root of the website 
+ with the filename `source.zip`
+ local images will be include but externally hosted images will not

You can change the configuration of the plugin by using the following options in mkdocs.yml:

+ `source_zip_dir` will set the directory of the source zip file 
+ `source_zip_file_name` will set the name of the file
+ setting `download_images` to `true` will cause images to be downloaded and saves to `/images` in the zip file
+ `download_image_zip_dir` will change the name of the directory where images are downloaded
+ setting `verbose` to `true` will output  more information during the source zip build

e.g. ::

    - autozip:
        source_zip_dir: download
        source_zip_file_name: my_source.zip
        download_images: true
        download_image_zip_dir: downloaded_images
        verbose: true

Be careful with the spacing of the options. mkdocs is very particular. There must be 4 spaces before the name of the option. e.g. ::

    - autozip:
        source_zip_dir: download

not ::

    - autozip:
      source_zip_dir: download

Status
------

Alpha. Expect issues.

Change history
--------------

v0.0.1 - 2020-08-25
^^^^^^^^^^^^^^^^^^^

+ first version
+ only tested with a handful of mkdocs sites
