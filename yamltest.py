import sys
import yaml

def main():
    text = sys.stdin.read()
    input_yaml = yaml.safe_load(text)
    formatted_yaml = yaml.dump(input_yaml, default_flow_style=False, sort_keys=False, width=79)
    print(formatted_yaml)

if __name__ == "__main__":
    main()