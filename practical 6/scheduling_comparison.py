from tabulate import tabulate

# Simulated Virtual Machines
vms = [
    {"name": "VM1", "mips": 500},
    {"name": "VM2", "mips": 1000},
    {"name": "VM3", "mips": 1500}
]

# Simulated Cloud Tasks
tasks = [
    {"name": "Task1", "length": 60000},
    {"name": "Task2", "length": 10000},
    {"name": "Task3", "length": 10000},
    {"name": "Task4", "length": 60000},
    {"name": "Task5", "length": 10000}
]


def round_robin(tasks, vms):
    """Round Robin scheduling: assign tasks sequentially to VMs."""
    loads = [0] * len(vms)   # total workload on each VM
    results = []

    for i, task in enumerate(tasks):
        vm_index = i % len(vms)
        vm = vms[vm_index]

        start_time = loads[vm_index] / vm["mips"]
        execution_time = task["length"] / vm["mips"]
        finish_time = start_time + execution_time

        loads[vm_index] += task["length"]

        results.append([
            task["name"],
            vm["name"],
            round(start_time, 2),
            round(execution_time, 2),
            round(finish_time, 2)
        ])

    return results


def least_loaded(tasks, vms):
    """Least-Loaded scheduling: assign each task to the least loaded VM."""
    loads = [0] * len(vms)
    results = []

    for task in tasks:
        # Find VM with minimum current load / capacity
        vm_index = min(
            range(len(vms)),
            key=lambda i: loads[i] / vms[i]["mips"]
        )
        vm = vms[vm_index]

        start_time = loads[vm_index] / vm["mips"]
        execution_time = task["length"] / vm["mips"]
        finish_time = start_time + execution_time

        loads[vm_index] += task["length"]

        results.append([
            task["name"],
            vm["name"],
            round(start_time, 2),
            round(execution_time, 2),
            round(finish_time, 2)
        ])

    return results


# Run both scheduling algorithms
rr_results = round_robin(tasks, vms)
ll_results = least_loaded(tasks, vms)

headers = [
    "Task",
    "VM",
    "Start Time",
    "Execution Time",
    "Finish Time"
]

print("\nRound Robin Scheduling\n")
print(tabulate(rr_results, headers=headers, tablefmt="grid"))

print("\nLeast-Loaded Scheduling\n")
print(tabulate(ll_results, headers=headers, tablefmt="grid"))

# Makespan = maximum finish time
rr_makespan = max(row[4] for row in rr_results)
ll_makespan = max(row[4] for row in ll_results)

comparison = [
    ["Round Robin", rr_makespan],
    ["Least-Loaded", ll_makespan]
]

print("\nScheduling Performance Comparison\n")
print(tabulate(
    comparison,
    headers=["Scheduling Method", "Total Completion Time"],
    tablefmt="grid"
))

improvement = ((rr_makespan - ll_makespan) / rr_makespan) * 100
print(f"\nPerformance Improvement: {improvement:.2f}%")