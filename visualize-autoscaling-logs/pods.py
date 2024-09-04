import os
import re
from datetime import datetime

def parse_creation_line(line):
    match = re.search(r'(\d{2}:\d{2}:\d{2}\.\d+).*Controller created pod.*pod="([^"]*)".*', line)
    if match:
        creation_time = match.group(1)
        pod_name = match.group(2)
        return pod_name, creation_time
    return None, None

def parse_bind_line(line):
    match = re.search(r'(\d{2}:\d{2}:\d{2}\.\d+).*Pod Scheduled Successfully.*For="([^"]*)".*', line)
    if match:
        scheduling_time = match.group(1)
        pod_name = match.group(2)
        return pod_name, scheduling_time
    return None, None
#
def parse_e2es_line(line):
    match = re.search(r'Observed pod startup duration.*pod="([^"]*)".*podStartE2EDuration="([\d\.]+)s".*observedRunningTime=".*(\d{2}:\d{2}:\d{2}\.\d+)\d{3}[^"]*".*watchObservedRunningTime=".*(\d{2}:\d{2}:\d{2}\.\d+)\d{3}[^"]*"', line)
    if match:
        pod_name = match.group(1)
        e2e_duration = str(int(float(match.group(2)) * 1e6))
        observed_running_time = match.group(3)
        watch_observed_running_time = match.group(4)
        return pod_name, e2e_duration, observed_running_time, watch_observed_running_time
    return None, None, None, None

def read_logs(filepath, parse_function):
    data = {}
    with open(filepath, 'r') as file:
        for line in file:
            pod_name, *values = parse_function(line)
            if pod_name:
                data[pod_name] = values
    return data

def format_time_string(time_str):
    dt = datetime.strptime(time_str, "%H:%M:%S.%f")
    return dt.time()

def time_to_microseconds(time_str):
    time_obj = datetime.strptime(str(time_str), "%H:%M:%S.%f")
    microseconds = (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) * 1_000_000 + time_obj.microsecond
    return microseconds


def main():
    FILE_PATH = os.getenv("RESULT_PATH")
    create_data = read_logs(f'{FILE_PATH}/create', parse_creation_line)
    bind_data = read_logs(f'{FILE_PATH}/bind', parse_bind_line)
    e2es_data = read_logs(f'{FILE_PATH}/e2es', parse_e2es_line)

    for pod_name in set(create_data) | set(bind_data) | set(e2es_data):
        creation_time = format_time_string(create_data.get(pod_name, ["N/A"])[0]) if pod_name in create_data else "N/A"
        scheduling_time = format_time_string(bind_data.get(pod_name, ["N/A"])[0]) if pod_name in bind_data else "N/A"
        e2e_duration, observed_time, watch_observed_time = e2es_data.get(pod_name, ("N/A", "N/A", "N/A"))
        
        print(f"{pod_name} {time_to_microseconds(creation_time)} {time_to_microseconds(scheduling_time)} {e2e_duration} {time_to_microseconds(observed_time)} {time_to_microseconds(watch_observed_time)}")


if __name__ == "__main__":
    main()
