FutureLearn Data Downloader
==============================

The FutureLearn Data Downloader is a utility for accessing data about `FutureLearn <https://futurelearn.com>`_ courses.

The API and download utility will download data for all runs of multiple courses, combining them together into a single dataset. 

It is useful for doing data analysis either in Python using `pandas`_ or with `csv` files.

The `full documentation <https://fl-data-downloader.readthedocs.io/>`_ describes how to install, its API and the download utility.

What you need?
--------------

To use the dataset downloader utility you will need:

+ Access to the internet
+ `Python 3 <https://www.python.org/downloads/>`_ installed on your computer (be sure to click *Add Python to the PATH* when installing on Windows)
+ a FutureLearn account which can access your courses dataset files

Install
-------

Open a command prompt or terminal and enter this command::

    pip3 install fl-data-downloader

To upgrade to the latest version use::

    pip3 install fl-data-downloader --upgrade

If you are installing on macOS or linux you may need to use `sudo` when running `pip3` in order to install the utility::

    sudo pip3 install fl-data-downloader

If you are using Windows and you receive a `pip3 is not recognised` error, have a look at this guide to `Using pip on Windows <https://projects.raspberrypi.org/en/projects/using-pip-on-windows>`_.

API
---

The `fl_data_downloader` API can be used to gain and manipulate data using Python.

Data is returned as `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_ objects. See the `pandas Getting started <https://pandas.pydata.org/pandas-docs/stable/getting_started/index.html>`_ for more information.

To use the API create a `FutureLearnData` object passing the organisation and call a `get_` method e.g.::

    from fl_data_downloader import FutureLearnData
            
    fl = FutureLearnData("raspberry-pi")

    enrolments_df = fl.get_dataset_for_course(course="programming-101", dataset="enrolments")

    print(enrolments_df)

There are code `examples <https://github.com/raspberrypilearning/fl-data-downloader/tree/master/fl_data_downloader/examples>`_ of how to use all the API calls in the `github repository <https://github.com/raspberrypilearning/fl-data-downloader>`_.

For more information see the `API documentation <https://fl-data-downloader.readthedocs.io/en/latest/api.html>`_.

CSV download tool
-----------------

The `fl-data-dl` command line tool can be used to download data for FutureLearn courses and datasets.

Each dataset is downloaded to a separate file with the name `[yyyy-mm-dd-hh-mm-ss]-[dataset].csv`

Using the `-h` option will display the `fl-data-dl` command usage instructions::

    fl-data-dl -h

::

    usage: fl-data-dl [-h] [-d DATASET [DATASET ...]] [-o OUTPUT] [-l] [-v] organisation course [course ...]

    FutureLearn Data Downloader

    positional arguments:
    organisation          The organisation you want to download data for.
    course                The course(s) you want to download data for.

    optional arguments:
    -h, --help            show this help message and exit
    -d DATASET [DATASET ...], --dataset DATASET [DATASET ...]
                            The dataset(s) you wish to download data for: archetype_survey_responses, campaigns, comments, enrolments,
                            leaving_survey_responses, peer_review_assignments, peer_review_reviews, post_course_survey_data,
                            post_course_survey_free_text, question_response, step_activity, team_members, video_stats,
                            weekly_sentiment_survey_responses
    -o OUTPUT, --output OUTPUT
                            The output directory where the data files should be written, defaults to the current directory.
    -l, --login           Login and store FutureLearn credentials.
    -V, --version         Display the version number
    --no-cache            Disable the cache.

e.g. to download all the datasets for all the runs of the `programming-101` course from the `raspberry-pi` organisation::

    fl-data-dl raspberry-pi programming-101

When the downloader is run, you will be asked to enter your FutureLearn username and password. 

See the `CSV downloader documentation <https://fl-data-downloader.readthedocs.io/en/latest/downloader.html#examples>`_ for more examples.

.. _pandas: https://pandas.pydata.org/