import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Initialize lists to hold the data
threads = []
bandwidth_means_write = []
latency_means_write = []
iops_means_write = []

bandwidth_means_read = []
latency_means_read = []
iops_means_read = []

# Assuming the files are named 'result_1_threads.json', 'result_read_1_threads.jso
results_dir = 'results'
for i in range(1, 15):
    # Write workload results
    file_name_write = f'result_{i}_threads.json'
    file_path_write = os.path.join(results_dir, file_name_write)
    with open(file_path_write, 'r') as f:
        data_write = json.load(f)
        # Append the mean values for bandwidth, latency, and IOPS for write
        bandwidth_means_write.append(data_write['jobs'][0]['write']['bw_mean'] / 1024)  # KB/s to MB/s
        latency_means_write.append(data_write['jobs'][0]['write']['lat_ns']['mean'] / 1000)  # ns to us
        iops_means_write.append(data_write['jobs'][0]['write']['iops_mean'])

    # Read workload results
    file_name_read = f'result_read_{i}_threads.json'
    file_path_read = os.path.join(results_dir, file_name_read)
    with open(file_path_read, 'r') as f:
        data_read = json.load(f)
        # Append the mean values for bandwidth, latency, and IOPS for read
        bandwidth_means_read.append(data_read['jobs'][0]['read']['bw_mean'] / 1024)  # KB/s to MB/s
        latency_means_read.append(data_read['jobs'][0]['read']['lat_ns']['mean'] / 1000)  # ns to us
        iops_means_read.append(data_read['jobs'][0]['read']['iops_mean'])

    # Append to the threads list only once
    if i not in threads:
        threads.append(i)

# Create a DataFrame
df_write = pd.DataFrame({
    'Threads': threads,
    'Bandwidth (MB/s)': bandwidth_means_write,
    'Latency (us)': latency_means_write,
    'IOPS': iops_means_write
})

df_read = pd.DataFrame({
    'Threads': threads,
    'Bandwidth (MB/s)': bandwidth_means_read,
    'Latency (us)': latency_means_read,
    'IOPS': iops_means_read
})

plt.figure(figsize=(10, 6))
plt.plot(df_write['Threads'], df_write['IOPS'], marker='o', color="blue", label='Write seq-wr-4k')
plt.plot(df_read['Threads'], df_read['IOPS'], marker='s', color="orange", label='Read seq-rd-4k')
plt.title('Threads vs Mean IOPS')
plt.xlabel('Number of Threads')
plt.ylabel('Mean IOPS')
plt.ylim(bottom=0)
plt.grid(True)
plt.legend(title='Workload')
plt.savefig('plots/iops_plot_combined.png')
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(df_write['Bandwidth (MB/s)'], df_write['Latency (us)'], marker='o', color="blue", label='Write seq-wr-4k')
plt.plot(df_read['Bandwidth (MB/s)'], df_read['Latency (us)'], marker='s', color="orange", label='Read seq-rd-4k')
plt.title('Latency vs Bandwidth')
plt.xlabel('Mean Bandwidth (MB/s)')
plt.ylabel('Mean Latency (us)')
plt.xlim(left=0)  # Set the x-axis to start at 0
plt.ylim(bottom=0)  # Set the y-axis to start at 0
plt.grid(True)
plt.legend(title='Workload')
plt.savefig('plots/latency_vs_bandwidth_plot_combined.png')
plt.show()

