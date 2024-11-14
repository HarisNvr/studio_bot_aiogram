from pathlib import Path

from aiogram.types import FSInputFile


def get_file(file_name: str, directory: Path) -> FSInputFile:
    """
    Prepare file for sending to user.

    :param directory: Directories full name.
    :param file_name: File's full name with extension.
    :return: An FSInputFile object containing the photo.
    """

    path = directory.joinpath(file_name)
    return FSInputFile(path)
