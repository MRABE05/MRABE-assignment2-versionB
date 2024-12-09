#!/usr/bin/env python3

import subprocess
import sys
import argparse

'''
OPS445 Assignment 2 - Fall 2024
Program: duim.py 
Author: "Ma. Therese Dominique Rabe"
The python code in this file (duim.py) is original work written by
Ma. Therese Dominique Rabe. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: A tool to inspect disk usage of directories with a graphical representation.

Date: 
'''

def parse_command_args():
    """
    Set up argparse to handle command-line arguments.
    Returns the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="DU Improved -- See Disk Usage Report with bar charts",
        epilog="Copyright 202X"
    )
    parser.add_argument(
        "-l", "--length", type=int, default=20,
        help="Specify the length of the graph. Default is 20."
    )
    parser.add_argument(
        "-H", "--human-readable", action="store_true",
        help="Print sizes in human-readable format (e.g., 1K, 23M, 2G)."
    )
    parser.add_argument(
        "target", nargs="?", default=".", 
        help="The directory to scan. Defaults to the current directory."
    )
    return parser.parse_args()

def percent_to_graph(percent, total_chars):
    """
    Converts a percentage into a bar graph representation.
    
    Arguments:
    - percent: A number between 0 and 100 indicating the percentage to represent.
    - total_chars: The total length of the bar graph.
    
    Returns:
    A string representation of the bar graph.
    """
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100.")
    
    num_filled = int(round((percent / 100) * total_chars))
    return "=" * num_filled + " " * (total_chars - num_filled)

def call_du_sub(location):
    """
    Takes the target directory as an argument and returns a list of strings
    returned by the command `du -d 1 location`, ignoring permission errors.
    """
    try:
        result = subprocess.Popen(
            ["du", "-d", "1", location],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = result.communicate()
        
        # Ignore "Permission denied" errors
        if result.returncode != 0:
            # Print only stderr output if there are permission issues
            stderr_output = stderr.decode()
            if "Permission denied" in stderr_output:
                pass  # Ignore permission errors
            else:
                print(f"Error: {stderr_output}", file=sys.stderr)
            return []
        
        return [line.decode().strip() for line in stdout.splitlines()]
    except Exception as e:
        print(f"Error calling du: {e}", file=sys.stderr)
        return []

def create_dir_dict(du_output):
    """
    Converts the output of `du` into a dictionary.

    :param du_output: List of strings, each containing size and directory path.
    :return: Dictionary with paths as keys and sizes as integer values.
    """
    dir_dict = {}
    for line in du_output:
        try:
            size, path = line.split('\t')
            dir_dict[path.strip()] = int(size.strip())
        except ValueError as e:
            print(f"Skipping malformed line: {line} ({e})")
    return dir_dict

def human_readable(size):
    """
    Convert a byte size to a human-readable format without importing extra modules.
    """
    units = ['B', 'K', 'M', 'G', 'T']
    for unit in units:
        if size < 1024.0:
            return f"{size:.2f}{unit}"
        size /= 1024.0
    return f"{size:.2f}P"  # In case it exceeds petabytes

def validate_directory(directory):
    """
    Validate if the directory exists using subprocess.
    """
    try:
        # Run a simple command to check if the directory exists and is accessible
        result = subprocess.check_output(['test', '-d', directory])
        return True  # If no error, directory is valid
    except subprocess.CalledProcessError:
        return False  # Directory does not exist or is inaccessible

if __name__ == "__main__":
    args = parse_command_args()
    target_dir = args.target
    bar_length = args.length

    # Validate the target directory using subprocess
    if not validate_directory(target_dir):
        print(f"Error: {target_dir} is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    # Call call_du_sub to get disk usage information
    du_output = call_du_sub(target_dir)
    if not du_output:
        print("Error: No output from du command.", file=sys.stderr)
        sys.exit(1)

    # Convert du output to a dictionary
    dir_dict = create_dir_dict(du_output)

    # Calculate total size of the target directory
    total_size = dir_dict.get(target_dir, sum(dir_dict.values()))

    # Print results with bar graph
    for path, size in dir_dict.items():
        if path == target_dir:
            continue  # Skip graph for the target directory itself
        percent = (size / total_size) * 100
        graph = percent_to_graph(percent, bar_length)
        size_display = f"{size}" if not args.human_readable else human_readable(size)
        print(f"{percent:6.2f}% | {graph} | {size_display} | {path}")

    # Example test
    print(f"Processed {len(dir_dict)} directories from {target_dir}.")
