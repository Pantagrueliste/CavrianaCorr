import os
import fnmatch

# Directory containing the XML files
directory = 'letters'

# Text to search for
old_text = '<projectDesc><p>All places and persons are now referenced from authorityPlaces.xml and authorityPersons.xml</p></projectDesc></encodingDesc>'
# Replacement text
new_text = '<projectDesc><p>All places and persons are now referenced from placeNames.xml and persNames.xml</p></projectDesc></encodingDesc>'

# Iterate over all XML files in the directory
for root, _, files in os.walk(directory):
    for file in fnmatch.filter(files, '*.xml'):
        file_path = os.path.join(root, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the text
        if old_text in content:
            content = content.replace(old_text, new_text)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {file_path}")