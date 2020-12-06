import requests
import os
import glob
from datetime import datetime, timedelta


def get_config():
    """
    Funciton to get configuration file from online repository
    """

    config_url = "https://raw.githubusercontent.com/hamishgibbs/pull_facebook_data_for_good/master/.config"

    try:
        r = requests.get(config_url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    try:
        config = dict(x.split("=") for x in r.text.split("\n")[:-1])

    except Exception:

        raise Exception("Malformed .config file.")

    return config


def get_download_variables(dataset: str, country: str, end_date: str):
    """
    Function to get downlaod variable for a particular dataset from config file

    This could be simplified
    """

    config = get_config()

    try:

        dataset_id = config["_".join([country, dataset, "ID"])]

    except Exception:

        raise KeyError(
            "No config value for {}. To add a new dataset, see the Readme.".format(
                "_".join([country, dataset, "ID"])
            )
        )

    try:

        dataset_origin = config["_".join([country, dataset, "Origin"])]

    except Exception:

        raise KeyError(
            "No config value for {}.  To add a new dataset, see the Readme.".format(
                "_".join([country, dataset, "Origin"])
            )
        )

    dataset_origin = date_str_to_datetime(dataset_origin)

    return {
        "dataset_id": dataset_id,
        "start_date": dataset_origin,
        "end_date": end_date,
    }


def date_str_to_datetime(date: str):
    """
    Function to parse origin date in the format '%Y_%m_%d_%H' or '%Y_%m_%d'
    """

    formats = ["%Y_%m_%d_%H%M", "%Y_%m_%d_%H", "%Y_%m_%d"]

    for format in formats:

        try:

            return datetime.strptime(date, format)

        except ValueError:

            pass

    print(date)

    raise ValueError("Unknown date format.")


def get_file_dates(start_date, end_date, frequency):
    """
    Function to get date sequence between start_date and end_date with a
    given frequency
    """

    data_dates = []

    date = start_date

    while date < end_date:

        data_dates.append(date)

        date = date + timedelta(hours=frequency)

    return data_dates


def get_existing_dates(outdir: str, area: str):
    """
    Function to get dates from files in the outdir
    """

    date_str = [os.path.basename(x) for x in glob.glob(outdir + "/*.csv")]

    date_str = [x.replace(area + "_", "") for x in date_str]

    date_str = [x.replace(".csv", "") for x in date_str]

    date_str = [date_str_to_datetime(x) for x in date_str]

    if len(date_str) > 0:

        message = "Found existing collection in output directory ({} files).\nOnly new files will be downloaded."

        print(message.format(str(len(date_str))))

    return date_str
