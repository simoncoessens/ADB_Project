# Benchmarking files


Folder structure is as follows: 
```
4.Project_Benchmarking_Files
│   ├── Benchmark_Azure_iteration
│   │   ├── SF=1
│   │   ├── SF=10
│   │   ├── SF=100
│   │   └── SF=1000
│   ├── Benchmark_GCloud_iteration
│   ├── Benchmark_local_iteration
│   └── README.md
```

Azure is split into different SF's because we wanted to run them on different instances for cost analyisis. 

To run the benchmark: 
	1. Open the file benchmark.py
	2. Set up the connection to the DB
	3. Set the scale factors
	4. Run the file