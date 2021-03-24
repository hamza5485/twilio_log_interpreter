from lib.logger import Logger
from lib.functions import get_file, load_file
import os

log = Logger(os.path.basename(__file__))

FILES = ["march_9", "march_10", "march_11", "march_12", "march_15", "march_16", "march_17", "march_18"]
PROJ_DIR = "15_second_intervals/"
FLEX_INSIGHTS = f"flex_insights"


def basic_calculations(file_name: str) -> int:
    data = load_file(file_name)
    daily_discrepancy_counter = 0
    for d in data:
        hoa = int(d[3]) + int(d[4]) + int(d[5])
        sla = int(d[6]) + int(d[7]) + int(d[8]) + int(d[9]) + int(d[10])
        diff_h_sla = int(d[3]) - sla
        if diff_h_sla > 0:
            # total_discrepancy_counter += 1
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
    log.warn(f"discrepancies on {file_name.split('flex_insights/')[1]} : {daily_discrepancy_counter}")
    return daily_discrepancy_counter

# add outbound
if __name__ == '__main__':
    total_discrepancy_counter = 0
    for file in FILES:
        log.info(f"*****_{file}_*****")
        file_name: str = get_file(file, FLEX_INSIGHTS)
        total_discrepancy_counter += basic_calculations(file_name)
    log.error(f"Total Discrepancies: {total_discrepancy_counter}")
