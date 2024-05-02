# Experiments

Use the following scripts to run the performance benchmarks

- For sequential write, random read, sequential read inter zone experiments run the following scripts respectively `write_seq.sh`, `read_rand.sh`, `read_seq.sh`
- For intra zone experiments run `write_io_depth.sh`, `read_io_depth.sh`, `read_io_depth_seq.sh`
- Use `write_seq_off.sh` for sequential write experiment without the reset for inter zone experiment. For intra zone experiment without reset interference run `write_io_depth_off.sh`