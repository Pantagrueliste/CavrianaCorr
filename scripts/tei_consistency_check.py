#!/usr/bin/env python3
"""
scripts/tei_consistency_check.py
Analyzes TEI encoding for inconsistencies and recommends improvements.
"""

from pathlib import Path
from lxml import etree
import re
from collections import defaultdict

# Configuration
LETTERS_DIR = Path("letters")
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def analyze_tei_files():
    """Analyze all TEI files for consistency issues."""
    
    issues = defaultdict(list)
    recommendations = []
    
    # Skip entity files
    xml_files = [f for f in LETTERS_DIR.glob("*.xml") 
                 if f.name not in ["persNames.xml", "placeNames.xml"]]
    
    print(f"Analyzing {len(xml_files)} TEI letter files...")
    
    # Track various encoding patterns
    date_formats = set()
    salutation_patterns = set()
    closing_patterns = set()
    lb_usage = defaultdict(int)
    choice_usage = defaultdict(int)
    
    for xml_file in xml_files:
        try:
            # Parse the XML
            doc = etree.parse(xml_file)
            root = doc.getroot()
            
            # Check for basic TEI structure
            tei_header = root.find(".//tei:teiHeader", namespaces=NS)
            text_body = root.find(".//tei:text/tei:body", namespaces=NS)
            
            if tei_header is None:
                issues["missing_tei_header"].append(xml_file.name)
            
            if text_body is None:
                issues["missing_text_body"].append(xml_file.name)
            
            # Check date formats
            dates = root.xpath(".//tei:date[@when]/@when", namespaces=NS)
            for date in dates:
                date_formats.add(date)
            
            # Check salutation patterns
            salutations = root.xpath(".//tei:opener/tei:salute", namespaces=NS)
            for salute in salutations:
                text = (salute.text or "").strip()
                if text:
                    salutation_patterns.add(text[:50])  # First 50 chars
            
            # Check closing patterns
            closings = root.xpath(".//tei:closer/tei:salute", namespaces=NS)
            for salute in closings:
                text = (salute.text or "").strip()
                if text:
                    closing_patterns.add(text[:50])  # First 50 chars
            
            # Check line break usage
            lbs = root.xpath(".//tei:lb", namespaces=NS)
            lb_usage[xml_file.name] = len(lbs)
            
            # Check choice/abbreviation usage
            choices = root.xpath(".//tei:choice", namespaces=NS)
            choice_usage[xml_file.name] = len(choices)
            
            # Check for missing required elements
            title_stmt = root.find(".//tei:titleStmt/tei:title", namespaces=NS)
            if title_stmt is None or not title_stmt.text:
                issues["missing_title"].append(xml_file.name)
            
            # Check correspondence metadata
            corresp_sent = root.find(".//tei:correspAction[@type='sent']", namespaces=NS)
            corresp_received = root.find(".//tei:correspAction[@type='received']", namespaces=NS)
            
            if corresp_sent is None:
                issues["missing_corresp_sent"].append(xml_file.name)
            
            if corresp_received is None:
                issues["missing_corresp_received"].append(xml_file.name)
            
            # Check for inconsistent entity references
            person_refs = root.xpath(".//tei:persName[@ref]/@ref", namespaces=NS)
            place_refs = root.xpath(".//tei:placeName[@ref]/@ref", namespaces=NS)
            
            # Check for potential encoding issues
            # Look for raw text that might need encoding
            text_content = root.xpath(".//tei:p/text()", namespaces=NS)
            for text in text_content:
                if text and len(text) > 200:  # Very long text without markup
                    issues["long_unencoded_text"].append(f"{xml_file.name}: {text[:50]}...")
                    break
            
        except Exception as e:
            issues["parsing_error"].append(f"{xml_file.name}: {str(e)}")
    
    # Generate recommendations based on findings
    if date_formats:
        recommendations.append(f"Date formats found: {len(date_formats)} unique formats")
        recommendations.append("Recommendation: Standardize on YYYY-MM-DD format")
    
    if salutation_patterns:
        recommendations.append(f"Salutation patterns: {len(salutation_patterns)} unique patterns")
        recommendations.append("Recommendation: Consider standardizing salutation encoding")
    
    if closing_patterns:
        recommendations.append(f"Closing patterns: {len(closing_patterns)} unique patterns")
        recommendations.append("Recommendation: Consider standardizing closing encoding")
    
    # Analyze line break usage
    avg_lb = sum(lb_usage.values()) / len(lb_usage) if lb_usage else 0
    recommendations.append(f"Line break usage: Average {avg_lb:.1f} <lb/> elements per letter")
    
    # Analyze choice/abbreviation usage
    avg_choice = sum(choice_usage.values()) / len(choice_usage) if choice_usage else 0
    recommendations.append(f"Abbreviation encoding: Average {avg_choice:.1f} <choice> elements per letter")
    
    return issues, recommendations

