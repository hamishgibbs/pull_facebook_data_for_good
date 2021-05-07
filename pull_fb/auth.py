import requests
import browser_cookie3


def get_auth_cookies():

    print(u"\U0001f512" + " Getting authentication cookies...")

    return browser_cookie3.load(domain_name=".facebook.com")


def check_auth(cookies):

    login_url = "https://partners.facebook.com/data_for_good/"

    r = requests.get(login_url, cookies=cookies)

    check_auth_headers(r.headers, login_url)


def check_auth_headers(headers, login_url):

    if 'x-fb-rlafr' in headers.keys():

        print(u"\U00002705" + " Authenticated.")

        return True

    else:

        print(u"\U0000274c" + f" Not authenticated. You must log in to {login_url} in your default browser.")

        return False
