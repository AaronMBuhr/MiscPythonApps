import os

def write_files_to_markdown(directory):
    with open('code.md', 'w') as markdown_file:
        for filename in os.listdir(directory):
            if filename.endswith('.h') or filename.endswith('.cpp'):
                # Write filename as header
                markdown_file.write(f'# {filename}\n\n')

                # Write code block with file content
                with open(os.path.join(directory, filename), 'r') as code_file:
                    code_content = code_file.read()
                    markdown_file.write('```cpp\n')
                    markdown_file.write(code_content)
                    markdown_file.write('\n```\n\n')
                    
if __name__ == "__main__":
    current_directory = os.getcwd()
    write_files_to_markdown(current_directory)

