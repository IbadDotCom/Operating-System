from prettytable import PrettyTable
import matplotlib.pyplot as plt

def fifo_scheduling(processes, arrival_times, burst_times):
    n = len(processes)
    waiting_times = [0] * n
    turnaround_times = [0] * n
    start_times = [-1] * n
    completion_times = [0] * n
    response_times = [-1] * n
    gantt_chart = []
    resource_allocation = []

    time_elapsed = 0

    for i in range(n):
        if arrival_times[i] > time_elapsed:
            time_elapsed = arrival_times[i]

        start_times[i] = time_elapsed
        response_times[i] = time_elapsed - arrival_times[i]
        time_elapsed += burst_times[i]
        completion_times[i] = time_elapsed
        turnaround_times[i] = completion_times[i] - arrival_times[i]
        waiting_times[i] = start_times[i] - arrival_times[i]
        
        gantt_chart.append((processes[i], start_times[i], completion_times[i]))
        resource_allocation.append((processes[i], start_times[i], completion_times[i]))

    return start_times, waiting_times, turnaround_times, completion_times, response_times, gantt_chart, resource_allocation


# Input data
processes = ['P1', 'P2', 'P3', 'P4', 'P5']
arrival_times = [0, 1, 2, 3, 4]
burst_times = [10, 1, 2, 1, 5]

# Function call
start_times, waiting_times, turnaround_times, completion_times, response_times, gantt_chart, resource_allocation = fifo_scheduling(
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
        gnt.broken_barh([(start, end - start)], (process_index - 0.4, 0.8), facecolors=('tab:green'))
        gnt.text(start + (end - start) / 2, process_index, process, ha='center', va='center', color='white', fontweight='bold')

    plt.title("Gantt Chart - FIFO Scheduling")
    plt.show()

# Plotting the Gantt Chart
plot_gantt_chart(gantt_chart)
