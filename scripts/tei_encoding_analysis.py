#!/usr/bin/env python3
"""
scripts/tei_encoding_analysis.py
Comprehensive TEI encoding analysis with specific recommendations.
"""

from pathlib import Path
from lxml import etree
import re
from collections import defaultdict

# Configuration
LETTERS_DIR = Path("letters")
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def analyze_encoding_patterns():
    """Analyze TEI encoding patterns across all letters."""
    
    print("🔍 TEI Encoding Pattern Analysis")
    print("=" * 50)
    
    # Skip entity files and incomplete files
    xml_files = [f for f in LETTERS_DIR.glob("*.xml") 
                 if f.name not in ["persNames.xml", "placeNames.xml", "1572-02-06.xml", "1572-03-08.xml"]]
    
    print(f"Analyzing {len(xml_files)} complete TEI letter files...")
    
    # Initialize analysis data structures
    encoding_stats = {
        'total_letters': 0,
        'with_cipher': 0,
        'with_abbreviations': 0,
        'with_line_breaks': 0,
        'with_entity_refs': 0,
        'with_supplied_text': 0,
        'with_unclear_text': 0,
        'with_foreign_lang': 0,
        'date_formats': set(),
        'salutation_types': set(),
        'closing_types': set(),
        'lb_counts': [],
        'choice_counts': [],
        'entity_ref_counts': [],
        'word_counts': []
    }
    
    # Specific encoding examples
    encoding_examples = {
        'cipher_examples': [],
        'abbreviation_examples': [],
        'complex_entity_examples': [],
        'unencoded_text_examples': []
    }
    
    for xml_file in xml_files:
        try:
            encoding_stats['total_letters'] += 1
            
            # Parse the XML
            doc = etree.parse(xml_file)
            root = doc.getroot()
            
            # Check for various TEI elements
            has_cipher = len(root.xpath(".//tei:seg[@type='cipher']", namespaces=NS)) > 0
            has_abbreviations = len(root.xpath(".//tei:choice", namespaces=NS)) > 0
            has_line_breaks = len(root.xpath(".//tei:lb", namespaces=NS)) > 0
            has_entity_refs = len(root.xpath(".//tei:persName[@ref] | .//tei:placeName[@ref]", namespaces=NS)) > 0
            has_supplied = len(root.xpath(".//tei:supplied", namespaces=NS)) > 0
            has_unclear = len(root.xpath(".//tei:unclear", namespaces=NS)) > 0
            has_foreign = len(root.xpath(".//tei:foreign", namespaces=NS)) > 0
            
            # Update statistics
            if has_cipher:
                encoding_stats['with_cipher'] += 1
            if has_abbreviations:
                encoding_stats['with_abbreviations'] += 1
            if has_line_breaks:
                encoding_stats['with_line_breaks'] += 1
            if has_entity_refs:
                encoding_stats['with_entity_refs'] += 1
            if has_supplied:
                encoding_stats['with_supplied_text'] += 1
            if has_unclear:
                encoding_stats['with_unclear_text'] += 1
            if has_foreign:
                encoding_stats['with_foreign_lang'] += 1
            
            # Collect specific examples
            if has_cipher:
                cipher_ex = root.xpath(".//tei:seg[@type='cipher']", namespaces=NS)
                if cipher_ex:
                    encoding_examples['cipher_examples'].append({
                        'file': xml_file.name,
                        'example': etree.tostring(cipher_ex[0], encoding='unicode')[:100]
                    })
            
            if has_abbreviations:
                choice_ex = root.xpath(".//tei:choice", namespaces=NS)
                if choice_ex:
                    encoding_examples['abbreviation_examples'].append({
                        'file': xml_file.name,
                        'example': etree.tostring(choice_ex[0], encoding='unicode')[:100]
                    })
            
            # Count specific elements
            lb_count = len(root.xpath(".//tei:lb", namespaces=NS))
            choice_count = len(root.xpath(".//tei:choice", namespaces=NS))
            entity_ref_count = len(root.xpath(".//tei:persName[@ref] | .//tei:placeName[@ref]", namespaces=NS))
            
            encoding_stats['lb_counts'].append(lb_count)
            encoding_stats['choice_counts'].append(choice_count)
            encoding_stats['entity_ref_counts'].append(entity_ref_count)
            
            # Get word count from body text
            body = root.find(".//tei:text/tei:body", namespaces=NS)
            if body is not None:
                text_content = " ".join(body.xpath(".//text()", namespaces=NS))
                words = re.findall(r'\b\w+\b', text_content)
                encoding_stats['word_counts'].append(len(words))
            
            # Analyze date formats
            dates = root.xpath(".//tei:date[@when]/@when", namespaces=NS)
            for date in dates:
                encoding_stats['date_formats'].add(date)
            
            # Analyze salutation and closing patterns
            salutations = root.xpath(".//tei:opener/tei:salute", namespaces=NS)
            for salute in salutations:
                text = (salute.text or "").strip()
                if text:
                    # Categorize by type
                    if "Sereniss" in text or "Sereniss" in text:
                        encoding_stats['salutation_types'].add("formal_noble")
                    elif "Illustriss" in text:
                        encoding_stats['salutation_types'].add("formal_clergy")
                    else:
                        encoding_stats['salutation_types'].add("general")
            
            closings = root.xpath(".//tei:closer/tei:salute", namespaces=NS)
            for salute in closings:
                text = (salute.text or "").strip()
                if text:
                    if "servitore" in text.lower() or "servidore" in text.lower():
                        encoding_stats['closing_types'].add("servitore")
                    else:
                        encoding_stats['closing_types'].add("general")
            
            # Check for complex entity references
            complex_refs = root.xpath(".//tei:persName[@ref][contains(@ref, '-')] | .//tei:placeName[@ref][contains(@ref, '-')]", namespaces=NS)
            if len(complex_refs) > 5:  # More than 5 entity references
                encoding_examples['complex_entity_examples'].append(xml_file.name)
            
            # Look for potentially unencoded text
            long_paragraphs = root.xpath(".//tei:p[string-length(text()) > 200]", namespaces=NS)
            if long_paragraphs:
                encoding_examples['unencoded_text_examples'].append({
                    'file': xml_file.name,
                    'length': len(long_paragraphs)
                })
            
        except Exception as e:
            print(f"⚠️  Error analyzing {xml_file.name}: {e}")
    
    return encoding_stats, encoding_examples

