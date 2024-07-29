import sys

def srt_to_txt():
    for line in sys.stdin:
        # Ignore lines with just a newline, numbers, and timestamps
        if line.strip().isdigit() or '-->' in line or not line.strip():
            continue
        # Write the subtitle text to stdout
        sys.stdout.write(line)

if __name__ == "__main__":
    srt_to_txt()
