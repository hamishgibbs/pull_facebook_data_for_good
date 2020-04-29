# pull_facebook_data_for_good
Imitate an API for downloading data from Facebook Data for Good

Currently, Facebook Data for Good does not provide an API to automatically download or update datasets.

This program uses selenium webdriver to imitate the behaviour of an API for downloading the full timeseries of a data collection.

*Disclaimer: This download routine will only work for those with access to Facebook Data for Good, and will only function for datasets to which the user has been granted access. This tool is not developed by or associated with Facebook, is is simply a utility to automate downloading data from the Facebook Data for Good Geoinsights Platform.*

### Installation
Clone this repository and alter the output file path in the makefile

### Usage

Currently functional for Mobility and Colocation datasets only.   

Target datsets are stored in a standard format (country, id, origin_year, origin_month, origin_day, *origin_hour*) in a csv file. Currently, the full timeseries of every listed datset is downloaded.   

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

Input your Facebook login credentials when prompted. These credentials are not stored on your computer but are simply passed to the webdriver.

#### Notes:
This is an early release with limited functionality, suggestions and contributions are welcome.

More info on Facebook Data for Good: https://dataforgood.fb.com/
