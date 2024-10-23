import csv

FIRST_SEEN='~/outs/first_seen.txt'

# pod: first_seen,sandbox_start,sandbox_end,queue_start,user_start,observed_running,e2e_duration
pods = dict()

with open('~/outs/first_seen_clean.txt', mode='r', newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            pod = row[0]
            if pod in pods:
                pods[pod][0] = row[1]
            else:
                pods[pod] = [row[1], -1, -1, -1, -1, -1, -1]

with open('~/outs/strtup_duration_clean.txt', mode='r', newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            pod = row[0]
            if pod in pods:
                pods[pod][5], pods[pod][6] = row[1], row[2]
            else:
                pods[pod] = [-1, -1, -1, -1, -1, row[1], row[2]]

with open('~/outs/sandbox_clean.txt', mode='r', newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            pod = row[0]
            if row[2] == 'start':
                if pod in pods:
                    pods[pod][1] = row[1]

                else:
                    pods[pod] = [-1, row[1], -1, -1, -1, -1, -1] 
            else:
                if pod in pods:
                    pods[pod][2] = row[1]

                else:
                    pods[pod] = [-1, -1, row[1], -1, -1, -1, -1]]



with open('~/outs/container_clean.txt', mode='r', newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            pod = row[0]
            if row[2] == 'queue':
                if pod in pods:
                    pods[pod][3] = row[1]

                else:
                    pods[pod] = [-1, -1, -1, row[1], -1, -1, -1]
            else:
                if pod in pods:
                    pods[pod][4] = row[1]

                else:
                    pods[pod] = [-1, -1, -1, -1, row[1], -1, -1]


with open('~/outs/pods.txt') as f:
    writer = csv.writer(f)
    for k, v in pods.items():
        row = [k] + v
        writer.writerow([key, value])


