from prettytable import PrettyTable
import matplotlib.pyplot as plt

def hrrn_scheduling(processes, arrival_times, burst_times):
    n = len(processes)
    waiting_times = [0] * n
    turnaround_times = [0] * n
    start_times = [-1] * n
    completion_times = [0] * n
    response_times = [-1] * n
    gantt_chart = []
    resource_allocation = []

    time_elapsed = 0
    completed = [False] * n
    completed_processes = 0

    while completed_processes < n:
        highest_ratio = -1
        selected_process = -1

        for i in range(n):
            if arrival_times[i] <= time_elapsed and not completed[i]:
                waiting_time = time_elapsed - arrival_times[i]
                response_ratio = (waiting_time + burst_times[i]) / burst_times[i]

                if response_ratio > highest_ratio:
                    highest_ratio = response_ratio
                    selected_process = i
                elif response_ratio == highest_ratio:
                    if arrival_times[i] < arrival_times[selected_process]:
                        selected_process = i

        if selected_process == -1:
            time_elapsed += 1
            continue

        start_times[selected_process] = time_elapsed
        response_times[selected_process] = time_elapsed - arrival_times[selected_process]
        time_elapsed += burst_times[selected_process]
        completion_times[selected_process] = time_elapsed
        turnaround_times[selected_process] = completion_times[selected_process] - arrival_times[selected_process]
        waiting_times[selected_process] = start_times[selected_process] - arrival_times[selected_process]

        completed[selected_process] = True
        completed_processes += 1
        gantt_chart.append((processes[selected_process], start_times[selected_process], completion_times[selected_process]))
        resource_allocation.append((processes[selected_process], start_times[selected_process], completion_times[selected_process]))

    return start_times, waiting_times, turnaround_times, completion_times, response_times, gantt_chart, resource_allocation


# Input data
processes = ['P1', 'P2', 'P3', 'P4', 'P5']
arrival_times = [0, 1, 2, 3, 4]
burst_times = [10, 1, 2, 1, 5]

# Function call
start_times, waiting_times, turnaround_times, completion_times, response_times, gantt_chart, resource_allocation = hrrn_scheduling(
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
        gnt.broken_barh([(start, end - start)], (process_index - 0.4, 0.8), facecolors=('tab:purple'))
        gnt.text(start + (end - start) / 2, process_index, process, ha='center', va='center', color='white', fontweight='bold')

    plt.title("Gantt Chart - Highest Response Ratio Next (HRRN) Scheduling")
    plt.show()

# Plotting the Gantt Chart
plot_gantt_chart(gantt_chart)
