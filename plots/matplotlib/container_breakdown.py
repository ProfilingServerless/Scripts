import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np




import csv
from datetime import datetime

# Function to calculate the difference in seconds between two timestamps
def calculate_time_difference(start, end):
    start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
    end_time = datetime.fromisoformat(end.replace('Z', '+00:00'))
    difference = (end_time - start_time).total_seconds()
    return round(difference, 3)

queue_proxy_differences = []
user_container_differences = []

with open('cs.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        container_type, start_time, end_time = row
        time_difference = calculate_time_difference(start_time, end_time)
        
        if container_type == "queue-proxy":
            queue_proxy_differences.append(time_difference)
        elif container_type == "user-container":
            user_container_differences.append(time_difference)


def plot_cdf(title, data, file_name):
    plt.title(title)
    plt.xlabel('latency(s)')
    plt.ylabel('Cumulative Probability')
    
    cdf = np.arange(1, len(data) + 1) / len(data)
    plt.plot(data, cdf, marker='.', linestyle='-', color='b')
    plt.fill_between(data, cdf, color='lightblue', alpha=0.5) 
    plt.grid(True)
    plt.savefig(file_name, format='png')
    plt.show()

# plot_cdf('e2e_latency', sorted(e2e_latency), 'e2e_latency.png')
# plot_cdf('startup_latency', sorted(startup_latency), 'startup_latency.png')
# plot_cdf('control_plane_latency', sorted(control_plane_latency), 'control_plane_latency.png')
# plot_cdf('sandbox_latency', sorted(sandbox_latency), 'sandbox_latency.png')
plot_cdf('Queue Proxy Startup Latecny', sorted(queue_proxy_differences), 'queue_latency.png')
plot_cdf('User Container Startup Latency', sorted(user_container_differences), 'user_latency.png')

print(f"""
queue_latency: p50={np.percentile(sorted(queue_proxy_differences), 50)} p80={np.percentile(sorted(queue_proxy_differences), 80)} p90={np.percentile(sorted(queue_proxy_differences), 90)}
user_latency: p50={np.percentile(sorted(user_container_differences), 50)} p80={np.percentile(sorted(user_container_differences), 80)} p90={np.percentile(sorted(user_container_differences), 90)}
""")

