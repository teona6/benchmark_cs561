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
            ioengine=sync
            iodepth=1
            size=1z
            rw=read
            offset_increment=1z"

    # Loop to increment the number of jobs from 1 to 14
    for numjobs in 1 2 4 8 14; do
        echo "Running read experiment with $numjobs threads and block size $bs..."

        # Define the name of the output file based on the number of jobs and block size
        output_file="data/sr_${bs}_${numjobs}jobs.json"

        # Execute fio with the current number of jobs and save the output to a JSON file
        echo "$config" | fio --numjobs=$numjobs --output-format=json --output=$output_file -

        echo "Read experiment with $numjobs threads and block size $bs completed."
    done
done

echo "All read experiments completed. Results saved in the 'data' directory."

