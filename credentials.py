from getpass import getpass


def get_credentials():
    """
    Prompt for Facebook login get_credentials

    Future: add option to cache encrypted credentials
    """

    # Prompt for username
    username = input("Email: ")

    # Prompt for password
    password = getpass("Password: ")

    # Return dictionary of username and password
    return {"email": username, "password": password}
