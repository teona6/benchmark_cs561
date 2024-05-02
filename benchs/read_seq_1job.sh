#!/bin/bash

# Create the results directory if it doesn't already exist
mkdir -p data

# Block sizes to test
block_sizes=(4k)

# Loop over block sizes
for bs in "${block_sizes[@]}"; do
    # Loop to increment the size parameter from 1 to 14 zones
    for zones in {1..14}; do
        echo "Running read experiment with block size $bs on $zones zones..."

        # Configuration for fio
        config="[global]
                zonemode=zbd
                job_max_open_zones=1
                direct=1
                buffered=0
                group_reporting=1
                filename=/dev/nvme0n2
                bs=$bs

                [read]
                numjobs=1
                ioengine=sync
                rw=read
                size=${zones}z"

        # Define the name of the output file based on the block size and number of zones
        output_file="data/sr_${bs}_1job_${zones}zones.json"

        # Execute fio with the current configuration and save the output to a JSON file
        echo "$config" | fio --output-format=json --output=$output_file -

        echo "Read experiment with block size $bs on $zones zones completed."
    done
done

echo "All read experiments completed. Results saved in the 'data' directory."
