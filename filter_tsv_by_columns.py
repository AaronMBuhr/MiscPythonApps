import sys

def filter_tsv(num_columns):
    for line in sys.stdin:
        columns = line.strip().split('\t')
        if len(columns) == num_columns:
            print(line.strip())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <number_of_columns>")
        sys.exit(1)
    
    try:
        num_columns = int(sys.argv[1])
    except ValueError:
        print("Error: Please provide a valid integer for the number of columns.")
        sys.exit(1)
    
    filter_tsv(num_columns)
