from getpass import getpass


def get_credentials(username, password):
    """
    Prompt for Facebook login get_credentials

    Future: add option to cache encrypted credentials
    """

    # Prompt for username
    if username is None:

        username = input("Email: ")

    # Prompt for password
    if password is None:

        password = getpass("Password: ")

    # Return dictionary of username and password
    return {"email": username, "password": password}
