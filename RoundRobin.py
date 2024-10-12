from prettytable import PrettyTable # pip install prettytable

def round_robin(processes, arrival_times, burst_times, quantum):
    n = len(processes)
    remaining_burst_times = burst_times.copy()
    waiting_times = [0] * n
    turnaround_times = [0] * n
    completion_times = [0] * n
    response_times = [-1] * n
    time_elapsed = 0
    
    while True:
        done = True
        for i in range(n):
            if remaining_burst_times[i] > 0 and arrival_times[i] <= time_elapsed:
                done = False
                if response_times[i] == -1:
                    response_times[i] = time_elapsed - arrival_times[i]
                
                if remaining_burst_times[i] > quantum:
                    time_elapsed += quantum
                    remaining_burst_times[i] -= quantum
                else:
                    time_elapsed += remaining_burst_times[i]
                    waiting_times[i] = time_elapsed - burst_times[i] - arrival_times[i]
                    completion_times[i] = time_elapsed
                    remaining_burst_times[i] = 0
        if done:
            break

    for i in range(n):
        turnaround_times[i] = completion_times[i] - arrival_times[i]

    return waiting_times, turnaround_times, completion_times, response_times


# Input data
processes = ['P1', 'P2', 'P3', 'P4']
arrival_times = [0, 2, 4, 6]
burst_times = [5, 15, 8, 6]
quantum = 4

# Function call
waiting_times, turnaround_times, completion_times, response_times = round_robin(processes, arrival_times, burst_times, quantum)

# Creating a table for output
table = PrettyTable()
table.field_names = ["Process", "Arrival Time", "Burst Time", "Completion Time", "Waiting Time", "Turnaround Time", "Response Time"]

# Adding rows to the table
for i in range(len(processes)):
    table.add_row([processes[i], arrival_times[i], burst_times[i], completion_times[i], waiting_times[i], turnaround_times[i], response_times[i]])

# Display the table
print(table)
