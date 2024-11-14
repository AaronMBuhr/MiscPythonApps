#!/usr/bin/env python3

import re
import sys
import textwrap

def process_sections(input_stream):
    text = input_stream.read()
    # Regular expression to match the content after "### response:\"
    pattern = r'###\s*response:\s*\\\n(.*?)(?=\\\n|###\s*instruction:|\Z)'
    
    # Find all matches using the pattern
    matches = re.findall(pattern, text, re.DOTALL)
    
    # Format the captured sections and add an extra newline after each
    formatted_texts = [textwrap.fill(t.strip(), width=79) for t in matches]
    
    # Output the result
    sys.stdout.write("\n\n".join(formatted_texts) + "\n\n")

if __name__ == "__main__":
    process_sections(sys.stdin)
