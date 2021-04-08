from lib.logger import Logger
from typing import List
import pathlib
import os
import csv

log = Logger(os.path.basename(__file__))

EXT = ".csv"


def get_file(file_name: str, dir: str) -> str:
    """returns file name for provided date"""
    file = f"{pathlib.Path().absolute()}/{dir}/{file_name}{EXT}"
    if os.path.exists(file):
        log.success(f"File found: {file}!")
        return file
    else:
        log.error(f"{file_name}{EXT} not found in {dir}")
        raise Exception("404")


def load_file(file_name: str) -> List[List]:
    file_content = []
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        for row in reader:
            file_content.append(row)
    return file_content