def check_entity_consistency():
    """Check consistency between entity references and authority files."""
    
    # Load authority files
    try:
        pers_doc = etree.parse("letters/persNames.xml")
        place_doc = etree.parse("letters/placeNames.xml")
    except Exception as e:
        return {"authority_load_error": str(e)}, []
    
    # Get defined entities
    defined_pers = set()
    for person in pers_doc.xpath(".//tei:person", namespaces=NS):
        pers_id = person.get("xml:id", "")
        if pers_id:
            defined_pers.add(pers_id)
    
    defined_places = set()
    for place in place_doc.xpath(".//tei:place", namespaces=NS):
        place_id = place.get("xml:id", "")
        if place_id:
            defined_places.add(place_id)
    
    # Check references in letters
    entity_issues = defaultdict(list)
    
    xml_files = [f for f in LETTERS_DIR.glob("*.xml") 
                 if f.name not in ["persNames.xml", "placeNames.xml"]]
    
    for xml_file in xml_files:
        try:
            doc = etree.parse(xml_file)
            
            # Check person references
            person_refs = doc.xpath(".//tei:persName[@ref]/@ref", namespaces=NS)
            for ref in person_refs:
                # Handle both #pers-id and pers-id formats
                clean_ref = ref if ref.startswith("#") else f"#{ref}"
                if clean_ref not in defined_pers:
                    entity_issues["undefined_person_ref"].append(f"{xml_file.name}: {ref}")
            
            # Check place references
            place_refs = doc.xpath(".//tei:placeName[@ref]/@ref", namespaces=NS)
            for ref in place_refs:
                # Handle both #place-id and place-id formats
                clean_ref = ref if ref.startswith("#") else f"#{ref}"
                if clean_ref not in defined_places:
                    entity_issues["undefined_place_ref"].append(f"{xml_file.name}: {ref}")
            
        except Exception as e:
            entity_issues["entity_check_error"].append(f"{xml_file.name}: {str(e)}")
    
    return entity_issues, []

def main():
    """Main analysis function."""
    
    print("🔍 TEI Encoding Consistency Analysis")
    print("=" * 50)
    
    # Analyze TEI files
    issues, recommendations = analyze_tei_files()
    
    print("\n📋 ISSUES FOUND:")
    for issue_type, files in issues.items():
        if files:
            print(f"  • {issue_type.replace('_', ' ').title()}: {len(files)} occurrences")
            for file_info in files[:3]:  # Show first 3 examples
                print(f"    - {file_info}")
            if len(files) > 3:
                print(f"    - ... and {len(files) - 3} more")
    
    if not any(issues.values()):
        print("  • No major structural issues found!")
    
    # Check entity consistency
    entity_issues, _ = check_entity_consistency()
    
    print("\n🔗 ENTITY REFERENCE ISSUES:")
    for issue_type, refs in entity_issues.items():
        if refs:
            print(f"  • {issue_type.replace('_', ' ').title()}: {len(refs)} occurrences")
            for ref_info in refs[:3]:  # Show first 3 examples
                print(f"    - {ref_info}")
            if len(refs) > 3:
                print(f"    - ... and {len(refs) - 3} more")
    
    if not any(entity_issues.values()):
        print("  • All entity references are properly defined!")
    
    print("\n💡 RECOMMENDATIONS:")
    for i, recommendation in enumerate(recommendations, 1):
        print(f"  {i}. {recommendation}")
    
    print("\n✅ ANALYSIS COMPLETE")
    
    # Return summary
    total_issues = sum(len(v) for v in issues.values()) + sum(len(v) for v in entity_issues.values())
    print(f"\nSummary: {total_issues} total issues found across {len([f for f in LETTERS_DIR.glob('*.xml') if f.name not in ['persNames.xml', 'placeNames.xml']])} TEI files")

if __name__ == "__main__":
    main()