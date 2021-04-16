import click
import os
from datetime import datetime
import pull_fb.utils as utils
import pull_fb.url as url
import pull_fb.driver as driver
import pull_fb.credentials as credentials


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
    "-f",
    "--frequency",
    help="Dataset update frequency (hours). Default: 8.",
    default=8
)
@click.option(
    "-driver",
    "--driver_path",
    help="Path to webdriver.",
    default="/Applications/chromedriver",
)
@click.option(
    "-config",
    "--config_path",
    help=".config path. Default is requested from the repo, otherwise is read from provided local path or other http connection.",
    default="https://raw.githubusercontent.com/hamishgibbs/pull_facebook_data_for_good/master/.config",
)
@click.option(
    "-user",
    "--username",
    help="Facebook username.",
    default=None
)
@click.option(
    "-pass",
    "--password",
    help="Facebook password.",
    default=None
)
@click.option(
    "-driver_flags",
    "--driver_flags",
    help="Flags passed to chromedriver.",
    multiple=True,
    default=["--headless"]
)
@click.option(
    "-driver_prefs",
    "--driver_prefs",
    help="Preferences passed to chromedriver.",
    default={"download.default_directory": os.getcwd()}
)
def cli(
        dataset_name,
        area,
        outdir=None,
        end_date=None,
        frequency=None,
        driver_path=None,
        config_path=None,
        username=None,
        password=None,
        driver_flags=None,
        driver_prefs=None):
    """
    Entry point for the pull_fb cli.

    """

    pull_fb(dataset_name,
            area,
            outdir,
            end_date,
            frequency,
            driver_path,
            config_path,
            username,
            password,
            driver_flags,
            driver_prefs)


def pull_fb(dataset_name,
            area,
            outdir: str = os.getcwd(),
            end_date: datetime = datetime.now(),
            frequency: int = 8,
            driver_path: str = "/Applications/chromedriver",
            config_path: str = "https://raw.githubusercontent.com/hamishgibbs/pull_facebook_data_for_good/master/.config",
            username: str = None,
            password: str = None,
            driver_flags: list = ["--headless"],
            driver_prefs: dict = {"download.default_directory": os.getcwd()}):

    print("Reading dataset configuration...")
    # Get config variables from repository
    config = utils.get_download_variables(dataset_name,
                                          area,
                                          end_date,
                                          config_path)

    # Get date sequence between start and end dates
    data_dates = utils.get_file_dates(
        config["start_date"], config["end_date"], frequency
    )

    # Get downloaded dates from outdir
    existing_dates = utils.get_existing_dates(outdir, area)

    # Only download dates that have not already been downloaded
    download_dates = list(set(data_dates).difference(set(existing_dates)))

    download_dates.sort()

    # Get url of each of dataset
    download_urls = url.format_urls(dataset_name,
                                    config["dataset_id"],
                                    download_dates,
                                    config["dataset_extra"])


    # Get credentials here
    keys = credentials.get_credentials(username, password)

    # Authenticate webdriver
    request_cookies_browser = driver.authenticate_driver(keys,
                                                         driver_path,
                                                         driver_flags,
                                                         driver_prefs)

    # Download url sequence and move to output directory
    driver.download_data(download_urls,
                         area,
                         outdir,
                         request_cookies_browser)

    # Success message
    print('Done.')
