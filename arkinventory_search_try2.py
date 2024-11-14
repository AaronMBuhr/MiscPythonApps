import sys
import re

def parse_arkinventory(file_path, search_substring):
    with open(file_path, 'r') as file:
        data = file.read()
    
    # Extract character data
    characters = re.findall(r'ARKINVDB\["(.+?)"\]', data)
    
    for character in characters:
        # Extract items for each character
        items = re.findall(r'\[(\d+)\] = {(.+?)}', data)
        for item_id, item_data in items:
            if search_substring.lower() in item_data.lower():
                location = re.search(r'h = (\d+)', item_data)
                if location:
                    loc_type = "Bag" if int(location.group(1)) < 100 else "Bank"
                    print(f"Character: {character}, Item ID: {item_id}, Location: {loc_type}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <arkinventory.lua file> <search substring>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    search_substring = sys.argv[2]
    parse_arkinventory(file_path, search_substring)
