from tabulate import tabulate

# Simulated Virtual Machines
vms = [
    {"name": "VM1", "mips": 500},
    {"name": "VM2", "mips": 1000},
    {"name": "VM3", "mips": 1500}
]

# Simulated Cloud Tasks
tasks = [
    {"name": "Task1", "length": 10000},
    {"name": "Task2", "length": 20000},
    {"name": "Task3", "length": 30000},
    {"name": "Task4", "length": 40000},
    {"name": "Task5", "length": 50000}
]

results = []

# Round Robin allocation
for i, task in enumerate(tasks):
    vm = vms[i % len(vms)]
    execution_time = task["length"] / vm["mips"]
    results.append([
        task["name"],
        task["length"],
        vm["name"],
        vm["mips"],
        round(execution_time, 2)
    ])
    # pip install tabulate

headers = [
    "Task",
    "Workload (MI)",
    "VM",
    "VM Capacity (MIPS)",
    "Execution Time"
]

print("\nCloud Resource Allocation using Round Robin\n")
print(tabulate(results, headers=headers, tablefmt="grid"))
