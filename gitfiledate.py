#!/usr/bin/env python3
import os
import argparse
from git import Repo

def list_files(directory, recursive):
    """List files in directory. Optionally, do it recursively."""
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                yield os.path.join(root, file)
    else:
        for file in os.listdir(directory):
            full_path = os.path.join(directory, file)
            if os.path.isfile(full_path):
                yield full_path

def get_latest_commit_info(repo, file_path):
    """Get latest commit info for the given file."""
    commits = list(repo.iter_commits(paths=file_path, max_count=1))
    if commits:
        commit = commits[0]
        return commit.hexsha, commit.message.strip(), commit.committed_datetime
    return None, None, None

def main():
    parser = argparse.ArgumentParser(description='List files with their last commit date and details in a git repository.')
    parser.add_argument('directory', type=str, help='Directory to list files from')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursively list files in subdirectories')
    parser.add_argument('-o', '--oneline', action='store_true', help='Output information in one line per file')
    
    args = parser.parse_args()
    
    # Attempt to initialize a git repository object.
    try:
        repo = Repo(args.directory, search_parent_directories=True)
    except Exception as e:
        print(f"Error initializing git repository: {e}")
        return
    
    for file_path in list_files(args.directory, args.recursive):
        relative_file_path = os.path.relpath(file_path, start=repo.working_tree_dir)
        commit_hash, commit_message, commit_date = get_latest_commit_info(repo, relative_file_path)
        
        if args.oneline:
            date_str = commit_date.strftime('%Y-%m-%d %H:%M:%S') if commit_date else ' ' * 19
            commit_hash_str = commit_hash if commit_hash else "(n/a)"
            print(f"{date_str}, {commit_hash_str}, {relative_file_path}")
        else:
            if commit_date:
                print(f"File: {relative_file_path}\nLatest Commit Date: {commit_date.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Commit Hash: {commit_hash}\nCommit Message: {commit_message}\n" + "-" * 80)
            else:
                print(f"File: {relative_file_path}\nLatest Commit: Not available\n" + "-" * 80)

if __name__ == "__main__":
    main()
