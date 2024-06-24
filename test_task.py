import argparse
import logging
import time
from functions import synchronize, test_path


if __name__ == "__main__":
    # parsing the arguments
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("-s", "--source", required=True, help="Source folder path")
    parser.add_argument("-r", "--replica", required=True, help="Replica folder path")
    parser.add_argument("-l", "--log_file", default=None, help="Log file path")
    parser.add_argument("-i", "--interval", type=float, default=1, help="Synchronization interval in seconds")
    
    args = parser.parse_args()
    
    test_path(args.source)
    test_path(args.replica)

    if args.interval < 0:
        raise ValueError("Interval must be non-negative number.")

    if args.log_file:
        test_path(args.log_file)

    # setting the logger
    logger = logging.getLogger("Folder synchronization")
    logger.setLevel(logging.INFO)  
    
    if args.log_file is not None:
        file_handler = logging.FileHandler(args.log_file, mode="a")
    else:
        file_handler = logging.FileHandler("log_file", mode="w")

    console_handler = logging.StreamHandler()

    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)

    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


    # call the synchronization function
    while True:
        synchronize(args.source, args.replica, logger)
        time.sleep(args.interval)
