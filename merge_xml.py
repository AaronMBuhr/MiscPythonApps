import xml.etree.ElementTree as ET
import sys

def merge_xml_elements(target, source):
    """
    Merges source elements into the target, avoiding duplicates.
    """
    for src_child in source:
        # Find matching elements in the target
        match = None
        for tgt_child in target:
            if src_child.tag == tgt_child.tag and src_child.attrib == tgt_child.attrib:
                match = tgt_child
                break
        
        if match is not None:
            # Recursively merge children if they exist
            merge_xml_elements(match, src_child)
        else:
            # If no match is found, append the source child to the target
            target.append(src_child)

def merge_xml_files(file1, file2):
    # Parse the XML files
    tree1 = ET.parse(file1)
    root1 = tree1.getroot()

    tree2 = ET.parse(file2)
    root2 = tree2.getroot()

    # Merge the second root into the first
    merge_xml_elements(root1, root2)

    # Output the merged XML
    merged_tree = ET.ElementTree(root1)
    ET.dump(merged_tree)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_xml.py <file1.xml> <file2.xml>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    merge_xml_files(file1, file2)
