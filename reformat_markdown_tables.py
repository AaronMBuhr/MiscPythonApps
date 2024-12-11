import sys
import re

def parse_table_row(line):
    """Parse a markdown table row into cells, handling escaped pipes."""
    cells = []
    current_cell = ""
    i = 0
    while i < len(line):
        if line[i] == '\\' and i + 1 < len(line) and line[i + 1] == '|':
            current_cell += '|'
            i += 2
        elif line[i] == '|':
            if current_cell or cells:  # Skip leading pipe, but keep others
                cells.append(current_cell.strip())
                current_cell = ""
            i += 1
        else:
            current_cell += line[i]
            i += 1
    
    if current_cell:  # Add final cell if exists
        cells.append(current_cell.strip())
    
    return cells

def get_alignment(separator):
    """Determine column alignment based on separator cell"""
    separator = separator.strip()
    if separator.startswith(':') and separator.endswith(':'):
        return 'center'
    elif separator.startswith(':'):
        return 'left'
    elif separator.endswith(':'):
        return 'right'
    return 'left'  # default alignment

def format_cell(content, width, alignment):
    """Format a cell's content according to width and alignment"""
    content = content.strip()
    if alignment == 'right':
        return content.rjust(width)
    elif alignment == 'center':
        return content.center(width)
    else:  # left alignment
        return content.ljust(width)

def format_separator(width, alignment):
    """Format a separator cell with proper alignment markers"""
    if alignment == 'center':
        return ':' + '-' * (width - 2) + ':'
    elif alignment == 'right':
        return '-' * (width - 1) + ':'
    elif alignment == 'left':
        return ':' + '-' * (width - 1)
    return '-' * width

def format_table(table_lines):
    """Format a markdown table with proper alignment"""
    if not table_lines:
        return []
    
    # Parse the table into rows
    rows = [parse_table_row(line) for line in table_lines]
    
    # Ensure all rows have the same number of columns
    max_cols = max(len(row) for row in rows)
    rows = [row + [''] * (max_cols - len(row)) for row in rows]
    
    # Get column alignments from separator row
    separator_row = rows[1]
    alignments = [get_alignment(cell) for cell in separator_row]
    
    # Find maximum width needed for each column
    col_widths = [0] * max_cols
    for row in rows:
        for col in range(max_cols):
            cell_lines = row[col].split('<br>')
            max_line_length = max(len(line.strip()) for line in cell_lines)
            if max_line_length > col_widths[col]:
                col_widths[col] = max_line_length
    
    # Format each row
    formatted_lines = []
    for i, row in enumerate(rows):
        if i == 1:  # Separator row
            formatted_cells = [format_separator(width, align) 
                             for width, align in zip(col_widths, alignments)]
        else:
            # Handle multiline cells
            formatted_cells = []
            max_lines_in_cell = max(len(cell.split('<br>')) for cell in row)
            for line_idx in range(max_lines_in_cell):
                formatted_line_cells = []
                for cell, width, align in zip(row, col_widths, alignments):
                    cell_lines = cell.split('<br>')
                    if line_idx < len(cell_lines):
                        formatted_line_cells.append(format_cell(cell_lines[line_idx], width, align))
                    else:
                        formatted_line_cells.append(' ' * width)
                formatted_cells.append('| ' + ' | '.join(formatted_line_cells) + ' |')
            formatted_lines.extend(formatted_cells)
            continue
        
        formatted_line = '| ' + ' | '.join(formatted_cells) + ' |'
        formatted_lines.append(formatted_line)
    
    return formatted_lines

def is_table_row(line):
    """Determine if a line is a markdown table row"""
    line = line.strip()
    if not line:
        return False
    if '|' not in line:
        return False
    # Exclude lines that are code blocks or do not represent table rows
    if re.match(r'^\s*(```|---)', line):
        return False
    # A table row typically has at least one '|' not at the start or end
    if line.count('|') < 2:
        return False
    return True

def main():
    table_lines = []
    in_table = False
    
    for line in sys.stdin:
        line = line.rstrip('\n')
        
        # Check if line is part of a table
        if is_table_row(line):
            table_lines.append(line)
            in_table = True
        else:
            if in_table:
                # Table has ended, format it and print
                formatted_table = format_table(table_lines)
                print('\n'.join(formatted_table))
                in_table = False
                table_lines = []
            print(line)
    
    # Handle any remaining table at the end of input
    if table_lines:
        formatted_table = format_table(table_lines)
        print('\n'.join(formatted_table))

if __name__ == "__main__":
    main()
