#!/bin/bash

# Create the results directory if it doesn't already exist
mkdir -p data

# Block sizes to test
block_sizes=(4k)

# Starting offset
offset=100

# Loop over block sizes
for bs in "${block_sizes[@]}"; do
    # Loop to increment the iodepth from 1 to 64, doubling each time
    for (( depth=1; depth <= 64; depth*=2 )); do
        echo "Running experiment with 1 thread, block size $bs, and depth $depth..."

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
                offset=${offset}z

                [write]
                ioscheduler=mq-deadline
                ioengine=io_uring
                sqthread_poll=1
                rw=write
                size=1z"

        # Define the name of the output file based on the block size and depth
        output_file="data/sw_${bs}_1job_${depth}depth_off.json"

        # Execute fio with the current configuration and save the output to a JSON file
        echo "$config" | fio --iodepth=$depth --output-format=json --output=$output_file -

        echo "Experiment with block size $bs and depth $depth completed."

        # Increment offset for the next run
        ((offset++))
    done
done

echo "All experiments completed. Results saved in the 'data' directory."
