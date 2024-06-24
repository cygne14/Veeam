# Two folders synchronization
This Python script synchronizes the contents of a source folder with a replica folder, ensuring the replica is an identical copy of the source. The synchronization is one-way, meaning changes in the source folder will be reflected in the replica folder, but not vice versa. The script is run periodically, and logs operations to both a file and the console.


# Prerequisites
- Python >= 3.11.


# Run
`python test_task.py --source <source_folder_path> --replica <replica_folder_path> [--log_file <log_file_path>] [--interval <interval_in_seconds>]`


# Arguments
- -s or --source: Required. Path to the source folder.
- -r or --replica: Required. Path to the replica folder.
- -l or --log_file: Optional. Path to the log file. If not provided, logging will be done only to the console.
- -i or --interval: Optional. Synchronization interval in seconds. Default is 1 second.


# Output
The script outputs log messages to the console and optionally to a log file. The log messages include:
- File creation, copying, and deletion operations.
- Errors encountered during the synchronization process.