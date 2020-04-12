# pull_facebook_data_for_good
Imitate an API for downloading data from Facebook Data For Good

Disclaimer: This download routine will only work for those with access to Facebook Data for Good, and will only function for datasets to which the user has been granted access.  

Currently, Facebook Data for Good does not provide an API to automatically download or update datasets.

This program uses selenium webdriver to replicate the behaviour of an API for downloading the full timeseries of a data collection. 

Currently functional for Mobility and Colocation datasets. 

Login credentials are stored in encrypted files on the user's local machine. 

Target datsets are stored in a standard format (country, id, date) in a csv file. Currently, the full timeseries of every listed datset is downloaded. 

Note: this is an early release with limited functionality, suggestions and contributions are welcome.