import click
import os
from datetime import datetime
import utils
import url
import driver
import credentials
import clean_up


@click.command()
@click.option("-d", "--dataset_name", help="Dataset name to be downloaded.")
@click.option("-a", "--area", help="Area to be downloaded.")
@click.option(
    "-o",
    "--outdir",
    help="Outfile directory. Default: current directory.",
    default=os.getcwd(),
)
@click.option(
    "-e",
    "--end_date",
    help="Dataset end date. Default: datetime.now().",
    default=datetime.now(),
)
@click.option(
    "-f", "--frequency", help="Dataset update frequency (hours). Default: 8.", default=8
)
@click.option(
    "-driver",
    "--driver_path",
    help="Path to webdriver.",
    default="/Applications/chromedriver",
)
def cli(
    dataset_name, area, outdir=None, end_date=None, frequency=None, driver_path=None
):
    """
    Entry point for the pull_fb cli.

    Add args to manually pass start date, end date, id, and frequency

    """

    print("Reading dataset configuration...")
    config = utils.get_download_variables(dataset_name, area, end_date)

    data_dates = utils.get_file_dates(
        config["start_date"], config["end_date"], frequency
    )

    existing_dates = utils.get_existing_dates(outdir, area)

    download_dates = list(set(data_dates).difference(set(existing_dates)))

    # Get url of each of dataset
    download_urls = url.format_urls(dataset_name, config["dataset_id"], download_dates)

    # Get credentials here
    keys = credentials.get_credentials()

    # Download url sequence and move to output directory
    driver.download_data(download_urls, area, driver_path, keys, outdir)

    clean_up.remove_empty_files(outdir)
