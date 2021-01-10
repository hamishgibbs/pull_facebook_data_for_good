import time
import requests
from datetime import datetime
from selenium import webdriver
from progress.bar import Bar
from io import StringIO
import pandas as pd


def authenticate_driver(keys: dict,
                        driver_path: str,
                        driver_flags: list,
                        driver_prefs: dict):

    # Define options for web driver
    chrome_options = webdriver.ChromeOptions()

    # Apply preferences to chrome driver
    chrome_options.add_experimental_option("prefs", driver_prefs)

    # Add individual flags to chromedriver prefs
    for flag in driver_flags:

        chrome_options.add_argument(flag)

    driver = webdriver.Chrome(
        executable_path=driver_path, options=chrome_options
    )

    # Login url for Geoinsights platform
    geoinsights_url = "https://www.facebook.com/login/?next=https%3A%2F%2Fwww.facebook.com%2Fgeoinsights-portal%2F"

    # Access login url with webdriver
    driver.get(geoinsights_url)

    # Pause for page load (and cookie acceptance)
    time.sleep(5)

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

    time.sleep(1)

    # Get cookies from authenticated web driver
    request_cookies_browser = driver.get_cookies()

    driver.quit()

    return(request_cookies_browser)


def download_data(
    download_urls: list,
    area: str,
    driver_path: str,
    keys: dict,
    outdir: str,
    driver_flags: list,
    driver_prefs: dict
):

    request_cookies_browser = authenticate_driver(keys,
                                                  driver_path,
                                                  driver_flags,
                                                  driver_prefs)

    s = requests.Session()

    # Pass the cookies from the authenticated webdriver to the session
    [s.cookies.set(c['name'], c['value']) for c in request_cookies_browser]

    # Start download bar
    print("\n")
    bar = Bar("Downloading", max=len(download_urls))

    # Store unsuccessful download file names
    download_failed = []

    # For each download url, download dataset
    for i, url in enumerate(download_urls):

        # Request dataset from URL
        resp = s.get(url["url"])

        # Define output file name
        out_fn = format_out_fn(outdir, area, url["date"])

        if resp.status_code == 200:

            try:

                # try to convert response data to csv with >1 row
                data = response_as_dataframe(resp.text)

                # Write response data as csv
                data.to_csv(out_fn)

            except Exception:

                # Append failed filename download
                download_failed.append(out_fn)

                pass

        # Update progress bar
        bar.next()

    # Close progress bar
    bar.finish()

    print('Failed to download {} files. Please try again later.'.format(len(download_failed)))


def response_as_dataframe(text: str):

    data = StringIO(text)

    df = pd.read_csv(data)

    try:

        assert len(df.index) > 1

    except Exception as e:

        raise e

    return(df)


def format_out_fn(outdir: str, area: str, date: datetime):

    # Define new file name as AREA_DATE.csv
    new_name = outdir + "/" + area + date.strftime("_%Y_%m_%d_%H%M") + ".csv"

    return(new_name)
