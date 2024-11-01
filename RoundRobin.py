from prettytable import PrettyTable
import matplotlib.pyplot as plt

def round_robin(processes, arrival_times, burst_times, quantum):
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

    while True:
        done = True
        for i in range(n):
            if remaining_times[i] > 0 and arrival_times[i] <= time_elapsed:
                done = False
                if start_times[i] == -1:
                    start_times[i] = time_elapsed
                
                if response_times[i] == -1:
                    response_times[i] = time_elapsed - arrival_times[i]
                
                if remaining_times[i] > quantum:
                    gantt_chart.append((processes[i], time_elapsed, time_elapsed + quantum))
                    resource_allocation.append((processes[i], time_elapsed, time_elapsed + quantum))
                    time_elapsed += quantum
                    remaining_times[i] -= quantum
                else:
                    gantt_chart.append((processes[i], time_elapsed, time_elapsed + remaining_times[i]))
                    resource_allocation.append((processes[i], time_elapsed, time_elapsed + remaining_times[i]))
                    time_elapsed += remaining_times[i]
                    waiting_times[i] = start_times[i] - arrival_times[i]
                    completion_times[i] = time_elapsed
                    remaining_times[i] = 0

        if done:
            break

    for i in range(n):
        turnaround_times[i] = completion_times[i] - arrival_times[i]

    return start_times, waiting_times, turnaround_times, completion_times, response_times, gantt_chart, resource_allocation


# Input data
processes = ['P1', 'P2', 'P3', 'P4', 'P5']
arrival_times = [0, 1, 2, 3, 4]
burst_times = [10, 1, 2, 1, 5]
quantum = 2

# Function call
start_times, waiting_times, turnaround_times, completion_times, response_times, gantt_chart, resource_allocation = round_robin(
    processes, arrival_times, burst_times, quantum
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
    fig, gnt = plt.subplots(figsize=(11, 5))
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
        gnt.broken_barh([(start, end - start)], (process_index - 0.4, 0.8), facecolors=('tab:blue'))
        gnt.text(start + (end - start) / 2, process_index, process, ha='center', va='center', color='white', fontweight='bold')

    plt.title("Gantt Chart - Round Robin Scheduling")
    plt.show()

# Plotting the Gantt Chart
plot_gantt_chart(gantt_chart)
