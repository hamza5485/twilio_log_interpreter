from logger import Logger
import os
import csv

log = Logger(os.path.basename(__file__))

if __name__ == '__main__':
    log.success(f"Everything Working")
