from os import getenv

from dotenv import load_dotenv

load_dotenv()


def get_admin_ids() -> list[int]:
    """
    Fetches and returns a list of admin IDs from the environment variable
    'ADMIN_IDS'. The 'ADMIN_IDS' environment variable is expected to be a
    comma-separated string of numeric admin IDs, which are then converted
    to integers.

    :return: List of admin IDs as integers.
    """

    admin_ids = []

    for admin_id in (getenv('ADMIN_IDS').split(',')):
        admin_ids.append(int(admin_id))

    return admin_ids
