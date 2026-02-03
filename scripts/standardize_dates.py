#!/usr/bin/env python3
"""
scripts/standardize_dates.py
Analyzes and standardizes date formats in TEI files.
"""

from pathlib import Path
from lxml import etree
import re
from datetime import datetime

# Configuration
LETTERS_DIR = Path("letters")
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def analyze_date_formats():
    """Analyze current date formats across all letters."""
    
    print("🔍 Analyzing Date Formats")
    print("=" * 40)
    
    # Skip entity files and incomplete files
    xml_files = [f for f in LETTERS_DIR.glob("*.xml") 
                 if f.name not in ["persNames.xml", "placeNames.xml", "1572-02-06.xml", "1572-03-08.xml"]]
    
    date_formats = {}
    date_issues = []
    
    for xml_file in xml_files:
        try:
            doc = etree.parse(xml_file)
            root = doc.getroot()
            
            # Find all date elements with @when attributes
            dates = root.xpath(".//tei:date[@when]", namespaces=NS)
            
            for date_elem in dates:
                date_value = date_elem.get("when")
                date_text = date_elem.text
                
                if date_value not in date_formats:
                    date_formats[date_value] = []
                
                date_formats[date_value].append({
                    'file': xml_file.name,
                    'text': date_text
                })
                
                # Check for potential issues
                if '/' in date_value:  # Date range in @when
                    date_issues.append(f"{xml_file.name}: Date range in @when: {date_value}")
                elif len(date_value) == 4:  # Year only
                    date_issues.append(f"{xml_file.name}: Year-only date: {date_value}")
                elif len(date_value) == 7:  # Year-month only
                    date_issues.append(f"{xml_file.name}: Year-month date: {date_value}")
                
        except Exception as e:
            print(f"⚠️  Error analyzing {xml_file.name}: {e}")
    
    return date_formats, date_issues

def standardize_date_format(date_value, date_text):
    """Standardize a date value to preferred format."""
    
    # Handle different date formats
    if '/' in date_value:  # Date range
        # Split range and standardize each part
        parts = date_value.split('/')
        standardized_parts = []
        
        for part in parts:
            if len(part) == 4:  # Year only
                standardized_parts.append(part + '-01-01')  # Default to Jan 1
            elif len(part) == 7:  # Year-month
                standardized_parts.append(part + '-01')  # Default to day 1
            else:
                standardized_parts.append(part)
        
        # Return as date range with proper attributes
        return {
            'from': standardized_parts[0],
            'to': standardized_parts[1] if len(standardized_parts) > 1 else standardized_parts[0],
            'text': date_text or f"from {standardized_parts[0]} to {standardized_parts[1]}"
        }
    
    elif len(date_value) == 4:  # Year only
        return {
            'when': date_value + '-01-01',  # Default to Jan 1
            'text': date_text or f"sometime in {date_value}"
        }
    
    elif len(date_value) == 7:  # Year-month
        return {
            'when': date_value + '-01',  # Default to day 1
            'text': date_text or f"sometime in {date_value}"
        }
    
    else:  # Already in YYYY-MM-DD format
        return {
            'when': date_value,
            'text': date_text
        }

def update_tei_file(file_path, standardization_map):
    """Update TEI file with standardized date formats."""
    
    try:
        doc = etree.parse(file_path)
        root = doc.getroot()
        
        modified = False
        
        # Find all date elements
        dates = root.xpath(".//tei:date[@when]", namespaces=NS)
        
        for date_elem in dates:
            original_date = date_elem.get("when")
            
            if original_date in standardization_map:
                standardized = standardization_map[original_date]
                
                # Clear existing attributes
                for attr in ['when', 'from', 'to', 'cert']:
                    if attr in date_elem.attrib:
                        del date_elem.attrib[attr]
                
                # Add standardized attributes
                if 'when' in standardized:
                    date_elem.set("when", standardized['when'])
                if 'from' in standardized:
                    date_elem.set("from", standardized['from'])
                if 'to' in standardized:
                    date_elem.set("to", standardized['to'])
                
                # Update text if provided
                if standardized['text']:
                    date_elem.text = standardized['text']
                
                modified = True
        
        if modified:
            # Write back to file
            doc.write(file_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to analyze and standardize dates."""
    
    # Analyze current date formats
    date_formats, date_issues = analyze_date_formats()
    
    print(f"\n📊 DATE FORMAT ANALYSIS:")
    print(f"Found {len(date_formats)} unique date formats across {len([f for f in LETTERS_DIR.glob('*.xml') if f.name not in ['persNames.xml', 'placeNames.xml', '1572-02-06.xml', '1572-03-08.xml']])} letters")
    
    if date_issues:
        print(f"\n⚠️  DATE FORMAT ISSUES:")
        for issue in date_issues[:10]:  # Show first 10
            print(f"  • {issue}")
        if len(date_issues) > 10:
            print(f"  • ... and {len(date_issues) - 10} more")
    
    # Show most common date formats
    print(f"\n📋 MOST COMMON DATE FORMATS:")
    for date_format, occurrences in sorted(date_formats.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  • {date_format}: {len(occurrences)} occurrences")
    
    # Ask for confirmation before making changes
    print(f"\n🔧 STANDARDIZATION PLAN:")
    print("  • Convert date ranges to @from/@to attributes")
    print("  • Standardize year-only dates to YYYY-01-01")
    print("  • Standardize year-month dates to YYYY-MM-01")
    print("  • Preserve original date text with clarifications")
    
    # Create standardization map
    standardization_map = {}
    
    for date_value, occurrences in date_formats.items():
        if date_value.count('-') < 2:  # Not already in YYYY-MM-DD format
            standardized = standardize_date_format(date_value, occurrences[0]['text'])
            standardization_map[date_value] = standardized
            print(f"  • {date_value} → {standardized}")
    
    if not standardization_map:
        print("  • All dates are already in standard format!")
        return
    
    # Apply standardization
    print(f"\n🔄 APPLYING STANDARDIZATION...")
    
    xml_files = [f for f in LETTERS_DIR.glob("*.xml") 
                 if f.name not in ["persNames.xml", "placeNames.xml", "1572-02-06.xml", "1572-03-08.xml"]]
    
    updated_count = 0
    
    for xml_file in xml_files:
        if update_tei_file(xml_file, standardization_map):
            updated_count += 1
            print(f"  ✅ Updated {xml_file.name}")
    
    print(f"\n✅ STANDARDIZATION COMPLETE!")
    print(f"Updated {updated_count} files with standardized date formats")
    
    if updated_count > 0:
        print(f"\n💡 RECOMMENDATION:")
        print(f"  • Review the changes with: git diff")
        print(f"  • Test the updated files with: python scripts/letter_parser.py")
        print(f"  • Consider adding date format validation to your workflow")

if __name__ == "__main__":
    main()