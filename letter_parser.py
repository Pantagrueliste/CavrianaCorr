import os
import re
import csv
from lxml import etree

# Function to count words in a text
def count_words(text):
    # Clean the text and count words
    text = re.sub(r'\s+', ' ', text).strip()
    return len(text.split())

# Function to extract text from an element and its descendants
def get_text(element):
    if element is None:
        return ""
    text = element.text or ""
    for child in element:
        text += ' ' + get_text(child)
    if element.tail:
        text += ' ' + element.tail
    return text.strip()

# Function to count words in body text
def count_body_words(body_elem, ns):
    text_content = ""
    # Get text from paragraph-like elements
    for elem in body_elem.xpath('.//tei:p | .//tei:div | .//tei:opener | .//tei:closer', namespaces=ns):
        text_content += ' ' + get_text(elem)
    
    # Clean and count
    text_content = re.sub(r'\s+', ' ', text_content).strip()
    return count_words(text_content)

# Process a single XML file
def process_xml_file(file_path):
    try:
        # Parse XML
        tree = etree.parse(file_path)
        root = tree.getroot()
        
        # Define namespace
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        
        # Extract date
        date_elem = root.xpath('//tei:correspAction[@type="sent"]/tei:date', namespaces=ns)
        date = date_elem[0].get('when') if date_elem else ''
        
        # Extract place
        place_elem = root.xpath('//tei:correspAction[@type="sent"]/tei:placeName', namespaces=ns)
        place = get_text(place_elem[0]) if place_elem else ''
        
        # Extract sender
        sender_elem = root.xpath('//tei:correspAction[@type="sent"]/tei:persName', namespaces=ns)
        sender = get_text(sender_elem[0]) if sender_elem else ''
        
        # Extract receiver
        receiver_elem = root.xpath('//tei:correspAction[@type="received"]/tei:persName', namespaces=ns)
        receiver = get_text(receiver_elem[0]) if receiver_elem else ''
        
        # Extract repository
        repo_elem = root.xpath('//tei:msIdentifier/tei:repository', namespaces=ns)
        repository = get_text(repo_elem[0]) if repo_elem else ''
        
        # Extract idno
        idno_elem = root.xpath('//tei:msIdentifier/tei:idno', namespaces=ns)
        idno = get_text(idno_elem[0]) if idno_elem else ''
        
        # Extract locus
        locus_elem = root.xpath('//tei:msItem/tei:locus', namespaces=ns)
        locus = ''
        if locus_elem:
            from_attr = locus_elem[0].get('from')
            to_attr = locus_elem[0].get('to')
            if from_attr and to_attr:
                locus = f"{from_attr}-{to_attr}"
            else:
                locus = get_text(locus_elem[0])
        
        # Extract summary
        summary_elem = root.xpath('//tei:note[@type="summary"]', namespaces=ns)
        summary = get_text(summary_elem[0]) if summary_elem else ''
        
        # Get word count from body text
        body_elems = root.xpath('//tei:text/tei:body', namespaces=ns)
        word_count = 0
        if body_elems:
            word_count = count_body_words(body_elems[0], ns)
        
        return {
            'date': date,
            'place': place,
            'sender': sender,
            'receiver': receiver,
            'repository': repository,
            'idno': idno,
            'locus': locus,
            'word_count': word_count,
            'summary': summary
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Main function to process all XML files and create CSV
def main():
    # Files to exclude
    exclude_files = ['persNames.xml', 'placeNames.xml']
    
    # Directory with XML files
    letters_dir = 'letters'
    
    # List to store letter data
    letter_data = []
    
    # Process each XML file
    for filename in os.listdir(letters_dir):
        if filename.endswith('.xml') and filename not in exclude_files:
            file_path = os.path.join(letters_dir, filename)
            data = process_xml_file(file_path)
            if data:
                letter_data.append(data)
                print(f"Processed {filename}")
            else:
                print(f"Failed to process {filename}")
    
    # Sort by date
    letter_data.sort(key=lambda x: x['date'])
    
    # Write to CSV with UTF-8 encoding
    with open('letter_metadata.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['date', 'place', 'sender', 'receiver', 'repository', 'idno', 'locus', 'word_count', 'summary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in letter_data:
            writer.writerow(data)
    
    print(f"Created CSV with {len(letter_data)} letters")

if __name__ == "__main__":
    main()