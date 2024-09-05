import csv
import numpy as np
import os

def read_csv_column(filepath, column_index):
    values = []
    with open(filepath, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header
        for row in csv_reader:
            values.append(int(row[column_index]))
    return values

def calculate_percentiles(data):
    p50 = int(np.percentile(data, 50))
    p80 = int(np.percentile(data, 80))
    p90 = int(np.percentile(data, 90))
    p99 = int(np.percentile(data, 99))
    return p50, p80, p90, p99

def main():
    FILE_PATH = os.getenv("RESULT_PATH")

    decision_durations = read_csv_column(f'{FILE_PATH}/clean/decisions.csv', 1)
    patch_durations = read_csv_column(f'{FILE_PATH}/clean/patches.csv', 1)
    scheduling_durations = read_csv_column(f'{FILE_PATH}/clean/pods.csv', 1)
    startup_durations = read_csv_column(f'{FILE_PATH}/clean/pods.csv', 2)
    
    decision_p50, decision_p80, decision_p90, decision_p99 = calculate_percentiles(decision_durations)
    patch_p50, patch_p80, patch_p90, patch_p99 = calculate_percentiles(patch_durations)
    scheduling_p50, scheduling_p80, scheduling_p90, scheduling_p99 = calculate_percentiles(scheduling_durations)
    startup_p50, startup_p80, startup_p90, startup_p99 = calculate_percentiles(startup_durations)
    
    with open(f'{FILE_PATH}/stats.csv', mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['phase', 'latency_p50', 'latency_p80', 'latency_p90', 'latency_p99'])
        csv_writer.writerow(['decision', decision_p50, decision_p80, decision_p90, decision_p99])
        csv_writer.writerow(['patch', patch_p50, patch_p80, patch_p90, patch_p99])
        csv_writer.writerow(['scheduling', scheduling_p50, scheduling_p80, scheduling_p90, scheduling_p99])
        csv_writer.writerow(['startup', startup_p50, startup_p80, startup_p90, startup_p99])

if __name__ == "__main__":
    main()
