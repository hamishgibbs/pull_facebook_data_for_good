import time
import glob
import os
from shutil import move
from datetime import datetime
from selenium import webdriver
from progress.bar import Bar


def download_data(
    download_urls: list, area: str, driver_path: str, keys: dict, outdir: str
):
    """
    Function to instantiate web driver, stuff credentials, and repeately hit download urls
    """

    chrome_options = webdriver.ChromeOptions()

    prefs = {"download.default_directory": outdir}

    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        executable_path=driver_path, chrome_options=chrome_options
    )

    geoinsights_url = "https://www.facebook.com/login/?next=https%3A%2F%2Fwww.facebook.com%2Fgeoinsights-portal%2F"

    driver.get(geoinsights_url)

    time.sleep(2)

    try:

        driver.find_element_by_xpath('//*[@id="u_0_h"]').click()

    except Exception:

        pass

    driver.find_element_by_xpath('//*[@id="email"]').send_keys(keys["email"])

    driver.find_element_by_xpath('//*[@id="pass"]').send_keys(keys["password"])

    driver.find_element_by_xpath('//*[@id="loginbutton"]').click()

    bar = Bar("Downloading", max=len(download_urls))

    for i, url in enumerate(download_urls):

        download_start = datetime.timestamp(datetime.now())

        driver.get(url["url"])

        latest_file = wait_for_download(download_start, outdir)

        rename_file(latest_file, outdir, area, url["date"])

        bar.next()

    bar.finish()


def wait_for_download(download_start: float, outdir: str):
    """Function to wait for a file to be downloaded"""

    new_files = 0

    while new_files == 0:

        downloaded_files = glob.glob(outdir + "/*.csv")

        ctimes = [os.path.getctime(x) for x in downloaded_files]

        new_files = sum([x > download_start for x in ctimes])

        time.sleep(3)

    latest_file = max(downloaded_files, key=os.path.getctime)

    return latest_file


def rename_file(latest_file: str, outdir: str, area: str, date: datetime):

    new_name = outdir + "/" + area + date.strftime("_%Y_%m_%d_%H%M") + ".csv"

    move(latest_file, new_name)
