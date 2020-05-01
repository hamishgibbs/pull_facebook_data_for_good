# pull_facebook_data_for_good
Imitate an API for downloading data from Facebook Data for Good

Currently, Facebook Data for Good does not provide an API to automatically download or update datasets.

This program uses selenium webdriver to imitate the behaviour of an API for downloading the full timeseries of a data collection.

*Disclaimer: This download routine will only work for those with access to Facebook Data for Good, and will only function for datasets to which the user has been granted access. This tool is not developed by or associated with Facebook, is is simply a utility to automate downloading data from the Facebook Data for Good Geoinsights Platform.*

### Installation
Clone this repository and alter the output file path in the makefile

### Usage

Currently functional for Mobility and Colocation datasets only.   

Download colocation data:  
```shell
$ make pull_colocation
```

Download mobility data:  
```shell
$ make pull_mobility
```

Run unit tests:
```shell
$ make test
```

Input your Facebook login credentials when prompted. These credentials are not stored on your computer but are passed directly to the webdriver.


### Target dataset files

This tool uses csv files with one row per target dataset. These files store the country name, earliest date of data publication, and download ID in the format:  

`country, id, origin_year, origin_month, origin_day, origin_hour`

To download the full timeseries of a new dataset, open Geoinsights and navigate to the desired data collection. Click `See all available downloads`.

The dataset ID is embedded in the url of this page. For example, the dataset ID for the collection stored at `https://www.facebook.com/geoinsights-portal/downloads/?id=243071640406689` is `243071640406689`.

#### Notes:
This is an early release with limited functionality, suggestions and contributions are welcome. To request a feature or report an issue with this tool, please [open an issue](https://github.com/hamishgibbs/pull_facebook_data_for_good/issues/new).

More info on Facebook Data for Good: https://dataforgood.fb.com/
