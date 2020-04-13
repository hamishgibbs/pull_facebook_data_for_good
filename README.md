# pull_facebook_data_for_good
Imitate an API for downloading data from Facebook Data for Good

Currently, Facebook Data for Good does not provide an API to automatically download or update datasets.

This program uses selenium webdriver to replicate the behaviour of an API for downloading the full timeseries of a data collection.

*Disclaimer: This download routine will only work for those with access to Facebook Data for Good, and will only function for datasets to which the user has been granted access. This tool is not developed by or associated with Facebook, is is simply a utility to speed downloading data from the Facebook Data For Good Geoinsights Platform.*

### Installation
Clone this repository and alter the file paths in the makefile

### Usage
Target datsets are stored in a standard format (country, id, origin_date) in a csv file. Currently, the full timeseries of every listed datset is downloaded. 

Download colocation data: 
`make pull_colocation`

Download mobility data:
`make pull_mobility`

Run unit tests:
`make test`

Currently functional for Mobility and Colocation datasets only. 

Login credentials are stored in encrypted files on the user's local machine. To bypass the process of encrypting and decrypting login credentials, replace:
`keys = [fernet.decrypt(username).decode("utf-8") , fernet.decrypt(password).decode("utf-8")]`
with:
`keys = ["your_username@mail.com", "yourpassword"]`

#### Notes:
This is an early release with limited functionality, suggestions and contributions are welcome.

More info on Facebook Data for Good: https://dataforgood.fb.com/
