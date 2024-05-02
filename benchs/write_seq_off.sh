#!/bin/bash

# Create the results directory if it doesn't already exist
mkdir -p data

# Block sizes to test
block_sizes=(4k)

# Start offset at 500
offset=500

# Loop over block sizes
for bs in "${block_sizes[@]}"; do
    # Loop to increment the number of jobs from 1 to 14
    for numjobs in 1 2 4 8 14; do
        echo "Running experiment with $numjobs threads, block size $bs, and offset $offset..."

        # Configuration for fio
        config="[global]
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
                iodepth=1
                rw=write
                size=1z
                offset=${offset}z
                offset_increment=1z"

        # Define the name of the output file based on the number of jobs, block size, and offset
        output_file="data/sw_${bs}_${numjobs}jobs_off.json"

        # Execute fio with the current number of jobs and save the output to a JSON file
        echo "$config" | fio --numjobs=$numjobs --output-format=json --output=$output_file -

        echo "Experiment with $numjobs threads, block size $bs, and offset $offset completed."

        # Increment offset by 20 for the next run
        offset=$((offset + 20))
    done
done

echo "All experiments completed. Results saved in the 'data' directory."
