import re
import sys
import argparse

def extract_items(file_path, substring=None):
    items = []
    character_info = {}
    in_item_data = False
    item_name = None
    item_count = None
    
    with open(file_path, 'r') as file:
        for line in file:
            # print(line)
            
            if '["player_id"]' in line:
                # # print(f"player_id: {line}")
                match = re.search(r'\["player_id"\] = "(\S+) - (\S+)"', line)
                # # print(match)
                if match:
                    character_info['character_name'], character_info['character_realm'] = match.groups()
                    # # print(character_info)
            elif '["loc_id"]' in line:
                in_item_data = True
            elif in_item_data:
                if '["count"]' in line:
                    # # print(f"count: {line}")
                    try:
                        item_count = re.search(r'\["count"\]\s*=\s*(\d+)', line)
                        if item_count:
                            item_count = item_count.group(1)
                        else:
                            item_count = None
                    except AttributeError:
                        print(f"Error: No match found for item count:")
                        print({
                                    "character_name": character_info['character_name'], 
                                    "character_realm": character_info['character_realm'], 
                                    "item_name": item_name, 
                                    "count": item_count
                                })
                        exit(0)
                elif '["h"]' in line:
                    # # print(f"h: {line}")
                    # item_name = re.search(r'\["h"\]\s*=\s*"([^"]*)"', line)
                    # ["h"] = "|cff00ccff|Hitem:122250::::::::26:258:::1:5805:::::Player-5-0DB34E75:|h[Tattered Dreadmist Mask]|h|r"
                    parts = line.split('|')
                    if len(parts) > 3:
                        # # print(parts[3])
                        # exit(0)
                        try:
                            item_name = re.search(r'h\[([^|\]]+)', parts[3]).group(1).strip()
                        except AttributeError:
                            if 'h[]' in line:
                                item_name = None
                            else:
                                print(f"Error: No match found for item name in line: {line}")
                                exit(0)
                        # # print(item_name)  # Output: Tattered Dreadmist Mask                    
                        # exit(0)
                elif '}' in line:
                    # # print("end of item")
                    try:
                        if item_name and item_count:
                            if substring is None \
                            or substring == "" \
                            or substring.lower() in item_name.lower():
                                # # print(f"character_name: {character_info['character_name']}")
                                # # print(f"character_realm: {character_info['character_realm']}")
                                # exit(0)
                                # print("found")
                                items.append({
                                    "character_name": character_info['character_name'], 
                                    "character_realm": character_info['character_realm'], 
                                    "item_name": item_name, 
                                    "count": item_count
                                })
                    except AttributeError:
                        print(f"Error: No match found for item name:")
                        print({
                                    "character_name": character_info['character_name'], 
                                    "character_realm": character_info['character_realm'], 
                                    "item_name": item_name, 
                                    "count": item_count
                                })
                        exit(0)
                    in_item_data = False
                    item_name = None
                    item_count = None
                    
    
    return items

def main():
    parser = argparse.ArgumentParser(description="Process item data from a file.")
    parser.add_argument("input_file", help="Input file name")
    parser.add_argument("substring", nargs='?', help="Substring to match in item names")
    args = parser.parse_args()

    try:
        matching_items = extract_items(args.input_file, args.substring)
    except FileNotFoundError:
        # # print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)

    # # print("character_name\tcharacter_realm\titem_name\tcount")
    for item in matching_items:
        print(f"{item['character_name']}\t{item['character_realm']}\t{item['item_name']}\t{item['count']}")

if __name__ == "__main__":
    main()
