#!/usr/bin/env python3

import subprocess
import sys
import argparse

'''
OPS445 Assignment 2 - Winter 2022
Program: duim.py 
Author: "Student Name"
The python code in this file (duim.py) is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script analyzes the contents of a directory using the `du` command,
generates a report with bar charts to show disk usage, and displays the output in
either raw bytes or human-readable format.

Date: 
'''

def parse_command_args():
    """
    Set up argparse to handle command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="DU Improved -- See Disk Usage Report with bar charts",
        epilog="Copyright 2022"
    )
    parser.add_argument(
        "-l", "--length", type=int, default=20,
        help="Specify the length of the graph. Default is 20."
    )
    parser.add_argument(
        "-H", "--human-readable", action="store_true",
        help="Display sizes in a human-readable format (e.g., M, G)."
    )
    parser.add_argument(
        "target", type=str, nargs=1,
        help="Specify the target directory to analyze."
    )
    return parser.parse_args()

def call_du_sub(location):
    """
    Takes the target directory as an argument and returns a list of strings
    returned by the command `du -d 1 location`.
    """
    try:
        result = subprocess.Popen(
            ["du", "-d", "1", location],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = result.communicate()
        if result.returncode != 0:
            print(f"Error: {stderr.decode()}", file=sys.stderr)
            return []
        return [line.decode().strip() for line in stdout.splitlines()]
    except Exception as e:
        print(f"Error calling du: {e}", file=sys.stderr)
        return []

def percent_to_graph(percent, total_chars):
    """
    Returns a string: eg. '##  ' for 50 if total_chars == 4.
    """
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100.")
    num_equals = int(round((percent / 100) * total_chars))
    return "=" * num_equals + " " * (total_chars - num_equals)

def create_dir_dict(alist):
    """
    Gets a list from call_du_sub, returns a dictionary which has the full
    directory name as the key, and the number of bytes in the directory as the value.
    """
    dir_dict = {}
    for entry in alist:
        try:
            size, path = entry.split(None, 1)  # Split on the first whitespace
            dir_dict[path] = int(size)
        except ValueError:
            continue
    return dir_dict

def convert_to_human_readable(size):
    """
    Converts a size in bytes to a human-readable string.
    """
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} P"

if __name__ == "__main__":
    args = parse_command_args()
    target_dir = args.target[0]
    length = args.length
    human_readable = args.human_readable

    # Call du and process the results
    raw_du_output = call_du_sub(target_dir)
    if not raw_du_output:
        sys.exit(1)
    
    dir_dict = create_dir_dict(raw_du_output)

    # Calculate total size
    total_size = sum(dir_dict.values())
    print(f"Total: {convert_to_human_readable(total_size) if human_readable else total_size} ({target_dir})")

    # Print formatted output
    for path, size in dir_dict.items():
        percent = (size / total_size) * 100 if total_size > 0 else 0
        graph = percent_to_graph(percent, length)
        if human_readable:
            size_str = convert_to_human_readable(size)
        else:
            size_str = f"{size} B"
        print(f"{percent:5.1f}% [{graph}] {size_str:10} {path}")
