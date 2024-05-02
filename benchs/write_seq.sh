#!/bin/bash

# Create the results directory if it doesn't already exist
mkdir -p data

# Block sizes to test
block_sizes=(4k 8k 16k)

# Loop over block sizes
for bs in "${block_sizes[@]}"; do
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
            offset_increment=1z"

    # Loop to increment the number of jobs from 1 to 14
    for numjobs in 1 2 4 6 8 10 12 14; do
        echo "Running experiment with $numjobs threads and block size $bs..."
        
        # Reset zones before each experiment
        blkzone reset /dev/nvme0n2
        if [ $? -ne 0 ]; then
            echo "Zone reset failed. Aborting experiment."
            exit 1
        fi

        # Define the name of the output file based on the number of jobs and block size
        output_file="data/sw_${bs}_${numjobs}jobs.json"

        # Execute fio with the current number of jobs and save the output to a JSON file
        echo "$config" | fio --numjobs=$numjobs --output-format=json --output=$output_file -

        echo "Experiment with $numjobs threads and block size $bs completed."
    done
done

echo "All experiments completed. Results saved in the 'data' directory."

