#!/usr/bin/python3
#!/usr/bin/python3
import sys
import re

# Check for the -q argument
quiet = False
if len(sys.argv) > 1 and sys.argv[1] == '-q':
    quiet = True
    pattern = sys.argv[2]
else:
    pattern = sys.argv[1]

# Compile the regex pattern
compiled_pattern = re.compile(pattern)

for line in sys.stdin:
    line = line.strip()
    match = compiled_pattern.search(line)
    if match:
        print('\t'.join(match.groups()))
    elif not quiet:
        print("No match")  # Print this if no match is found and -q is not used
