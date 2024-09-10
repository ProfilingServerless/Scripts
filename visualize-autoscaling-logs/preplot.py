import os
import csv
import yaml

data_dict = {}

for folder_name in os.listdir("."):
    folder_path = os.path.join(".", folder_name)
    if folder_name == "plots":
        continue
    if os.path.isdir(folder_path):
        config_path = os.path.join(folder_path, 'config.yaml')
        with open(config_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)
            title = config_data.get('title', 'unknown')
        
        stats_dict = {}
        
        stats_path = os.path.join(folder_path, 'stats.csv')
        with open(stats_path, 'r') as stats_file:
            csv_reader = csv.DictReader(stats_file)
            for row in csv_reader:
                phase = row['phase']
                latency_values = (
                    int(row['latency_p50']),
                    int(row['latency_p80']),
                    int(row['latency_p90']),
                    int(row['latency_p99'])
                )
                stats_dict[phase] = latency_values
        
        data_dict[title] = stats_dict

sorted_titles = sorted(data_dict.keys(), key=lambda x: int(x.split('-')[1]))

file_mapping = {
    'decision': 'plots/decision.dat',
    'patch': 'plots/patch.dat',
    'scheduling': 'plots/schedule.dat',
    'startup': 'plots/startup.dat'
}

file_handles = {}

for phase, file_name in file_mapping.items():
    file_handles[phase] = open(file_name, 'w')

for title in sorted_titles:
    stats = data_dict[title]
    
    for phase, latency_values in stats.items():
        if phase in file_handles:
            file_handles[phase].write(f"{title} {latency_values[0]} {latency_values[1]} {latency_values[2]} {latency_values[3]}\n")

for handle in file_handles.values():
    handle.close()

