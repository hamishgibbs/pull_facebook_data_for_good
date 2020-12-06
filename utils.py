import requests
import os
import glob
from datetime import datetime, timedelta


def get_config():
    """
    Funciton to get configuration file from online repository
    """

    # url for config variables
    config_url = "https://raw.githubusercontent.com/hamishgibbs/pull_facebook_data_for_good/master/.config"

    # Try to get config file or raise exception
    try:

        r = requests.get(config_url)

    except requests.exceptions.RequestException as e:

        raise SystemExit(e)

    # Extract config variables to dictionary or raise Exception
    try:
        config = dict(x.split("=") for x in r.text.split("\n")[:-1])

    except Exception:

        raise Exception("Malformed .config file.")

    # Return config variables as a dictionary
    return(config)


def get_download_variables(dataset: str, country: str, end_date: str):
    """
    Function to get downlaod variable for a particular dataset from config file

    This could be simplified
    """

    # Get config variables from repository
    config = get_config()

    # Extract dataset id or raise missing dataset error
    try:

        dataset_id = config["_".join([country, dataset, "ID"])]

    except Exception:

        raise KeyError(
            "No config value for {}. To add a new dataset, see the Readme.".format(
                "_".join([country, dataset, "ID"])
            )
        )

    # Extract dataset origin or raise missing dataset error
    try:

        dataset_origin = config["_".join([country, dataset, "Origin"])]

    except Exception:

        raise KeyError(
            "No config value for {}.  To add a new dataset, see the Readme.".format(
                "_".join([country, dataset, "Origin"])
            )
        )

    # Convert datset origin string to datetime object
    dataset_origin = date_str_to_datetime(dataset_origin)

    # Return config variables as dict
    return {
        "dataset_id": dataset_id,
        "start_date": dataset_origin,
        "end_date": end_date,
    }


def date_str_to_datetime(date: str):
    """
    Function to parse origin date in the format '%Y_%m_%d_%H' or '%Y_%m_%d'
    """

    # List of recognized date formats
    formats = ["%Y_%m_%d_%H%M", "%Y_%m_%d_%H", "%Y_%m_%d"]

    # Try to match formats until one succeeds
    for format in formats:

        try:

            # Return datetime object
            return datetime.strptime(date, format)

        except ValueError:

            pass

    # Raise ValueError for unknown date format
    raise ValueError("Unknown date format.")


def get_file_dates(start_date, end_date, frequency):
    """
    Function to get date sequence between start_date and end_date with a
    given frequency

    This could be replaced by a datetime function
    """

    # List to store dataset dates
    data_dates = []

    # Define start of date list
    date = start_date

    # Loop through date range, incrementing by `frequency` hours
    while date < end_date:

        data_dates.append(date)

        date = date + timedelta(hours=frequency)

    # Return list of dataset dates
    return data_dates


def get_existing_dates(outdir: str, area: str):
    """
    Function to get dates from files in the outdir
    """

    # Extract file names from csv files in outdir
    date_str = [os.path.basename(x) for x in glob.glob(outdir + "/*.csv")]

    # Remove area from file name
    date_str = [x.replace(area + "_", "") for x in date_str]

    # Remove extension from file name
    date_str = [x.replace(".csv", "") for x in date_str]

    # Convert date string to datetime object
    date_str = [date_str_to_datetime(x) for x in date_str]

    # If any existing files are found, notify user
    if len(date_str) > 0:

        message = "Found existing collection in output directory ({} files).\nOnly new files will be downloaded."

        print(message.format(str(len(date_str))))

    # Return a list of the dates of datasets that have already been downloaded
    return date_str
