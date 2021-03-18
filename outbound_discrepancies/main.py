from logger import Logger
from typing import List, Dict
from datetime import datetime
import os
import csv

FILES = ["march_1", "march_2", "march_3", "march_4"]
EXT = ".csv"
CALL_LOG_DIR = "./outbound_discrepancies/call_logs/"
FLEX_LOG_DIR = "./outbound_discrepancies/flex_logs/"
INTERNAL_LOG_DIR = "./outbound_discrepancies/internal_logs/"
OUTBOUND = "__REDACTED__"

log = Logger(os.path.basename(__file__))


def get_file(file_name: str, dir: str) -> str:
    """returns file name for provided date"""
    if file_name in FILES:
        return dir + file_name + EXT
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


def internal_log_count(internal_log_file: str) -> None:
    internal_log_data: List = load_file(internal_log_file)
    log.info(f"total records in internal_log_file: {len(internal_log_data)}")


def flex_count(flex_log_file: str) -> None:
    flex_log_data: List = load_file(flex_log_file)
    flex_log_counter: int = 0
    for row in flex_log_data:
        flex_log_counter += int(row[2])
    log.info(f"total overflow count as per flex insights: {flex_log_counter}")


def api_req_count(call_log_file: str) -> List:
    call_log_data: List = load_file(call_log_file)
    call_log_counter: int = 0
    data: List = []
    for row in call_log_data:
        if row[6] == OUTBOUND and row[7] == "Outgoing API":
            data.append({
                "to": row[6],
                "from": row[5],
                "direction": row[7],
                "start_time": row[2]
            })
            call_log_counter += 1
    log.info(f"total count where called_to = '{OUTBOUND}' and direction = 'Outgoing API': {call_log_counter}")
    return data


def dial_req_count(call_log_file: str) -> List:
    call_log_data: List = load_file(call_log_file)
    data: List = []
    for row in call_log_data:
        if row[6] == OUTBOUND and row[7] == "Outgoing Dial":
            data.append({
                "incoming": {
                    "to": "",
                    "from": "",
                    "direction": "",
                    "start_time": ""
                },
                "outgoing": {
                    "to": row[6],
                    "from": row[5],
                    "direction": row[7],
                    "start_time": row[2]
                },
                "overflow_gap": 0.0,
            })
    for elem in data:
        for row in call_log_data:
            if row[7] == "Incoming" and row[5] == elem["outgoing"]["from"]:
                elem["incoming"]["to"] = row[6]
                elem["incoming"]["from"] = row[5]
                elem["incoming"]["direction"] = row[7]
                elem["incoming"]["start_time"] = row[2]
                gap: float = (datetime.strptime(elem["outgoing"]["start_time"].replace("AEDT ", ''),
                                         "%H:%M:%S %Y-%m-%d") - datetime.strptime(
                    elem["incoming"]["start_time"].replace("AEDT ", ''), "%H:%M:%S %Y-%m-%d")).total_seconds()
                elem["overflow_gap"] = gap

    log.info(f"total count where called_to = '{OUTBOUND}' and direction = 'Outgoing Dial': {len(data)}")
    return data


def print_stats(data: List) -> None:
    overflow_gaps: Dict = {}
    for e in data:
        key: float = e["overflow_gap"]
        if key not in overflow_gaps:
            overflow_gaps[key] = 1
        else:
            overflow_gaps[key] += 1
    log.info("Overflow_gaps ~> { gap_amount_sec: num_occurrences}")
    for key in overflow_gaps:
        log.info(f"{{ {key}: {overflow_gaps[key]} }}", indent=1)


if __name__ == '__main__':
    for file in FILES:
        log.info(f"*****_{file}_*****")
        internal_log_file: str = get_file(file, INTERNAL_LOG_DIR)
        call_log_file: str = get_file(file, CALL_LOG_DIR)
        flex_log_file: str = get_file(file, FLEX_LOG_DIR)
        internal_log_count(internal_log_file)
        log.info("===================")
        flex_count(flex_log_file)
        log.info("===================")
        req_instances: List = api_req_count(call_log_file)
        log.info("===================")
        dial_instances: List = dial_req_count(call_log_file)
        log.info("===================")
        print_stats(dial_instances)
