from lib.logger import Logger
from lib.functions import get_file, load_file
import os
import pytz

log = Logger(os.path.basename(__file__))

FILES = ["march_9" , "march_10", "march_11", "march_12", "march_15", "march_16", "march_17", "march_18"]
PROJ_DIR = "15_second_intervals/"
FLEX_INSIGHTS = f"flex_insights"
CONSOLE_LOGS = f"twilio_console_logs"


def insights_15_min_gap(file_name: str) -> int:
    data = load_file(file_name)
    daily_discrepancy_counter = 0
    for d in data:
        hoa = int(d[3]) + int(d[4]) + int(d[5])
        sla = int(d[6]) + int(d[7]) + int(d[8]) + int(d[9]) + int(d[10])
        diff_h_sla = int(d[3]) - sla
        if diff_h_sla > 0:
            daily_discrepancy_counter += 1
            log.info(f"@ {d[0]} - ")
            log.info(f"total convo =               {d[1]}", indent=3)
            log.info(f"total inbound convo =       {d[2]}", indent=3)
            log.warn(f"                                 -----------")
            log.info(f"H =                      {d[3]}", indent=3)
            log.info(f"O =                      {d[4]}", indent=3)
            log.info(f"A =                      {d[5]}", indent=3)
            log.warn(f"                                 -----------")
            log.info(f"H+O+A =                     {hoa}", indent=3)
            log.info(f"SLA =                       {sla}", indent=3)
            log.info(f"diff b/w H & SLA =          {diff_h_sla}", indent=3)
            log.error("===================")
    # log.warn(f"discrepancies on {file_name.split('flex_insights/')[1]} : {daily_discrepancy_counter}")
    return daily_discrepancy_counter


def insights_total(file_name: str) -> None:
    data = load_file(file_name)
    t_h = 0
    t_o = 0
    t_a = 0
    t_convo = 0
    t_inbound = 0
    t_sla = 0
    for d in data:
        t_h += int(d[3])
        t_o += int(d[4])
        t_a += int(d[5])
        t_convo += int(d[1])
        t_inbound += int(d[2])
        t_sla += int(d[6]) + int(d[7]) + int(d[8]) + int(d[9]) + int(d[10])
    # log.error(f"[__INSIGHTS__]: total convo for {file_name.split('flex_insights/')[1]} : {t_convo}", indent=3)
    log.warn(f"[__INSIGHTS__]: total inbound for {file_name.split('flex_insights/')[1]} : {t_inbound}", indent=3)
    log.info(f"[__INSIGHTS__]: total handled for {file_name.split('flex_insights/')[1]} : {t_h}", indent=1)
    log.info(f"[__INSIGHTS__]: total overflow for {file_name.split('flex_insights/')[1]} : {t_o}", indent=1)
    log.info(f"[__INSIGHTS__]: total abandoned for {file_name.split('flex_insights/')[1]} : {t_a}", indent=1)
    log.warn(f"[__INSIGHTS__]: total SLA for {file_name.split('flex_insights/')[1]} : {t_sla}", indent=3)
    log.info(f"[__INSIGHTS__]: SLA + A = {t_sla + t_a}", indent=1)
    log.info(f"[__INSIGHTS__]: SLA + O = {t_sla + t_o}", indent=1)
    log.error(f"[__INSIGHTS__]: SLA + A + O = {t_sla + t_a + t_o}", indent=3)
    log.error(f"[__INSIGHTS__]: inbound - (A + O) = {t_inbound - (t_a + t_o)}", indent=3)


def console_total_incoming(file_name: str) -> None:
    data = load_file(file_name)
    incoming_counter = 0
    for d in data:
        if d[7] == "Incoming":
            incoming_counter += 1
            # log.info(f"{incoming_counter} -- incoming call logged @ {d[2]}")
    log.warn(f"[__CONSOLE__]: total incoming for {file_name.split('twilio_console_logs/')[1]} : {incoming_counter}",
             indent=3)


def is_time_between(begin_time: str, end_time: str, check_time: str) -> bool:
    begin_time = begin_time.replace('AEDT', '+1100')
    end_time = end_time.replace('AEDT', '+1100')
    check_time = check_time.replace('AEDT', '+1100')
    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def incoming_during_time(file_name: str, time_start: str, time_end: str):
    data = load_file(file_name)
    counter = 0
    incoming_counter = 0
    O_API_counter = 0
    O_D_counter = 0
    incoming_arr = []
    temp_arr = []
    for d in data:
        if is_time_between(time_start, time_end, d[2]):
            counter += 1
            if d[7] == "Incoming":
                incoming_counter += 1
            if d[7] == "Outgoing API":
                O_API_counter += 1
            if d[7] == "Outgoing Dial":
                O_D_counter += 1

    # for t in temp_arr:
    #     for d in data:
    #         if t[5] == d[5] and d[7] == "Outgoing Dial":
    #             incoming_arr.append({
    #                 "incoming": {
    #                     "from": t[5],
    #                     "to": t[6],
    #                     "startTime": t[2],
    #                     "endTime": t[3],
    #                     "direction": t[7]
    #                 },
    #                 "forwarding": {
    #                     "from": d[5],
    #                     "to": d[6],
    #                     "startTime": d[2],
    #                     "endTime": d[3],
    #                     "direction": d[7]
    #                 }
    #             })
    # for incoming in incoming_arr:
    #     pretty(incoming)
    print(f"total records: {counter}")
    print(f"total incoming: {incoming_counter}")
    print(f"total outgoing DIAL: {O_D_counter}")
    print(f"total outgoing API: {O_API_counter}")


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


# add outbound
if __name__ == '__main__':
    total_discrepancy_counter = 0
    for file in FILES:
        log.info(f"*****_{file}_*****")
        insights_file: str = get_file(file, FLEX_INSIGHTS)
        console_log_file: str = get_file(file, CONSOLE_LOGS)
        console_total_incoming(console_log_file)
        insights_total(insights_file)
        incoming_during_time(console_log_file, "13:15:00 AEDT 2021-03-09", "13:30:00 AEDT 2021-03-09")
        # total_discrepancy_counter += insights_15_min_gap(insights_file)
    log.error(f"Total Discrepancies from {FILES[0]} - {FILES[len(FILES) - 1]}: {total_discrepancy_counter}")
