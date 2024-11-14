import argparse
import re

def parse_lua_file(file_path, search_str):
    character_data = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        
    # Regex pattern to find character names and their items in bags, bank, etc.
    char_pattern = re.compile(r'\["([^"]+)"\] = {\n?.*?location = {\n(.*?)\n}\n}', re.DOTALL)
    bag_pattern = re.compile(r'\["bag"\] = {\n(.*?)\n}', re.DOTALL)
    bank_pattern = re.compile(r'\["bank"\] = {\n(.*?)\n}', re.DOTALL)
    other_pattern = re.compile(r'\["([^"]+)"\] = {\n(.*?)\n}', re.DOTALL)

    for char_match in char_pattern.finditer(data):
        character_name = char_match.group(1)
        locations = char_match.group(2)
        
        for bag_match in bag_pattern.finditer(locations):
            if search_str.lower() in bag_match.group(1).lower():
                print(f"Character: {character_name}, Location: Bag, Item: {search_str}")
        
        for bank_match in bank_pattern.finditer(locations):
            if search_str.lower() in bank_match.group(1).lower():
                print(f"Character: {character_name}, Location: Bank, Item: {search_str}")
        
        for other_match in other_pattern.finditer(locations):
            if search_str.lower() in other_match.group(2).lower():
                print(f"Character: {character_name}, Location: {other_match.group(1)}, Item: {search_str}")

def main():
    parser = argparse.ArgumentParser(description='Parse ArkInventory.lua files to search for items.')
    parser.add_argument('lua_file', help='Path to the ArkInventory.lua file')
    parser.add_argument('search_str', help='Substring to search for in item names')
    args = parser.parse_args()
    
    parse_lua_file(args.lua_file, args.search_str)

if __name__ == '__main__':
    main()
