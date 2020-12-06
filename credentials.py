from getpass import getpass


def get_credentials():
    '''
    Prompt for Facebook login get_credentials

    Future: add option to cache encrypted credentials
    '''

    username = input("Email: ")

    password = getpass("Password: ")

    return({
        'email': username,
        'password': password
    })
