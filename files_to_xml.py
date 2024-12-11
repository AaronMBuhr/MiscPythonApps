import sys
import glob

def main():
    # Print XML opening tag
    print("<xml>")
    
    # Create a list to store all matching files
    all_files = []
    
    # Process each argument from command line
    for pattern in sys.argv[1:]:
        # Expand wildcards and add to file list
        matches = glob.glob(pattern)
        if matches:
            all_files.extend(matches)
        else:
            print(f"\nWarning: No files match pattern '{pattern}'", file=sys.stderr)
    
    # Process each matching file
    for filename in sorted(all_files):  # Sort for consistent output
        try:
            # Read the file contents
            with open(filename, 'r') as f:
                contents = f.read()
            
            # Print blank line, then file tag with contents
            print()
            print(f'<file name="{filename}">')
            print(contents, end='')
            print('</file>')
            
        except FileNotFoundError:
            print(f"\nError: File '{filename}' not found.", file=sys.stderr)
        except IOError as e:
            print(f"\nError reading '{filename}': {e}", file=sys.stderr)
    
    # Print final blank line and closing XML tag
    print()
    print("</xml>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python files_to_xml.py file1|wildcard [file2|wildcard ...]", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python files_to_xml.py file.txt", file=sys.stderr)
        print("  python files_to_xml.py *.txt", file=sys.stderr)
        print("  python files_to_xml.py data/*.xml config/*.xml", file=sys.stderr)
        sys.exit(1)
    main()
