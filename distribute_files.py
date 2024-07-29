import os
import sys
import shutil

def create_and_distribute_files(base_name, files_per_dir):
    # Convert files_per_dir to integer
    files_per_dir = int(files_per_dir)
    
    # Get all files in the current directory
    all_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    # Sort files to ensure consistent distribution
    all_files.sort()
    
    # Calculate number of directories needed
    num_dirs = (len(all_files) + files_per_dir - 1) // files_per_dir
    
    for i in range(num_dirs):
        # Create directory name
        dir_name = f"{base_name}{(i+1):03d}"
        
        # Create directory
        os.makedirs(dir_name, exist_ok=True)
        
        # Calculate start and end indices for files to move
        start = i * files_per_dir
        end = min((i + 1) * files_per_dir, len(all_files))
        
        # Move files to the new directory
        for file in all_files[start:end]:
            shutil.move(file, os.path.join(dir_name, file))
        
        print(f"Created directory {dir_name} with {end - start} files")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <base_name> <files_per_directory>")
        sys.exit(1)
    
    base_name = sys.argv[1]
    files_per_dir = sys.argv[2]
    
    create_and_distribute_files(base_name, files_per_dir)