def generate_recommendations(stats, examples):
    """Generate specific recommendations based on analysis."""
    
    recommendations = []
    
    # Basic statistics
    recommendations.append("📊 ENCODING STATISTICS:")
    recommendations.append(f"  • Total letters analyzed: {stats['total_letters']}")
    recommendations.append(f"  • Letters with cipher text: {stats['with_cipher']} ({stats['with_cipher']/stats['total_letters']*100:.1f}%)")
    recommendations.append(f"  • Letters with abbreviations: {stats['with_abbreviations']} ({stats['with_abbreviations']/stats['total_letters']*100:.1f}%)")
    recommendations.append(f"  • Letters with entity references: {stats['with_entity_refs']} ({stats['with_entity_refs']/stats['total_letters']*100:.1f}%)")
    recommendations.append(f"  • Letters with supplied text: {stats['with_supplied_text']} ({stats['with_supplied_text']/stats['total_letters']*100:.1f}%)")
    recommendations.append(f"  • Letters with unclear text: {stats['with_unclear_text']} ({stats['with_unclear_text']/stats['total_letters']*100:.1f}%)")
    
    # Averages
    if stats['lb_counts']:
        avg_lb = sum(stats['lb_counts']) / len(stats['lb_counts'])
        recommendations.append(f"  • Average line breaks per letter: {avg_lb:.1f}")
    
    if stats['choice_counts']:
        avg_choice = sum(stats['choice_counts']) / len(stats['choice_counts'])
        recommendations.append(f"  • Average abbreviations per letter: {avg_choice:.1f}")
    
    if stats['entity_ref_counts']:
        avg_refs = sum(stats['entity_ref_counts']) / len(stats['entity_ref_counts'])
        recommendations.append(f"  • Average entity references per letter: {avg_refs:.1f}")
    
    if stats['word_counts']:
        avg_words = sum(stats['word_counts']) / len(stats['word_counts'])
        recommendations.append(f"  • Average word count: {avg_words:.0f}")
    
    # Specific recommendations
    recommendations.append("\n💡 SPECIFIC RECOMMENDATIONS:")
    
    if stats['with_cipher'] > 0:
        recommendations.append(f"  ✅ Cipher encoding: Well implemented in {stats['with_cipher']} letters")
        if examples['cipher_examples']:
            recommendations.append(f"     Example: {examples['cipher_examples'][0]['example']}...")
    
    if stats['with_abbreviations'] < stats['total_letters'] * 0.8:
        recommendations.append(f"  ⚠️  Abbreviation encoding: Only {stats['with_abbreviations']/stats['total_letters']*100:.1f}% of letters use <choice> for abbreviations")
        recommendations.append("     Recommendation: Consider adding more abbreviation expansions for consistency")
    else:
        recommendations.append(f"  ✅ Abbreviation encoding: Well implemented in {stats['with_abbreviations']/stats['total_letters']*100:.1f}% of letters")
    
    if len(stats['date_formats']) > 1:
        recommendations.append(f"  ⚠️  Date formats: {len(stats['date_formats'])} different formats found")
        recommendations.append("     Recommendation: Standardize on YYYY-MM-DD format for consistency")
    
    if len(stats['salutation_types']) > 2:
        recommendations.append(f"  ✅ Salutation patterns: {len(stats['salutation_types'])} different types (formal, general, etc.)")
        recommendations.append("     This variety is appropriate for different addressees")
    
    if examples['unencoded_text_examples']:
        recommendations.append(f"  ⚠️  Long unencoded text: Found in {len(examples['unencoded_text_examples'])} letters")
        recommendations.append("     Recommendation: Consider adding more semantic markup to long paragraphs")
    
    if stats['with_entity_refs'] < stats['total_letters'] * 0.9:
        recommendations.append(f"  📍 Entity references: {stats['with_entity_refs']/stats['total_letters']*100:.1f}% of letters use entity references")
        recommendations.append("     Recommendation: Consider adding more entity references for better semantic richness")
    
    # Encoding quality assessment
    quality_score = 0
    if stats['with_abbreviations'] > stats['total_letters'] * 0.7:
        quality_score += 1
    if stats['with_entity_refs'] > stats['total_letters'] * 0.8:
        quality_score += 1
    if len(stats['date_formats']) <= 2:
        quality_score += 1
    if stats['with_supplied_text'] > 0 or stats['with_unclear_text'] > 0:
        quality_score += 1
    
    quality_percentage = (quality_score / 4) * 100
    recommendations.append(f"\n🎯 OVERALL ENCODING QUALITY: {quality_percentage:.0f}/100")
    
    if quality_percentage >= 80:
        recommendations.append("  Excellent! The TEI encoding is comprehensive and consistent.")
    elif quality_percentage >= 60:
        recommendations.append("  Good! The TEI encoding is solid with room for improvement.")
    elif quality_percentage >= 40:
        recommendations.append("  Fair! The TEI encoding is functional but could be enhanced.")
    else:
        recommendations.append("  Needs attention! The TEI encoding could benefit from significant improvement.")
    
    return recommendations

def main():
    """Main analysis function."""
    
    # Perform encoding analysis
    stats, examples = analyze_encoding_patterns()
    
    # Generate recommendations
    recommendations = generate_recommendations(stats, examples)
    
    # Display recommendations
    for recommendation in recommendations:
        print(recommendation)
    
    print("\n✅ ANALYSIS COMPLETE")
    print(f"\nDetailed analysis available in script output above.")

if __name__ == "__main__":
    main()