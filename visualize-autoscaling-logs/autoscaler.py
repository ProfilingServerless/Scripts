import os
import re
import json
from datetime import datetime


def parse_ticks_file(filepath):
    ticks = {}
    with open(filepath, 'r') as file:
        for line in file:
            deployment_name, timestamp = parse_ticks_line(line)
            if deployment_name in ticks:
                ticks[deployment_name].append(timestamp)
            else:
                ticks[deployment_name] = [timestamp]
    return ticks

def parse_ticks_line(line):
    log_dict = json.loads(line)
    deployment_name = log_dict["knative.dev/key"]
    timestamp = clean_timestamp(log_dict["timestamp"])
    return deployment_name, timestamp

def parse_decision_file(filepath):
    decisions = {}
    with open(filepath, 'r') as file:
        for line in file:
            deployment_name, timestamp, pod_count = parse_decision_line(line)
            if deployment_name in decisions:
                decisions[deployment_name].append((timestamp, pod_count))
            else:
                decisions[deployment_name] = [(timestamp, pod_count)]
    return decisions

def parse_decision_line(line):
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

def time_to_microseconds(time_str):
    time_obj = datetime.strptime(str(time_str), "%H:%M:%S.%f")
    microseconds = (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) * 1_000_000 + time_obj.microsecond
    return microseconds


def main():
    FILE_PATH = os.getenv("RESULT_PATH")
    ticks = parse_ticks_file(f'{FILE_PATH}/ticks')
    decisions = parse_decision_file(f'{FILE_PATH}/dec')
    patches = parse_patch_file(f"{FILE_PATH}/patch")
  
if __name__ == "__main__":
    main()
