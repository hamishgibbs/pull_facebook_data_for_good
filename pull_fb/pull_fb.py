import click
import os
from datetime import datetime
import browser_cookie3
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
