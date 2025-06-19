import queue
from prettytable import PrettyTable
# see footnote 2. for the refernce used for this library

# given information for processes
Processes = [
	{"pid": "P1", "arrival_time": 0, "burst_time": 5},
    {"pid": "P2", "arrival_time": 1, "burst_time": 3},
    {"pid": "P3", "arrival_time": 2, "burst_time": 1}
]

completed = []

time_quantum = 2

rq = queue.Queue()

time_slice = 0

table = PrettyTable()

while len(completed) < len(Processes):
    # add the processes that have arrived to the ready queue
    for p in Processes:
        if p not in rq.queue and p["arrival_time"] <= time_slice and p not in completed:
                print(f"Adding {p['pid']} to the ready queue at time {time_slice}.")
                rq.put(p)
                
	# 
    if rq.empty():
        time_slice += 1
        continue
    
    current = rq.get()
    print(f"Time Slice: {time_slice}, Processing: {current['pid']}")
    # see footnote 2. for the ChatGPT convo on the method of adding time_remaining to the process
    if "time_remaining" not in current:
        current["time_remaining"] = current["burst_time"]
    
    if current["time_remaining"] > time_quantum:
        time_slice += time_quantum
        current["time_remaining"] -= time_quantum 
    else:
        time_slice += current["time_remaining"]
        current["completion_time"] = time_slice
        completed.append(current)
    
    # need to check again for processes that have arrived, before adding the current process back to the queue
    for p in Processes:
        if p is not current and p["arrival_time"] <= time_slice and p not in rq.queue and p not in completed:
                print(f"Adding {p['pid']} to the ready queue at time {time_slice}.")
                rq.put(p)
    
    if current not in completed:
        rq.put(current)

for p in completed:
    print(f"Process {p['pid']} completed at time {p['completion_time']}.")
    print(f"Turnaround time for {p['pid']}: {p['completion_time'] - p['arrival_time']}.")
    print(f"Waiting time for {p['pid']}: {p['completion_time'] - p['arrival_time'] - p['burst_time']}.")

table.field_names = ["Process ID", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"]
for p in completed:
    turnaround_time = p["completion_time"] - p["arrival_time"]
    waiting_time = turnaround_time - p["burst_time"]
    table.add_row([p["pid"], p["arrival_time"], p["burst_time"], p["completion_time"], turnaround_time, waiting_time])

print(table)