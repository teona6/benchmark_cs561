import os
import json
import matplotlib.pyplot as plt

def load_data(directory, operation, jobs_range):
    results = {'reset': {}, 'no_reset': {}}
    for numjobs in jobs_range:
        reset_file_name = f"{operation}_4k_{numjobs}jobs.json"
        offset_file_name = f"{operation}_4k_{numjobs}jobs_off.json"
        for key, file_name in {'reset': reset_file_name, 'no_reset': offset_file_name}.items():
            file_path = os.path.join(directory, file_name)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    results[key][numjobs] = data['jobs'][0]['write']
            except FileNotFoundError:
                print(f"File {file_name} not found.")
    return results

def plot_metric(results, ylabel, plot_file):
    plt.figure(figsize=(10, 6))
    for key, res in results.items():
        numjobs = sorted(res.keys())
        values = [res[j]['iops_mean'] / 1000 if 'IOPS' in ylabel else res[j]['clat_ns']['mean'] / 1e6 for j in numjobs]
        label = f"sw-4k-{key}"
        marker = 'x' if key == 'no_reset' else 'o'
        plt.plot(numjobs, values, marker=marker, label=label)

    plt.title(f"{ylabel} vs Jobs")
    plt.xlabel("Number of Jobs")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.ylim(bottom=0)  # Ensure y-axis starts at 0
    plt.savefig(f"plots/{plot_file}")
    plt.show()

results_dir = 'data'
jobs_range = [1, 2, 4, 8, 14]
os.makedirs('plots', exist_ok=True)

all_results = load_data(results_dir, 'sw', jobs_range)
plot_metric(all_results, 'IOPS (KIOPS)', 'sw_4k_iops_jobs.png')
plot_metric(all_results, 'Latency (ms)', 'sw_4k_latency_jobs.png')
