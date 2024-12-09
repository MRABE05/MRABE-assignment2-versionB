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

Description: A tool to inspect disk usage of directories with a graphical representation.

Date: 
'''

def parse_command_args():
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts", epilog="Copyright 2022")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Display sizes in a human-readable format (e.g., MB, GB).")
    parser.add_argument("target", nargs=1, help="Target directory to inspect.")
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

if __name__ == "__main__":
    args = parse_command_args()
    target_dir = args.target[0]
    bar_length = args.length
    
    # Test the implemented functions
    print(f"Testing 'call_du_sub' with target directory '{target_dir}'...")
    du_output = call_du_sub(target_dir)
    for line in du_output:
        print(line)
    
    print("\nTesting 'percent_to_graph'...")
    print(percent_to_graph(50, bar_length))  # Example test
