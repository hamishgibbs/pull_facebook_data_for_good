import click
from datetime import datetime

from pull_fb.auth import (
    get_auth_cookies,
    check_auth
)

from pull_fb.collection import (
    download_data,
    get_update_config,
)


@click.group()
def cli():
    pass


@click.group()
def auth():
    pass


@click.group()
def collection():
    pass


@auth.command('status')
def auth_status():

    cookies = get_auth_cookies()

    check_auth(cookies)


@collection.command("init")
@click.option('--dataset_id', required=True)
@click.option('--start_date', required=True)
@click.option('--end_date')
def collection_init(dataset_id,
                    start_date,
                    end_date=datetime.strftime(datetime.now(), "%Y-%m-%d")):

    cookies = get_auth_cookies()

    download_data(
        dataset_id,
        start_date,
        end_date,
        cookies
    )


@collection.command("update")
def collection_update():

    cookies = get_auth_cookies()

    config = get_update_config()

    download_data(
        config["dataset_id"],
        config["start_date"],
        config["end_date"],
        cookies
    )


cli.add_command(auth)
cli.add_command(collection)

# add pull_fb collection audit
# to check - no duplicate files
# all files are present in range
# Only one dataset id
