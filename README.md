# pull_facebook_data_for_good
Imitate an API for downloading data from Facebook Data for Good.

Currently, Facebook Data for Good does not provide an API to automatically download or update datasets.

This library uses selenium webdriver to imitate the behaviour of an API for downloading the full timeseries of a data collection.

This library is developed and tested in Python 3.8.

*Disclaimer: This download routine will only work for those with access to the Facebook Geoinsights platform, and will only function for datasets to which the user has been granted access. This tool is not developed by or associated with Facebook, it is simply a utility to automate downloading data from the Geoinsights Platform.*

### Installation

**From a clone:**

To develop this project locally, clone it onto your machine:

```shell
git clone https://github.com/hamishgibbs/pull_facebook_data_for_good.git
```

Enter the project directory:

```shell
cd pull_facebook_data_for_good
```

Install the package with:

```shell
pip install .
```

**From GitHub:**

To install the package directly from GitHub run:

```shell
pip install git+https://github.com/hamishgibbs/pull_facebook_data_for_good.git
```

### Usage

Currently functional for `TileMovement` datasets only.   

The command line interface follows the format:

```python
$ pull_fb --dataset_name --area
```

For example, to pull the `TileMovement` dataset for `Britain`:

```python
$ pull_fb --dataset_name TileMovement --area Britain
```

or:

```python
$ pull_fb --d TileMovement --a Britain
```

The country name must exactly match the name stored in the [`.config`](https://github.com/hamishgibbs/pull_facebook_data_for_good/blob/master/.config) file. For multi-word names, each word will be separated by `'_'`. *ie. New_Zealand*

**Please Note:**

If the [`.config`](https://github.com/hamishgibbs/pull_facebook_data_for_good/blob/master/.config) file is missing variables for a given dataset, please alter the [`.config`](https://github.com/hamishgibbs/pull_facebook_data_for_good/blob/master/.config) file and open a PR to share with others.

### Credentials

Credentials must be input manually on each download.

**Credentials are not stored on your computer but are passed directly to the Facebook login page by the web driver.**

### Tests

This project is tested with [`tox`](https://tox.readthedocs.io/en/latest/).

To run unit tests:

```shell
$ tox
```

### Contributions

#### Issues:

To request a feature or report an issue with this tool, please [open an issue](https://github.com/hamishgibbs/pull_facebook_data_for_good/issues/new).

#### Adding a dataset:

Dataset attributes are stored in the [`.config`](https://github.com/hamishgibbs/pull_facebook_data_for_good/blob/master/.config) file.

Each time you use the library, `pull_facebook_data_for_good` will look for dataset configuration variables here.

To add the ability to download another dataset, alter the `.config` file with two pieces of information:

1. The dataset id, embedded in the url of the Geoinsights download page. For example, the dataset ID for the collection stored at `https://www.facebook.com/geoinsights-portal/downloads/?id=243071640406689` is `243071640406689`.

2. The date origin of the dataset, the earliest date of data publication, in the format: `year_month_day(_hour)`. i.e. `2020_01_01_00`.

Please open a Pull Request to share the config variables for a new dataset with everyone.

#### Other contributions:

Other contributions are welcome.

Please look for [open issues](https://github.com/hamishgibbs/pull_facebook_data_for_good/issues?q=is%3Aopen+is%3Aissue) with the `Help Wanted` tag.
