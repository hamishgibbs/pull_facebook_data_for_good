# pull_facebook_data_for_good
Imitate an API for downloading data from Facebook Data for Good

Currently, Facebook Data for Good does not provide an API to automatically download or update datasets.

This program uses selenium webdriver to imitate the behaviour of an API for downloading the full timeseries of a data collection.

*Disclaimer: This download routine will only work for those with access to Facebook Data for Good, and will only function for datasets to which the user has been granted access. This tool is not developed by or associated with Facebook, it is simply a utility to automate downloading data from the Facebook Data for Good Geoinsights Platform.*

### Installation
Clone and `cd` into this repository.
```shell
cd pull_facebook_data_for_good
```

### Usage

Currently functional for `TileMobility`, `TilePopulation`, and `Colocation` datasets only.   

The command line inteface follows the format:
```python
$ python pull.py [Country_Name] [DatasetName]
```

For example, to pull the `TileMobility` dataset for Britain:
```python
$ python pull.py Britain TileMobility
```

The country name must exactly match the name stored in the `.config` file. For multi-word names, each word will be separated by `'_'`. *ie. New_Zealand*

Run unit tests:
```python
$ python -m unittest
```

### Dataset Attributes

Dataset attributes are stored in the remote `.config` file of this repository. To add functionality for downloading another dataset, alter the `.config` file with two pieces of information:
1. The dataset id, embedded in the url of the Geoinsights download page. For example, the dataset ID for the collection stored at `https://www.facebook.com/geoinsights-portal/downloads/?id=243071640406689` is `243071640406689`.
2. The date origin of the dataset, the earliest date of data publication, in the format: `year_month_day(_hour)`.

Please open a PR to share the config variables for a new dataset in the `.config` file. 

### Credentials

Credentials can be input manually on each download or stored in a `.env` file.

If you are using a `.env` file, set the environment variables: `FB_USERNAME`, `FB_PASSWORD`, and `FB_OUTDIR`. 

If you are not using a `.env` file, input your Facebook login credentials when prompted. 

**Credentials are not stored on your computer but are passed directly to the Facebook login page by the web driver.**

#### Notes:
This is an early release with limited functionality, suggestions and contributions are welcome. To request a feature or report an issue with this tool, please [open an issue](https://github.com/hamishgibbs/pull_facebook_data_for_good/issues/new).

More info on Facebook Data for Good: https://dataforgood.fb.com/
