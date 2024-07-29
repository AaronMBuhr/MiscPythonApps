#!/usr/bin/env python3

import sys
import re
import textwrap

def main():
    input_text = sys.stdin.read()

    # remove backslash
    input_text = input_text.replace("\\", "")
    
    # Regular expression to find all responses
    responses = re.findall(r'### response:(.*?)###', input_text, re.DOTALL | re.IGNORECASE)
    
    # Last response might not be followed by "###", handle separately
    last_response_match = re.search(r'### response:(.*)', input_text, re.DOTALL | re.IGNORECASE)
    if last_response_match:
        last_response = last_response_match.group(1)
        if last_response not in responses:
            responses.append(last_response)
    
    for response in responses:
        wrapped_response = textwrap.fill(response.strip(), width=79)
        print(f"\n\n{wrapped_response}\n\n")

if __name__ == "__main__":
    main()
