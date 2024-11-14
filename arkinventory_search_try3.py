import re
import sys
import argparse

def extract_items(data, substring=None):
    pattern = r'\["h"\]\s*=\s*"([^"]*)".*?\["count"\]\s*=\s*(\d+)'
    items = []
    
    for character_data in re.finditer(r'\["([^"]+) - ([^"]+)"\]\s*=\s*{', data):
        character_name, realm = character_data.groups()
        for item_match in re.finditer(pattern, data[character_data.end():]):
            item_name = re.search(r'\[([^\]]+)\]', item_match.group(1))
            if item_name and (substring is None or substring.lower() in item_name.group(1).lower()):
                items.append({
                    'character_name': character_name,
                    'character_realm': realm,
                    'item_name': item_name.group(1),
                    'count': int(item_match.group(2))
                })
    return items

def main():
    parser = argparse.ArgumentParser(description="Process item data from a file.")
    parser.add_argument("input_file", help="Input file name")
    parser.add_argument("substring", nargs='?', help="Substring to match in item names")
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as file:
            data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)

    matching_items = extract_items(data, args.substring)

    print("character_name\tcharacter_realm\titem_name\tcount")
    for item in matching_items:
        print(f"{item['character_name']}\t{item['character_realm']}\t{item['item_name']}\t{item['count']}")

if __name__ == "__main__":
    main()
