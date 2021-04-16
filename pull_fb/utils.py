import requests
import os
import glob
from datetime import datetime, timedelta


def get_config(config_path):
    """
    Funciton to get configuration file from online repository
    """

    # Try to get config file or raise exception
    try:
        if config_path.startswith('http'):
            r = requests.get(config_path)
            config_var = r.text.split("\n")[:-1]
        else:
            with open(config_path) as f:
                r = f.readlines()
            config_var = [x.replace("\n", "") for x in r]

    except requests.exceptions.RequestException as e:

        raise SystemExit(e)

    # Extract config variables to dictionary or raise Exception
    try:
        config = dict(x.split("-") for x in config_var)

    except Exception:

        raise Exception("Malformed .config file.")

    # Return config variables as a dictionary
    return(config)


def get_download_variables(dataset: str, country: str, end_date: str, config_path: str):
    """
    Function to get downlaod variable for a particular dataset from config file

    This could be simplified
    """

    # Get config variables from repository
    config = get_config(config_path)

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

    # Extract extra element which appears in URL of certain datasets but not all
    try:

        dataset_extra = config["_".join([country, dataset, "Extra"])]

    except KeyError:

        dataset_extra = None

    # Return config variables as dict
    return {
        "dataset_id": dataset_id,
        "start_date": dataset_origin,
        "end_date": end_date,
        "dataset_extra": dataset_extra
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

    # Extract file names from csv files in outdir (only for current area)
    date_str = [os.path.basename(x) for x in glob.glob(outdir + "/" + area + "_" + "*.csv")]

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
