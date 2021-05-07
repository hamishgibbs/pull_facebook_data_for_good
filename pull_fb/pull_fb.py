import click
import os
from datetime import datetime
import browser_cookie3
import zipfile
import requests
import glob


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

    print("Checking auth status...")

    cookies = get_auth_cookies()

    login_url = "https://partners.facebook.com/data_for_good/"

    r = requests.get(login_url, cookies=cookies)

    if 'x-fb-rlafr' in r.headers.keys():

        print("Authenticated.")

    else:

        print(f"Not authenticated. You must log in to {login_url} on your default browser.")


@click.group()
def collection():
    pass


def request_data(dataset_id, start_date, end_date, cookies):

    url = "https://partners.facebook.com/data_for_good/bulk_download/?"
    query = f"resource_type=downloadable_csv&start_date={start_date}&end_date={end_date}&dataset_id={dataset_id}"

    r = requests.get(url + query,
                     cookies=cookies)

    return r


def get_outfn(r):

    return os.getcwd() + "/" + r.headers["Content-Disposition"].replace(
        "attachment;filename=",
        "")


def write_zipfile(out_fn, r):

    with open(out_fn, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)


def unzip_data(out_fn):

    with zipfile.ZipFile(out_fn, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())


def download_data(dataset_id, start_date, end_date, cookies):

    r = request_data(dataset_id, start_date, end_date, cookies)

    out_fn = get_outfn(r)

    write_zipfile(out_fn, r)

    unzip_data(out_fn)

    os.remove(out_fn)


@collection.command("init")
def collection_init():

    print("Getting authentication cookies...")
    cookies = get_auth_cookies()

    # replace this with args
    dataset_id = input("Dataset ID: ")

    # replace this with args
    start_date = input("Start date (YYYY-MM-DD): ")

    # replace this with args
    end_date = input("End date (YYYY-MM-DD): ")

    download_data(dataset_id, start_date, end_date, cookies)


def get_file_dataset_ids(files: list):

    try:

        dataset_ids = [x.split("/")[-1].split("_")[0] for x in files]

    except Exception:

        raise Exception("Unable to parse dataset ids.")

    return dataset_ids


def get_file_dates(files: list):

    try:

        dates = [x.split("/")[-1].split("_")[1].replace(".csv", "")
                 for x in files]

        dates = [datetime.strptime(x, "%Y-%m-%d") for x in dates]

    except Exception:

        raise Exception("Unable to parse dates.")

    return dates


@collection.command("update")
def collection_update():

    # check that all ids are the same
    # check for duplicate files
    # ...check for missing files?

    cookies = get_auth_cookies()

    files = glob.glob(os.getcwd() + "/*.csv")

    dataset_ids = get_file_dataset_ids(files)
    dates = get_file_dates(files)

    assert len(set(dataset_ids)) == 1

    start_date = datetime.strftime(max(dates), "%Y-%m-%d")
    end_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    dataset_id = dataset_ids[0]

    print(start_date, end_date, dataset_id)

    download_data(dataset_id, start_date, end_date, cookies)

    # get data function here


cli.add_command(auth)
cli.add_command(collection)
