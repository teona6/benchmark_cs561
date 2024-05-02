import os
import json
import matplotlib.pyplot as plt
from itertools import chain

# Directory containing the results
results_dir = 'data'

# Lists to hold the data for each operation type
threads = [1, 2, 4, 6, 8, 10, 12, 14]  # Updated threads list
block_sizes = ['4k', '8k', '16k']
write_results = {}
read_results = {}
random_read_results = {}

# Initialize results dictionaries
for bs in block_sizes:
    write_results[bs] = []
    read_results[bs] = []
    random_read_results[bs] = []

# Process the result files
for bs in block_sizes:
    for thread in threads:
        sw_file_name = f"sw_{bs}_{thread}jobs.json"
        sr_file_name = f"sr_{bs}_{thread}jobs.json"
        rr_file_name = f"rr_{bs}_{thread}jobs.json"

        # Process sequential write files
        sw_file_path = os.path.join(results_dir, sw_file_name)
        if os.path.exists(sw_file_path):
            with open(sw_file_path, 'r') as file:
                data = json.load(file)
                write_results[bs].append(data['jobs'][0]['write'])

        # Process sequential read files
        sr_file_path = os.path.join(results_dir, sr_file_name)
        if os.path.exists(sr_file_path):
            with open(sr_file_path, 'r') as file:
                data = json.load(file)
                read_results[bs].append(data['jobs'][0]['read'])

        # Process random read files
        rr_file_path = os.path.join(results_dir, rr_file_name)
        if os.path.exists(rr_file_path):
            with open(rr_file_path, 'r') as file:
                data = json.load(file)
                random_read_results[bs].append(data['jobs'][0]['read'])

# Find the maximum IOPS and latency values
max_iops = max(max(job['iops_mean'] for job in res) for res in chain(write_results.values(), read_results.values(), random_read_results.values())) / 1000
max_latency = max(max(job['lat_ns']['mean'] for job in res) for res in chain(write_results.values(), read_results.values(), random_read_results.values())) / 1e6

# Increase by 10% for plotting
max_iops *= 1.10
max_latency *= 1.10

def plot_results(results, title, y_label, file_name, max_y_value):
    plt.figure(figsize=(10, 6))
    colors = {'4k': 'black', '8k': 'red', '16k': 'blue'}  # Color mapping for different block sizes

    # The x_positions should match the threads list
    x_positions = threads  # This includes all thread counts

    for bs, res in results.items():
        if 'IOPS' in y_label:
            values = [r['iops_mean'] / 1000 for r in res]
        else:
            values = [r['lat_ns']['mean'] / 1e6 for r in res]
        
        plt.plot(x_positions, values, label=f"{bs} Block Size", marker='o', color=colors[bs])

    plt.title(title, fontsize=14)
    plt.xlabel('Threads', fontsize=14)
    plt.ylabel(y_label, fontsize=14)

    # Set labels for the x-axis directly corresponding to thread counts
    plt.xticks(x_positions, [str(x) for x in threads], fontsize=12)

    plt.yticks(fontsize=12)
    plt.legend(loc='upper left', fontsize='large')
    
    # Apply horizontal grid lines and make them darker
    plt.grid(True, which='both', axis='y', color='grey', linestyle='-', linewidth=0.75)

    plt.ylim(0, max_y_value)
    plt.savefig(f"plots/{file_name}")
    plt.show()


os.makedirs('plots', exist_ok=True)
plot_results(write_results, 'Sequential Write IOPS vs Threads', 'IOPS (KIOPS)', 'seq_write_iops.png', max_iops)
plot_results(read_results, 'Sequential Read IOPS vs Threads', 'IOPS (KIOPS)', 'seq_read_iops.png', max_iops)
plot_results(random_read_results, 'Random Read IOPS vs Threads', 'IOPS (KIOPS)', 'random_read_iops.png', max_iops)
plot_results(write_results, 'Sequential Write Latency vs Threads', 'Latency (ms)', 'seq_write_latency.png', max_latency)
plot_results(read_results, 'Sequential Read Latency vs Threads', 'Latency (ms)', 'seq_read_latency.png', max_latency)
plot_results(random_read_results, 'Random Read Latency vs Threads', 'Latency (ms)', 'random_read_latency.png', max_latency)
