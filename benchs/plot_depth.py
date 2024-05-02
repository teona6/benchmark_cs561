import os
import json
import matplotlib.pyplot as plt

def load_data(directory, operation, iodepths, offset=False):
    results = {}
    for depth in iodepths:
        suffix = '_off' if offset else ''
        file_name = f"{operation}_4k_1job_{depth}depth{suffix}.json"
        file_path = os.path.join(directory, file_name)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                results[depth] = data['jobs'][0]['write' if operation in ['sw', 'sw_off'] else 'read']
        except FileNotFoundError:
            print(f"File {file_name} not found.")
    return results

def plot_metric(sr_results, rr_results, sw_results, sw_offset_results, ylabel, plot_file):
    plt.figure(figsize=(10, 6))
    iodepths = sorted(set(sr_results.keys()) | set(rr_results.keys()) | set(sw_results.keys()) | set(sw_offset_results.keys()))
    indices = range(len(iodepths))

    sr_values = [sr_results.get(d, {'iops_mean': 0, 'clat_ns': {'mean': 0}})['iops_mean'] / 1000 if 'IOPS' in ylabel else sr_results.get(d, {'iops_mean': 0, 'clat_ns': {'mean': 0}})['clat_ns']['mean'] / 1e6 for d in iodepths]
    rr_values = [rr_results.get(d, {'iops_mean': 0, 'clat_ns': {'mean': 0}})['iops_mean'] / 1000 if 'IOPS' in ylabel else rr_results.get(d, {'iops_mean': 0, 'clat_ns': {'mean': 0}})['clat_ns']['mean'] / 1e6 for d in iodepths]
    sw_values = [sw_results.get(d, {'iops_mean': 0, 'clat_ns': {'mean': 0}})['iops_mean'] / 1000 if 'IOPS' in ylabel else sw_results.get(d, {'iops_mean': 0, 'clat_ns': {'mean': 0}})['clat_ns']['mean'] / 1e6 for d in iodepths]
    sw_off_values = [sw_offset_results.get(d, {'iops_mean': 0, 'clat_ns': {'mean': 0}})['iops_mean'] / 1000 if 'IOPS' in ylabel else sw_offset_results.get(d, {'iops_mean': 0, 'clat_ns': {'mean': 0}})['clat_ns']['mean'] / 1e6 for d in iodepths]

    plt.plot(indices, sr_values, 'o-', color='red', label='sr-4k')
    plt.plot(indices, rr_values, 'o-', color='orange', label='rr-4k')
    plt.plot(indices, sw_values, 'o-', color='blue', label='sw-4k')
    plt.plot(indices, sw_off_values, 'x-', color='blue', label='sw-4k-offset')

    plt.title(f"{ylabel} vs I/O Depth")
    plt.xlabel("I/O Depth")
    plt.ylabel(ylabel)
    plt.xticks(indices, [str(d) for d in iodepths])
    plt.legend()
    plt.grid(True)
    plt.ylim(bottom=0)
    plt.savefig(f"plots/{plot_file}")
    plt.show()

results_dir = 'data'
iodepths = [2**i for i in range(0, 7)]  # From 1 to 64, doubling

sr_results = load_data(results_dir, 'sr', iodepths)
rr_results = load_data(results_dir, 'rr', iodepths)
sw_results = load_data(results_dir, 'sw', iodepths)
sw_offset_results = load_data(results_dir, 'sw', iodepths, offset=True)

plot_metric(sr_results, rr_results, sw_results, sw_offset_results, 'IOPS (KIOPS)', 'iops_vs_depth.png')
plot_metric(sr_results, rr_results, sw_results, sw_offset_results, 'Latency (ms)', 'latency_vs_depth.png')
