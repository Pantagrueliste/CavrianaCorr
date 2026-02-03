#!/usr/bin/env python3
"""
scripts/reorganize_entities.py
Reorganizes entity files with logical grouping and adds incomplete entity section.
"""

from pathlib import Path
from lxml import etree
import sys

# Configuration
PERS_FILE = Path("letters/persNames.xml")
PLACE_FILE = Path("letters/placeNames.xml")
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def parse_entities(file_path):
    """Parse TEI entity file and return root element."""
    try:
        doc = etree.parse(file_path)
        return doc.getroot()
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def get_entity_elements(root, entity_type):
    """Extract entity elements from TEI file."""
    if entity_type == "person":
        return root.xpath(".//tei:person", namespaces=NS)
    elif entity_type == "place":
        return root.xpath(".//tei:place", namespaces=NS)
    return []

def categorize_person(person_elem):
    """Categorize person entity based on ID and content."""
    pers_id = person_elem.get("xml:id", "")
    
    # Check if entity is complete (has basic metadata)
    pers_name = person_elem.find(".//tei:persName", namespaces=NS)
    has_viat = person_elem.find(".//tei:idno[@type='VIAF']", namespaces=NS) is not None
    has_occupation = person_elem.find(".//tei:occupation", namespaces=NS) is not None
    
    is_complete = pers_name is not None and (has_viat or has_occupation)
    
    # Categorize by family/dynasty - check for known undefined entities first
    if pers_id == "pers-bourbon-conde":
        return ("French Nobility - Condé", False)  # Known undefined
    elif pers_id == "pers-pontefice":
        return ("Ecclesiastical Figures - Popes", False)  # Known undefined
    elif pers_id == "pers-cesare":
        return ("Italian Noble Houses - Este", False)  # Likely Cesare d'Este
    elif pers_id == "pers-este-card":
        return ("Ecclesiastical Figures - Cardinals", False)  # Este cardinal
    elif pers_id == "pers-guadagni":
        return ("Other Historical Figures", False)  # Guadagni family
    elif pers_id == "pers-lorraine-h":
        return ("French Nobility - Lorraine", False)  # Henry of Lorraine
    elif pers_id == "pers-papazzone-g":
        return ("Ecclesiastical Figures - Popes", False)  # Pope reference
    elif pers_id == "pers-sanseverino-g":
        return ("Other Historical Figures", False)  # Sanseverino family
    elif pers_id == "pers-taxis-c":
        return ("Other Historical Figures", False)  # Taxi family
    
    # Categorize known complete entities
    elif "medici" in pers_id:
        return ("Italian Noble Houses - Medici Dynasty", is_complete)
    elif "este" in pers_id or "deste" in pers_id:
        return ("Italian Noble Houses - Este", is_complete)
    elif "savoy" in pers_id or "savoie" in pers_id:
        return ("Italian Noble Houses - Savoy", is_complete)
    elif "gonzaga" in pers_id:
        return ("Italian Noble Houses - Gonzaga", is_complete)
    elif "valois" in pers_id:
        return ("French Royal Family - Valois", is_complete)
    elif "bourbon" in pers_id:
        return ("French Royal Family - Bourbon", is_complete)
    elif "conde" in pers_id:
        return ("French Nobility - Condé", is_complete)
    elif "guise" in pers_id:
        return ("French Nobility - Guise", is_complete)
    elif "montmorency" in pers_id:
        return ("French Nobility - Montmorency", is_complete)
    elif any(x in pers_id for x in ["card", "cardinal"]):
        return ("Ecclesiastical Figures - Cardinals", is_complete)
    elif any(x in pers_id for x in ["milit", "sold", "capitano"]):
        return ("Military Figures", is_complete)
    elif any(x in pers_id for x in ["ambas", "secret", "mess"]):
        return ("Diplomats and Ambassadors", is_complete)
    else:
        return ("Other Historical Figures", is_complete)

