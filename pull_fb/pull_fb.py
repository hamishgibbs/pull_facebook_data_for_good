import click
import os
from datetime import datetime
import browser_cookie3
import webbrowser
import zipfile
import requests
import glob
import pull_fb.utils as utils
import pull_fb.url as url
import pull_fb.driver as driver
import pull_fb.credentials as credentials


def get_auth_cookies():

    return browser_cookie3.load(domain_name = ".facebook.com")


@click.group()
def cli():
    pass


@click.group()
def auth():
    pass


@auth.command('status')
def auth_status():
    print("Checking auth status")


@auth.command('login')
def auth_login():
    webbrowser.get("https://partners.facebook.com/data_for_good/")


@click.group()
def collection():
    pass


@collection.command("init")
def collection_init():

    print("Getting authentication cookies...")
    cookies = get_auth_cookies()

    # replace this with args
    dataset_id = input("Dataset ID: ")

    # replace this with args
    start_date = input("Start date (YYYY-MM-DD): ")

    end_date = input("End date (YYYY-MM-DD): ")

    # replace this with args
    #end_date = datetime.strftime(datetime.now(), "%Y-%m-%d")

    url = "https://partners.facebook.com/data_for_good/bulk_download/?"
    query = f"resource_type=downloadable_csv&start_date={start_date}&end_date={end_date}&dataset_id={dataset_id}"

    print(url + query)

    r = requests.get(url + query,
                     cookies=cookies)

    print(r.request.url)
    print(r.status_code)
    print(r.headers)

    out_fn = os.getcwd() + "/" + r.headers["Content-Disposition"].replace(
        "attachment;filename=",
        "")

    with open(out_fn, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

    with zipfile.ZipFile(out_fn, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())

    os.remove(out_fn)


@collection.command("update")
def collection_update():

    # check that all ids are the same
    # check for duplicate files
    # ...check for missing files?

    files = glob.glob(os.getcwd() + "/*.csv")

    dataset_ids = [x.split("/")[-1].split("_")[0] for x in files]
    dates = [x.split("/")[-1].split("_")[1].replace(".csv", "") for x in files]
    dates = [datetime.strptime(x, "%Y-%m-%d") for x in dates]

    assert len(set(dataset_ids)) == 1

    start_date = datetime.strftime(max(dates), "%Y-%m-%d")
    end_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    dataset_id = dataset_ids[0]

    print(start_date, end_date, dataset_id)

    # get data function here


cli.add_command(auth)
cli.add_command(collection)


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
                                    download_dates)

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
