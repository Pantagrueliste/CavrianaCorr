#!/usr/bin/env python3
"""
scripts/add_incomplete_section.py
Adds a dedicated incomplete entities section to authority files while preserving existing structure.
"""

from pathlib import Path
from lxml import etree
import sys

# Configuration
PERS_FILE = Path("letters/persNames.xml")
PLACE_FILE = Path("letters/placeNames.xml")
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def parse_file(file_path):
    """Parse TEI file and return root element."""
    try:
        doc = etree.parse(file_path)
        return doc.getroot()
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def add_incomplete_section(file_path, entity_type, incomplete_entities):
    """Add incomplete entities section to file."""
    root = parse_file(file_path)
    if root is None:
        return False
    
    # Find the list element
    list_elem = root.find(f".//tei:list{entity_type.capitalize()}", namespaces=NS)
    if list_elem is None:
        print(f"Could not find list element in {file_path}")
        return False
    
    # Add section header for incomplete entities
    incomplete_header = etree.Comment(" INCOMPLETE ENTITIES (needs research) ")
    list_elem.append(incomplete_header)
    
    # Add placeholder entities for known undefined references
    for entity_id, entity_data in incomplete_entities.items():
        if entity_type == "person":
            person = etree.Element("{http://www.tei-c.org/ns/1.0}person")
            person.set("{http://www.w3.org/XML/1998/namespace}id", entity_id)
            
            pers_name = etree.SubElement(person, "{http://www.tei-c.org/ns/1.0}persName")
            pers_name.text = entity_data.get("name", "UNKNOWN")
            
            if entity_data.get("sex"):
                sex_elem = etree.SubElement(person, "{http://www.tei-c.org/ns/1.0}sex")
                sex_elem.set("value", entity_data["sex"])
            
            if entity_data.get("occupation"):
                occ_elem = etree.SubElement(person, "{http://www.tei-c.org/ns/1.0}occupation")
                occ_elem.text = entity_data["occupation"]
            
            # Add note about missing data
            note_elem = etree.SubElement(person, "{http://www.tei-c.org/ns/1.0}note")
            note_elem.text = "Entity needs research and completion"
            
            list_elem.append(person)
        
        elif entity_type == "place":
            place = etree.Element("{http://www.tei-c.org/ns/1.0}place")
            place.set("{http://www.w3.org/XML/1998/namespace}id", entity_id)
            
            place_name = etree.SubElement(place, "{http://www.tei-c.org/ns/1.0}placeName")
            place_name.set("type", "modern")
            place_name.text = entity_data.get("name", "UNKNOWN")
            
            if entity_data.get("country"):
                country_elem = etree.SubElement(place, "{http://www.tei-c.org/ns/1.0}placeName")
                country_elem.set("type", "country")
                country_elem.text = entity_data["country"]
            
            # Add note about missing data
            note_elem = etree.SubElement(place, "{http://www.tei-c.org/ns/1.0}note")
            note_elem.text = "Entity needs coordinates and authority references"
            
            list_elem.append(place)
    
    # Write back to file
    try:
        doc = etree.ElementTree(root)
        doc.write(file_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)
        print(f"✅ Added incomplete section to {file_path}")
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False

def main():
    """Main function to add incomplete entity sections."""
    print("Adding incomplete entity sections...")
    
    # Known undefined person entities
    undefined_persons = {
        "pers-bourbon-conde": {
            "name": "Louis I de Bourbon, Prince of Condé",
            "sex": "male",
            "occupation": "Prince of Condé"
        },
        "pers-pontefice": {
            "name": "The Pope",
            "sex": "male",
            "occupation": "Pope"
        },
        "pers-cesare": {
            "name": "Cesare d'Este",
            "sex": "male",
            "occupation": "Noble"
        },
        "pers-este-card": {
            "name": "Este Cardinal",
            "sex": "male",
            "occupation": "Cardinal"
        },
        "pers-guadagni": {
            "name": "Guadagni family member",
            "occupation": "Noble"
        },
        "pers-lorraine-h": {
            "name": "Henry of Lorraine",
            "sex": "male",
            "occupation": "Noble"
        },
        "pers-papazzone-g": {
            "name": "Pope (papazzone)",
            "sex": "male",
            "occupation": "Pope"
        },
        "pers-sanseverino-g": {
            "name": "Sanseverino family member",
            "occupation": "Noble"
        },
        "pers-taxis-c": {
            "name": "Taxi family member",
            "occupation": "Noble"
        }
    }
    
    # Known undefined place entities
    undefined_places = {
        "place-blois": {
            "name": "Blois",
            "country": "France"
        },
        "place-sancerre": {
            "name": "Sancerre",
            "country": "France"
        },
        "place-bourbon": {
            "name": "Bourbon",
            "country": "France"
        },
        "place-europe": {
            "name": "Europe",
            "country": "Europe"
        },
        "place-ferrara": {
            "name": "Ferrara",
            "country": "Italy"
        },
        "place-gatinais": {
            "name": "Gâtinais",
            "country": "France"
        },
        "place-genova": {
            "name": "Genoa",
            "country": "Italy"
        },
        "place-guyenne": {
            "name": "Guyenne",
            "country": "France"
        },
        "place-lille": {
            "name": "Lille",
            "country": "France"
        },
        "place-limousin": {
            "name": "Limousin",
            "country": "France"
        },
        "place-lyon": {
            "name": "Lyon",
            "country": "France"
        },
        "place-navarre": {
            "name": "Navarre",
            "country": "Spain/France"
        },
        "place-orleans": {
            "name": "Orléans",
            "country": "France"
        },
        "place-venezia": {
            "name": "Venice",
            "country": "Italy"
        }
    }
    
    # Add incomplete sections
    if not add_incomplete_section(PERS_FILE, "person", undefined_persons):
        print("❌ Failed to add incomplete section to persNames.xml")
        return 1
    
    if not add_incomplete_section(PLACE_FILE, "place", undefined_places):
        print("❌ Failed to add incomplete section to placeNames.xml")
        return 1
    
    print("✅ Incomplete entity sections added successfully!")
    print(f"   Added {len(undefined_persons)} incomplete person entities")
    print(f"   Added {len(undefined_places)} incomplete place entities")
    return 0

if __name__ == "__main__":
    sys.exit(main())