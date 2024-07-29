import sys
import re

def remove_comments(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression to match single line and multi-line comments
    pattern = r'//.*?$|/\*.*?\*/'
    # Use re.DOTALL to match across lines (for multi-line comments)
    # Use re.MULTILINE to allow start-of-line markers (^) to match after every newline
    cleaned_content = re.sub(pattern, '', content, flags=re.DOTALL | re.MULTILINE)

    return cleaned_content

if __name__ == "__main__":
    # Ensure the script is called with a file argument
    if len(sys.argv) != 2:
        print("Usage: python remove_cpp_comments.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = remove_comments(file_path)
    print(result)
