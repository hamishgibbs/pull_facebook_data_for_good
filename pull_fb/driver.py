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

    # Define options for web driver
    chrome_options = webdriver.ChromeOptions()

    # Define download directory as outdir
    prefs = {"download.default_directory": outdir}

    # Apply options to chrome driver
    chrome_options.add_experimental_option("prefs", prefs)

    # Instantiate web driver
    driver = webdriver.Chrome(
        executable_path=driver_path, chrome_options=chrome_options
    )

    # Login url for Geoinsights platform
    geoinsights_url = "https://www.facebook.com/login/?next=https%3A%2F%2Fwww.facebook.com%2Fgeoinsights-portal%2F"

    # Access login url with webdriver
    driver.get(geoinsights_url)

    # Pause for page load (and cookie acceptance)
    time.sleep(2)

    # Try to accept cookies. On failure, pass
    try:

        driver.find_element_by_xpath('//*[@id="u_0_h"]').click()

    except Exception:

        pass

    # Add username in username form field
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(keys["email"])

    # Add password in password form field
    driver.find_element_by_xpath('//*[@id="pass"]').send_keys(keys["password"])

    # Click login button
    driver.find_element_by_xpath('//*[@id="loginbutton"]').click()

    # Start download bar
    print("\n\n---------------------")
    bar = Bar("Downloading", max=len(download_urls))
	
    # For each download url, download dataset
    for i, url in enumerate(download_urls):

        # Get time of download start
        download_start = datetime.timestamp(datetime.now())

        # Access download url
        driver.get(url["url"])

        # Wait for file to be downloaded
        latest_file = wait_for_download(download_start, outdir)

        # Rename file with formatted file name
        rename_file(latest_file, outdir, area, url["date"])

        # Update progress bar
        bar.next()

    # Close progress bar
    bar.finish()


def wait_for_download(download_start: float, outdir: str):
    """Function to wait for a file to be downloaded"""

    # Record the number of files that have been downloaded
    new_files = 0

    # Repeat check for downloaded files
    while new_files == 0:

        # Get all files in the outdir
        downloaded_files = glob.glob(outdir + "/*.csv")

        # Get creation time for each file
        ctimes = [os.path.getctime(x) for x in downloaded_files]

        # Check for files created after the download_start
        new_files = sum([x > download_start for x in ctimes])

        # Wait 3 seconds and retry
        time.sleep(3)

    # Latest downloaded file has the maximum creation time in the outdir
    latest_file = max(downloaded_files, key=os.path.getctime)

    # Return latest file filename
    return latest_file


def rename_file(latest_file: str, outdir: str, area: str, date: datetime):

    # Define new file name as AREA_DATE.csv
    new_name = outdir + "/" + area + date.strftime("_%Y_%m_%d_%H%M") + ".csv"

    # Move file (rename) from latest_file to new_name
    move(latest_file, new_name)
