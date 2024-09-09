import os
import re
import json
import csv
from datetime import datetime

def parse_decision_file(filepath):
    durations = {}
    with open(filepath, 'r') as file:
        for line in file:
            deployment_name, timestamp, duration, pod_count = parse_decision_line(line)
            if deployment_name in durations:
                durations[deployment_name].append((timestamp, duration, pod_count))
            else:
                durations[deployment_name] = [(timestamp, duration, pod_count)]
    return durations 

def parse_decision_line(line):
    log_dict = json.loads(line)
    deployment_name = log_dict["knative.dev/key"]
    timestamp = clean_timestamp(log_dict["timestamp"])
    duration, pod_count = extract_decision_duration(log_dict["message"])
    return deployment_name, timestamp, duration, pod_count

def extract_decision_duration(message):
    pattern = r'Decided in (\d+\.\d+)µs scale (\d+)[^"]*'
    match = re.search(pattern, message)
    if match:
        return int(float(match.group(1))), int(match.group(2))
    return None, None

def parse_dec_file(filepath):
    decisions = {}
    with open(filepath, 'r') as file:
        for line in file:
            deployment_name, timestamp, pod_count = parse_dec_line(line)
            if deployment_name in decisions:
                decisions[deployment_name].append((timestamp, pod_count))
            else:
                decisions[deployment_name] = [(timestamp, pod_count)]
    return decisions

def parse_dec_line(line):
    log_dict = json.loads(line)
    deployment_name = log_dict["knative.dev/key"]
    timestamp = clean_timestamp(log_dict["timestamp"])
    pod_count = extract_pod_count(log_dict["message"])
    
    return deployment_name, timestamp, pod_count

def extract_pod_count(message):
    pattern = r'PodCount=(\d+)'
    match = re.search(pattern, message)
    if match:
        return int(match.group(1))
    return None

def parse_patch_file(filepath):
    patches = {}
    with open(filepath, 'r') as file:
        for line in file:
            deployment_name, timestamp, patch_scale = parse_patch_line(line)
            if deployment_name in patches:
                patches[deployment_name].append((timestamp, patch_scale))
            else:
                patches[deployment_name] = [(timestamp, patch_scale)]
    return patches 

def parse_patch_line(line):
    log_dict = json.loads(line)
    deployment_name = log_dict["knative.dev/key"]
    timestamp = clean_timestamp(log_dict["timestamp"])
    patch_scale = extract_patch_scale(log_dict["message"])

    return deployment_name, timestamp, patch_scale


def extract_patch_scale(message):
    pattern = r'Successfully scaled to (\d+)'
    match = re.search(pattern, message)
    if match:
        return int(match.group(1))
    return None

def clean_timestamp(timestamp):
    dt = datetime.fromisoformat(timestamp)
    return time_to_microseconds(dt.strftime('%H:%M:%S.%f'))

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

def get_patch_duration(decisions, patches):
    durations = {}
    for deployment in patches:
        durations[deployment] = []
        for timestamp, scale in patches[deployment]:
            tmp = list(filter(lambda d: d[0] < timestamp and d[2] == scale, decisions[deployment]))
            if len(tmp) > 0:
                decision_timestamp = max(tmp, key=lambda x: x[0])
                durations[deployment].append(timestamp - decision_timestamp[0])
    return durations
            
def get_schedule_durations(create_data, bind_data):
    durations = {}
    for pod in bind_data:
        if pod in create_data:
            durations[pod] = time_to_microseconds(bind_data[pod][0]) - time_to_microseconds(create_data[pod][0])
    return durations

def get_startup_durations(bind_data, e2es_data):
    durations = {}
    for pod in e2es_data:
        if pod in bind_data:
            durations[pod] = time_to_microseconds(e2es_data[pod][1]) - time_to_microseconds(bind_data[pod][0])
    return durations

def save_pods(filepath, schedule_duratinos, startup_durations):
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['pod', 'scheduling_duration', 'startup_duration'])
        
        for pod in schedule_duratinos:
            scheduling_duration = schedule_duratinos[pod]
            startup_duration = startup_durations[pod] if pod in startup_durations else "??"
            writer.writerow([pod, scheduling_duration, startup_duration])

def save_decisions(filepath, decisions):
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['deployment', 'decision_duration'])
        
        for deployment in decisions:
            for _, duration, _ in decisions[deployment]:
                writer.writerow([deployment, duration])
    
def save_patches(filepath, apply_durations):
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['deployment', 'patch_duration'])
        
        for deployment in apply_durations:
            for duration in apply_durations[deployment]:
                writer.writerow([deployment, duration])

def main():
    FILE_PATH = os.getenv("RESULT_PATH")
    
    decisions = parse_decision_file(f'{FILE_PATH}/decision')
    patches = parse_patch_file(f"{FILE_PATH}/patch")
    
    create_data = read_logs(f'{FILE_PATH}/create', parse_creation_line)
    bind_data = read_logs(f'{FILE_PATH}/bind', parse_bind_line)
    e2es_data = read_logs(f'{FILE_PATH}/e2es', parse_e2es_line)
    
    print("====L1====")
    for deployment in decisions:
        for _, duration, _ in decisions[deployment]:
            print(duration, end=' ')

    print()
    print("====L2====")
    apply_durations = get_patch_duration(decisions, patches)
    for deployment in apply_durations:
        for duration in apply_durations[deployment]:
            print(duration, end=' ')

    print()
    print("====L3====")
    schedule_duratinos = get_schedule_durations(create_data, bind_data)
    for pod in schedule_duratinos:
        print(schedule_duratinos[pod], end=' ')

    print()
    print("====L4====")
    startup_durations = get_startup_durations(bind_data, e2es_data)
    for pod in startup_durations:
        print(startup_durations[pod])
   
    save_decisions(f'{FILE_PATH}/clean/decisions.csv', decisions)
    save_patches(f'{FILE_PATH}/clean/patches.csv', apply_durations)
    
    save_pods(f'{FILE_PATH}/clean/pods.csv', schedule_duratinos, startup_durations) 
     
if __name__ == "__main__":
    main()
