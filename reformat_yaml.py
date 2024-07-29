import sys
import yaml
import textwrap
import re


def reformat_yaml(yaml_str):
    # Regular expression patterns to match 'description' and 'script' fields
    # These patterns look for 'description:' or 'script:' followed by a space and a quoted string
    # pattern = re.compile(r'(\b(description|script):\s+)(\'|\")(.+?)(\3)', re.DOTALL)
    pattern = re.compile(r"^(\s*)(description|script):\s+'((?:[^']|'')*)'", re.MULTILINE | re.DOTALL)


    # Function to format matched multi-line string
    def format_match(match):
        print(match)
        print(match.group(1))
        print(match.group(2))
        print(match.group(3))
        print(match.group(4))
        content = match.group(4).replace('\n', '\n  ')
        return f"{match.group(1)}|\n  {content}"

    # Apply the regular expressions
    # print(pattern.match(yaml_str))
    yaml_str = pattern.sub(format_match, yaml_str)

    return yaml_str

def main():
    text = sys.stdin.read()
    input_yaml = yaml.safe_load(text)
    dumped_yaml = yaml.dump(input_yaml, default_flow_style=False, sort_keys=False)
    formatted_yaml = reformat_yaml(dumped_yaml)
    # print("\nFormatted YAML:\n")
    # print(formatted_yaml)

if __name__ == "__main__":
    main()