def categorize_place(place_elem):
    """Categorize place entity based on ID and content."""
    place_id = place_elem.get("xml:id", "")
    
    # Check if entity is complete
    place_name = place_elem.find(".//tei:placeName", namespaces=NS)
    has_geo = place_elem.find(".//tei:geo", namespaces=NS) is not None
    has_tgn = place_elem.find(".//tei:idno[@type='TGN']", namespaces=NS) is not None
    
    is_complete = place_name is not None and (has_geo or has_tgn)
    
    # Check for known undefined places first
    if place_id == "place-blois":
        return ("French Cities and Regions", False)  # Known undefined
    elif place_id == "place-sancerre":
        return ("French Cities and Regions", False)  # Known undefined
    elif place_id == "place-bourbon":
        return ("French Cities and Regions", False)  # Known undefined
    elif place_id == "place-europe":
        return ("Other European Locations", False)  # Known undefined
    elif place_id == "place-ferrara":
        return ("Italian Cities and Regions", False)  # Known undefined
    elif place_id == "place-gatinais":
        return ("French Cities and Regions", False)  # Known undefined
    elif place_id == "place-genova":
        return ("Italian Cities and Regions", False)  # Known undefined
    elif place_id == "place-guyenne":
        return ("French Cities and Regions", False)  # Known undefined
    elif place_id == "place-lille":
        return ("French Cities and Regions", False)  # Known undefined
    elif place_id == "place-limousin":
        return ("French Cities and Regions", False)  # Known undefined
    elif place_id == "place-lyon":
        return ("French Cities and Regions", False)  # Known undefined
    elif place_id == "place-navarre":
        return ("Other European Locations", False)  # Known undefined
    elif place_id == "place-orleans":
        return ("French Cities and Regions", False)  # Known undefined
    elif place_id == "place-venezia":
        return ("Italian Cities and Regions", False)  # Known undefined
    
    # Categorize known complete places
    elif any(x in place_id for x in ["firenze", "milano", "venezia", "genova", 
                                    "roma", "napoli", "siena", "pisa"]):
        return ("Italian Cities and Regions", is_complete)
    elif any(x in place_id for x in ["paris", "lyon", "blois", "orleans",
                                     "rouen", "bordeaux", "marsiglia"]):
        return ("French Cities and Regions", is_complete)
    elif any(x in place_id for x in ["spagna", "inghilterra", "germania",
                                     "fiandre", "svizzera"]):
        return ("Other European Locations", is_complete)
    else:
        return ("Other Locations", is_complete)

def reorganize_file(file_path, entity_type):
    """Reorganize entity file with logical grouping."""
    root = parse_entities(file_path)
    if root is None:
        return False
    
    # Get all entity elements
    entities = get_entity_elements(root, entity_type)
    
    # Categorize entities
    categorized = {}
    for entity in entities:
        if entity_type == "person":
            category, is_complete = categorize_person(entity)
        else:
            category, is_complete = categorize_place(entity)
            
        if category not in categorized:
            categorized[category] = {"complete": [], "incomplete": []}
            
        if is_complete:
            categorized[category]["complete"].append(entity)
        else:
            categorized[category]["incomplete"].append(entity)
    
    # Create new list structure
    list_elem = root.find(f".//tei:list{entity_type.capitalize()}", namespaces=NS)
    if list_elem is None:
        print(f"Could not find list element in {file_path}")
        return False
    
    # Clear existing content
    list_elem.clear()
    
    # Add categorized entities with proper section separation
    current_category = None
    for category in sorted(categorized.keys()):
        # Add section header comment
        if category != current_category:
            list_elem.append(etree.Comment(f" {category} "))
            current_category = category
        
        # Add complete entities first
        if categorized[category]["complete"]:
            for entity in categorized[category]["complete"]:
                list_elem.append(entity)
        
        # Add incomplete entities within same category
        if categorized[category]["incomplete"]:
            for entity in categorized[category]["incomplete"]:
                list_elem.append(entity)
    
    # Add final incomplete section for entities that couldn't be categorized
    list_elem.append(etree.Comment(" INCOMPLETE ENTITIES (needs research) "))
    
    # Write back to file
    try:
        doc = etree.ElementTree(root)
        doc.write(file_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)
        print(f"✅ Reorganized {file_path}")
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False

def main():
    """Main function to reorganize entity files."""
    print("Reorganizing entity files...")
    
    # Reorganize person names
    if not reorganize_file(PERS_FILE, "person"):
        print("❌ Failed to reorganize persNames.xml")
        return 1
    
    # Reorganize place names  
    if not reorganize_file(PLACE_FILE, "place"):
        print("❌ Failed to reorganize placeNames.xml")
        return 1
    
    print("✅ Entity reorganization complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())