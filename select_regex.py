#!/usr/bin/python3
import sys
import re

# Initialize options
quiet = False
suppress_blank_lines = False

# Parse arguments
args = sys.argv[1:]
while args:
    if args[0] == '-q':
        quiet = True
        pattern = args[1]
        args = args[2:]
    elif args[0] == '-s':
        suppress_blank_lines = True
        args = args[1:]
    else:
        pattern = args[0]
        args = args[1:]

# Compile the regex pattern
compiled_pattern = re.compile(pattern)

for line in sys.stdin:
    line = line.strip()
    match = compiled_pattern.search(line)
    if match:
        result = '\t'.join(match.groups())
        if not (suppress_blank_lines and not result.strip()):
            print(result)
    elif not quiet:
        print("No match")  # Print this if no match is found and -q is not used
