#!/bin/bash

# Create the results directory if it doesn't already exist
mkdir -p data

# Block sizes to test
block_sizes=(4k)

# Loop over block sizes
for bs in "${block_sizes[@]}"; do
    # Configuration for fio
    config="[global]
            numjobs=1
            zonemode=zbd
            job_max_open_zones=1
            direct=1
            buffered=0
            group_reporting=1
            filename=/dev/nvme0n2
            bs=$bs

            [write]
            ioscheduler=mq-deadline
            ioengine=io_uring
            sqthread_poll=1
            rw=read
            size=1z"

    # Loop to increment the number of jobs from 1 to 14
    for (( depth=1; depth <= 64; depth*=2 )); do
        echo "Running experiment with 1 thread and block size $bs..."

        # Define the name of the output file based on the number of jobs and block size
        output_file="data/sr_${bs}_1job_${depth}depth.json"

        # Execute fio with the current number of jobs and save the output to a JSON file
        echo "$config" | fio --iodepth=$depth --output-format=json --output=$output_file -

        echo "Experiment with block size $bs and depth $depth completed."
    done
done

echo "All experiments completed. Results saved in the 'data' directory."

