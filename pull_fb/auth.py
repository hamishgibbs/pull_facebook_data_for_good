import requests
import browser_cookie3


def get_auth_cookies():

    return browser_cookie3.load(domain_name=".facebook.com")


def check_auth(cookies):

    login_url = "https://partners.facebook.com/data_for_good/"

    r = requests.get(login_url, cookies=cookies)

    if 'x-fb-rlafr' in r.headers.keys():

        print("Authenticated.")

        return True

    else:

        print(f"Not authenticated. You must log in to {login_url} in your default browser.")

        return False
