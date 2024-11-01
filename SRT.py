from prettytable import PrettyTable
import matplotlib.pyplot as plt

def shortest_remaining_time(processes, arrival_times, burst_times):
    n = len(processes)
    remaining_times = burst_times.copy()
    waiting_times = [0] * n
    turnaround_times = [0] * n
    start_times = [-1] * n
    completion_times = [0] * n
    response_times = [-1] * n
    time_elapsed = 0
    gantt_chart = []
    resource_allocation = []
    completed_processes = 0

    while completed_processes < n:
        shortest = -1
        shortest_time = float('inf')
        
        for i in range(n):
            if arrival_times[i] <= time_elapsed and remaining_times[i] > 0:
                if remaining_times[i] < shortest_time:
                    shortest_time = remaining_times[i]
                    shortest = i
                elif remaining_times[i] == shortest_time:
                    if arrival_times[i] < arrival_times[shortest]:
                        shortest = i

        if shortest == -1:
            time_elapsed += 1
            continue

        if start_times[shortest] == -1:
            start_times[shortest] = time_elapsed
        
        if response_times[shortest] == -1:
            response_times[shortest] = time_elapsed - arrival_times[shortest]

        resource_allocation.append((processes[shortest], time_elapsed, time_elapsed + 1))
        gantt_chart.append((processes[shortest], time_elapsed, time_elapsed + 1))
        
        remaining_times[shortest] -= 1
        time_elapsed += 1

        if remaining_times[shortest] == 0:
            completion_times[shortest] = time_elapsed
            turnaround_times[shortest] = completion_times[shortest] - arrival_times[shortest]
            waiting_times[shortest] = start_times[shortest] - arrival_times[shortest]
            completed_processes += 1

    return start_times, waiting_times, turnaround_times, completion_times, response_times, gantt_chart, resource_allocation


# Input data
processes = ['P1', 'P2', 'P3', 'P4', 'P5']
arrival_times = [0, 1, 2, 3, 4]
burst_times = [10, 1, 2, 1, 5]

# Function call
start_times, waiting_times, turnaround_times, completion_times, response_times, gantt_chart, resource_allocation = shortest_remaining_time(
    processes, arrival_times, burst_times
)

# Creating a table for output
table = PrettyTable()
table.field_names = [
    "Process", "Arrival Time", "Execution Time", "Start Time", "Wait Time", 
    "Completion Time", "Turnaround Time", "Response Time"
]

# Adding rows to the table
for i in range(len(processes)):
    table.add_row([
        processes[i], arrival_times[i], burst_times[i], start_times[i], 
        waiting_times[i], completion_times[i], turnaround_times[i], response_times[i]
    ])

# Display the table
print("Process Table:")
print(table)

# Resource Allocation Table
resource_table = PrettyTable()
resource_table.field_names = ["Process", "Start Time", "End Time"]

# Adding rows to the resource allocation table
for alloc in resource_allocation:
    resource_table.add_row([alloc[0], alloc[1], alloc[2]])

print("\nResource Allocation Table:")
print(resource_table)

# Gantt Chart plotting
def plot_gantt_chart(gantt_chart):
    fig, gnt = plt.subplots(figsize=(12, 5))
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')

    # Setting limits on x and y axis
    gnt.set_xlim(0, max([end for _, _, end in gantt_chart]) + 2)
    gnt.set_ylim(0, len(processes) + 1)

    # Setting gridlines on the chart
    gnt.grid(True)

    # Set ticks on y-axis
    gnt.set_yticks([i + 1 for i in range(len(processes))])
    gnt.set_yticklabels(processes)

    # Plot each process
    for process, start, end in gantt_chart:
        process_index = processes.index(process) + 1
        gnt.broken_barh([(start, end - start)], (process_index - 0.4, 0.8), facecolors=('tab:orange'))
        gnt.text(start + (end - start) / 2, process_index, process, ha='center', va='center', color='white', fontweight='bold')

    plt.title("Gantt Chart - Shortest Remaining Time Scheduling")
    plt.show()

# Plotting the Gantt Chart
plot_gantt_chart(gantt_chart)
