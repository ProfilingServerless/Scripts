import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

e2e_latency = []
startup_latency = []
control_plane_latency = []
sandbox_latency = []
queue_latency = []
user_latency = []

dummy = 0

with open('pods.csv', mode='r', newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            first_seen = datetime.strptime(row[1], '%H:%M:%S.%f') if row[1] != '-1' else -1
            sandbox_start = datetime.strptime(row[2], '%H:%M:%S.%f') if row[2] != '-1' else -1
            sandbox_end = datetime.strptime(row[3], '%H:%M:%S.%f') if row[3] != '-1' else -1
            queue_start = datetime.strptime(row[4], '%H:%M:%S.%f') if row[4] != '-1' else -1
            user_start = datetime.strptime(row[5], '%H:%M:%S.%f') if row[5] != '-1' else -1
            e2e = round(float(row[6]), 3)
            observed_running = datetime.strptime(row[7][:15], '%H:%M:%S.%f') if len(row[7]) > 0 and row[7][:15] != '-1' else -1
            
            e2e_latency.append(e2e) if e2e != -1 else dummy + 1
            startup_latency.append(round(float((observed_running - first_seen).total_seconds()), 3)) if observed_running != -1 and first_seen != -1 else dummy + -1
            control_plane_latency.append(round(e2e - float((observed_running - first_seen).total_seconds()), 3)) if observed_running != -1 and first_seen != -1 and e2e != -1 else dummy + 1
            sandbox_latency.append(round(float((sandbox_end - sandbox_start).total_seconds()), 3)) if sandbox_start != -1 and sandbox_end != -1 else dummy + 1
            if queue_start > user_start:
                user_latency.append(round(float((queue_start - user_start).total_seconds()), 3)) if queue_start != -1 and user_start != -1 else dummy + 1
                queue_latency.append(round(float((observed_running - queue_start).total_seconds()),  3)) if queue_start != -1 and observed_running != -1 else dummy + 1
            else:
                queue_latency.append(round(float((user_start - queue_start).total_seconds()), 3)) if queue_start != -1 and user_start != -1 else dummy + 1
                user_latency.append(round(float((observed_running - user_start).total_seconds()), 3)) if user_start != -1 and observed_running != -1 else dummy + 1


print(e2e_latency)
print(startup_latency)
print(control_plane_latency)
print(sandbox_latency)
print(queue_latency)
print(user_latency)


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

plot_cdf('Pod Startup E2E Duration', sorted(e2e_latency), 'e2e_latency.png')
plot_cdf('', sorted(startup_latency), 'startup_latency.png')
plot_cdf('Control Plane Latency', sorted(control_plane_latency), 'control_plane_latency.png')
plot_cdf('Sandbox Creation Latency', sorted(sandbox_latency), 'sandbox_latency.png')

print(f"""
e2e: p50={np.percentile(sorted(e2e_latency), 50)} p80={np.percentile(sorted(e2e_latency), 80)} p90={np.percentile(sorted(e2e_latency), 90)}
startup_latency: p50={np.percentile(sorted(startup_latency), 50)} p80={np.percentile(sorted(startup_latency), 80)} p90={np.percentile(sorted(startup_latency), 90)}
control_plane_latency: p50={np.percentile(sorted(control_plane_latency), 50)} p80={np.percentile(sorted(control_plane_latency), 80)} p90={np.percentile(sorted(control_plane_latency), 90)}
sandbox_latency: p50={np.percentile(sorted(sandbox_latency), 50)} p80={np.percentile(sorted(sandbox_latency), 80)} p90={np.percentile(sorted(sandbox_latency), 90)}
""")

# plot_cdf('queue_latency', sorted(queue_latency), 'queue_latency.png')
# plot_cdf('user_latency', sorted(user_latency), 'user_latency.png')
