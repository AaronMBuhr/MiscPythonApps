import requests
from bs4 import BeautifulSoup
import re
import argparse
from urllib.parse import urljoin, urlparse

def convert_url_to_filename(url):
    """Convert a URL to a filename by replacing periods with underscores and slashes with dashes."""
    # Remove protocol (http:// or https://)
    url = re.sub(r'^https?://', '', url)
    
    # Replace periods with underscores and slashes with dashes
    filename = url.replace('.', '_').replace('/', '-')
    
    # Add .md extension
    return f"{filename}.md"

def convert_table_to_markdown(table):
    markdown = []
    
    # Get all rows
    rows = table.find_all('tr')
    if not rows:
        return ''
    
    # Handle header row
    header = rows[0].find_all(['th', 'td'])
    if header:
        markdown.append('| ' + ' | '.join(cell.get_text().strip() for cell in header) + ' |')
        markdown.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
    
    # Handle data rows
    for row in rows[1:]:
        cells = row.find_all('td')
        if cells:
            markdown.append('| ' + ' | '.join(cell.get_text().strip() for cell in cells) + ' |')
    
    return '\n'.join(markdown)

def convert_html_to_markdown(html_content, base_url=''):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(['script', 'style']):
        script.decompose()
    
    markdown_lines = []
    
    # Convert title
    title = soup.find('title')
    if title:
        markdown_lines.append(f'# {title.get_text().strip()}\n')
    
    # Process body content
    body = soup.find('body')
    if body:
        for element in body.descendants:
            if element.name:
                # Headers
                if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    level = int(element.name[1])
                    markdown_lines.append(f"{'#' * level} {element.get_text().strip()}\n")
                
                # Paragraphs
                elif element.name == 'p':
                    markdown_lines.append(f"{element.get_text().strip()}\n\n")
                
                # Links
                elif element.name == 'a' and element.get('href'):
                    href = element.get('href')
                    # Make relative URLs absolute
                    if base_url and not href.startswith(('http://', 'https://')):
                        href = urljoin(base_url, href)
                    markdown_lines.append(f"[{element.get_text().strip()}]({href})")
                
                # Images
                elif element.name == 'img' and element.get('src'):
                    src = element.get('src')
                    alt = element.get('alt', '')
                    # Make relative URLs absolute
                    if base_url and not src.startswith(('http://', 'https://')):
                        src = urljoin(base_url, src)
                    markdown_lines.append(f"![{alt}]({src})")
                
                # Lists
                elif element.name == 'li':
                    # Check if it's part of an ordered list
                    if element.parent.name == 'ol':
                        markdown_lines.append(f"1. {element.get_text().strip()}\n")
                    else:
                        markdown_lines.append(f"* {element.get_text().strip()}\n")
                
                # Tables
                elif element.name == 'table':
                    markdown_lines.append(convert_table_to_markdown(element) + '\n\n')
    
    return '\n'.join(markdown_lines)

def main():
    parser = argparse.ArgumentParser(description='Convert HTML from URL to Markdown')
    parser.add_argument('url', help='URL of the webpage to convert')
    parser.add_argument('-o', '--output', help='Output markdown file path (optional)', default=None)
    
    args = parser.parse_args()
    
    try:
        # Generate output filename if not provided
        output_file = args.output if args.output else convert_url_to_filename(args.url)
        
        # Fetch the webpage
        response = requests.get(args.url)
        response.raise_for_status()
        
        # Convert to markdown
        markdown_content = convert_html_to_markdown(response.text, args.url)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Successfully converted {args.url} to {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    main()
    