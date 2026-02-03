#!/usr/bin/env python3
"""
scripts/validate_dates.py
Validates date formats in TEI files and provides quality control.
"""

from pathlib import Path
from lxml import etree
import re
from datetime import datetime

# Configuration
LETTERS_DIR = Path("letters")
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def validate_date_format(date_value):
    """Validate a date format and return validation result."""
    
    # Check for date ranges
    if '/' in date_value:
        parts = date_value.split('/')
        if len(parts) != 2:
            return {'valid': False, 'issue': 'Invalid date range format', 'date': date_value}
        
        # Validate each part of the range
        for part in parts:
            if not validate_single_date(part)['valid']:
                return {'valid': False, 'issue': 'Invalid date in range', 'date': date_value}
        
        return {'valid': True, 'type': 'range', 'date': date_value}
    
    else:
        return validate_single_date(date_value)

def validate_single_date(date_value):
    """Validate a single date value."""
    
    # Check length and format
    if len(date_value) == 10 and date_value.count('-') == 2:  # YYYY-MM-DD
        try:
            # Validate the date is actually valid
            datetime.strptime(date_value, '%Y-%m-%d')
            return {'valid': True, 'type': 'full', 'date': date_value}
        except ValueError:
            return {'valid': False, 'issue': 'Invalid date', 'date': date_value}
    
    elif len(date_value) == 7 and date_value.count('-') == 1:  # YYYY-MM
        try:
            datetime.strptime(date_value, '%Y-%m')
            return {'valid': True, 'type': 'year-month', 'date': date_value}
        except ValueError:
            return {'valid': False, 'issue': 'Invalid year-month', 'date': date_value}
    
    elif len(date_value) == 4 and date_value.isdigit():  # YYYY
        return {'valid': True, 'type': 'year', 'date': date_value}
    
    else:
        return {'valid': False, 'issue': 'Unrecognized date format', 'date': date_value}

def validate_tei_dates():
    """Validate all date formats in TEI files."""
    
    print("🔍 Validating TEI Date Formats")
    print("=" * 40)
    
    # Skip entity files and incomplete files
    xml_files = [f for f in LETTERS_DIR.glob("*.xml") 
                 if f.name not in ["persNames.xml", "placeNames.xml", "1572-02-06.xml", "1572-03-08.xml"]]
    
    validation_results = {
        'total_dates': 0,
        'valid_dates': 0,
        'invalid_dates': 0,
        'date_ranges': 0,
        'year_only': 0,
        'year_month': 0,
        'full_dates': 0,
        'issues': []
    }
    
    for xml_file in xml_files:
        try:
            doc = etree.parse(xml_file)
            root = doc.getroot()
            
            # Find all date elements
            dates = root.xpath(".//tei:date[@when]", namespaces=NS)
            
            for date_elem in dates:
                validation_results['total_dates'] += 1
                date_value = date_elem.get("when")
                
                result = validate_date_format(date_value)
                
                if result['valid']:
                    validation_results['valid_dates'] += 1
                    
                    if result['type'] == 'range':
                        validation_results['date_ranges'] += 1
                    elif result['type'] == 'year':
                        validation_results['year_only'] += 1
                    elif result['type'] == 'year-month':
                        validation_results['year_month'] += 1
                    elif result['type'] == 'full':
                        validation_results['full_dates'] += 1
                    
                else:
                    validation_results['invalid_dates'] += 1
                    validation_results['issues'].append({
                        'file': xml_file.name,
                        'date': date_value,
                        'issue': result['issue'],
                        'text': date_elem.text
                    })
            
        except Exception as e:
            validation_results['issues'].append({
                'file': xml_file.name,
                'date': 'N/A',
                'issue': f'Parsing error: {str(e)}',
                'text': 'N/A'
            })
    
    return validation_results

def generate_date_report(results):
    """Generate a report from validation results."""
    
    report = []
    
    report.append("📊 DATE VALIDATION REPORT")
    report.append("=" * 30)
    report.append(f"Total dates analyzed: {results['total_dates']}")
    report.append(f"Valid dates: {results['valid_dates']} ({results['valid_dates']/results['total_dates']*100:.1f}%)")
    report.append(f"Invalid dates: {results['invalid_dates']} ({results['invalid_dates']/results['total_dates']*100:.1f}%)")
    
    report.append("\n📋 DATE FORMAT BREAKDOWN:")
    report.append(f"  • Full dates (YYYY-MM-DD): {results['full_dates']}")
    report.append(f"  • Year-month dates (YYYY-MM): {results['year_month']}")
    report.append(f"  • Year-only dates (YYYY): {results['year_only']}")
    report.append(f"  • Date ranges: {results['date_ranges']}")
    
    if results['invalid_dates'] > 0:
        report.append("\n⚠️  INVALID DATES FOUND:")
        for issue in results['issues'][:10]:  # Show first 10
            report.append(f"  • {issue['file']}: {issue['date']} - {issue['issue']}")
        if len(results['issues']) > 10:
            report.append(f"  • ... and {len(results['issues']) - 10} more issues")
    else:
        report.append("\n✅ NO INVALID DATES FOUND!")
        report.append("   All dates conform to TEI best practices.")
    
    # Quality assessment
    if results['invalid_dates'] == 0:
        quality_score = 100
        quality_text = "Excellent"
    elif results['invalid_dates'] <= results['total_dates'] * 0.05:  # <= 5% invalid
        quality_score = 90
        quality_text = "Very Good"
    elif results['invalid_dates'] <= results['total_dates'] * 0.10:  # <= 10% invalid
        quality_score = 75
        quality_text = "Good"
    else:
        quality_score = 50
        quality_text = "Needs Attention"
    
    report.append(f"\n🎯 DATE ENCODING QUALITY: {quality_score}/100 ({quality_text})")
    
    if quality_score >= 90:
        report.append("   Your date encoding follows TEI best practices!")
    else:
        report.append("   Consider addressing the invalid dates for better consistency.")
    
    return report

def main():
    """Main validation function."""
    
    # Validate all dates
    results = validate_tei_dates()
    
    # Generate and display report
    report = generate_date_report(results)
    
    for line in report:
        print(line)
    
    # Return exit code based on validation
    if results['invalid_dates'] > 0:
        print(f"\n💡 RECOMMENDATION:")
        print(f"   Run: python scripts/standardize_dates.py")
        print(f"   To automatically fix date format issues.")
        return 1
    else:
        print(f"\n✅ VALIDATION PASSED!")
        print(f"   All {results['total_dates']} dates are properly formatted.")
        return 0

if __name__ == "__main__":
    exit(main())