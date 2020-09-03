# mkdocs_autozip

An mkdocs plugin to automatically zip the source files as part of the build process.

## Background

As part of my work on online courses for the Raspberry Pi foundation, I wanted to give people access to download a complete zip of the source content which made up our online courses.

We were already using mkdocs to provide a, free to access, mirror of all our course content, so I decided to create a plugin to automatically zip all the source files used in creating the site.

Many of the images used in the content are hosted externally, so the plugin also needed the ability to download external images and include them in the zip.

## Install

Install using pip ::

```bash
pip3 install mkdocs-autozip
```

## Usage

Add the plugin into your `mkdocs.yml` file e.g. ::

```
    plugins:
        - search
        - autozip
```

The source zip file will be created on `mkdocs build` or `serve`.

By default the source zip file will:

+ be created in the root of the website 
+ with the filename `source.zip`
+ local images will be include but externally hosted images will not
+ a linked to the source.zip file will be added to the navigation with the title 'Documentation source (zip)'

You can change the configuration of the plugin by using the following options in mkdocs.yml:

+ `source_zip_dir` will set the directory of the source zip file 
+ `source_zip_file_name` will set the name of the file
+ setting `add_source_zip_to_nav` to `false` will stop a link being added to the navigation
+ `source_zip_nav_description` will change the title of the link in the navigation
+ setting `download_images` to `true` will cause images to be downloaded and saves to `/images` in the zip file
+ `download_image_zip_dir` will change the name of the directory where images are downloaded
+ setting `verbose` to `true` will output  more information during the source zip build

e.g.

```
    - autozip:
        source_zip_dir: download
        source_zip_file_name: my_source.zip
        add_source_zip_to_nav: false
        source_zip_nav_description: download the source for this site as a zip
        download_images: true
        download_image_zip_dir: downloaded_images
        verbose: true
```


Note - you only need to add the configuration options you wish to change. 

Be careful with the spacing of the options. mkdocs is very particular. There must be 4 spaces before the name of the option. e.g.

```
    - autozip:
        source_zip_dir: download
```

not:

```
    - autozip:
      source_zip_dir: download
```

## Status

Beta. Tested on a few sites, but you many experience problems. If you find an issues please [raise them](https://github.com/martinohanlon/mkdocs_autozip/issues :)

## Change history

### v0.1.0 - 2020-09-02

+ added the functionality to include a link to the source zip in the navigation
+ fixed issue with relative and absolute image paths
+ general tidy up

### v0.0.1 - 2020-08-25

+ first version
+ only tested with a handful of mkdocs sites
