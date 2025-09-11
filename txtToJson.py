import json
import re
import os
from pathlib import Path

def txt_to_json_sentences(input_file, output_file):
    """
    Convert a text file to JSON format containing all sentences.
    
    Args:
        input_file (str): Path to the input .txt file
        output_file (str): Path to the output .json file
    
    Returns:
        list: List of sentences if successful, None if error occurred
    """
    sentences = []
    
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return None
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        
        print(f"Reading file: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as file:
            line_count = 0
            for line in file:
                line_count += 1
                
                # Remove line numbers at the beginning (digits followed by tab/spaces)
                line_cleaned = re.sub(r'^\d+\s+', '', line.strip())
                
                # Skip empty lines
                if not line_cleaned:
                    continue
                
                # Additional cleaning: remove extra whitespace
                line_cleaned = ' '.join(line_cleaned.split())
                
                # Add the sentence to the list
                sentences.append(line_cleaned)
                
                # Progress indicator for large files
                if line_count % 10000 == 0:
                    print(f"Processed {line_count} lines...")
        
        print(f"Writing {len(sentences)} sentences to JSON file...")
        
        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(sentences, json_file, ensure_ascii=False, indent=2)
        
        print(f"✅ Successfully converted {len(sentences)} sentences to {output_file}")
        print(f"📁 Output file size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
        
        return sentences
    
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.")
        return None
    except PermissionError:
        print(f"❌ Error: Permission denied accessing '{input_file}' or '{output_file}'.")
        return None
    except UnicodeDecodeError:
        print(f"❌ Error: Unable to decode file '{input_file}'. Try different encoding.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def txt_to_json_unique_sentences(input_file, output_file):
    """
    Convert a text file to JSON format containing unique sentences only.
    
    Args:
        input_file (str): Path to the input .txt file
        output_file (str): Path to the output .json file
    
    Returns:
        list: List of unique sentences if successful, None if error occurred
    """
    sentences = set()  # Use set to automatically handle duplicates
    
    try:
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return None
        
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"Reading file for unique sentences: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as file:
            line_count = 0
            for line in file:
                line_count += 1
                
                line_cleaned = re.sub(r'^\d+\s+', '', line.strip())
                
                if not line_cleaned:
                    continue
                
                line_cleaned = ' '.join(line_cleaned.split())
                sentences.add(line_cleaned)
                
                if line_count % 10000 == 0:
                    print(f"Processed {line_count} lines, found {len(sentences)} unique sentences...")
        
        # Convert set to sorted list for consistent output
        sentences_list = sorted(list(sentences))
        
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(sentences_list, json_file, ensure_ascii=False, indent=2)
        
        print(f"✅ Successfully converted {len(sentences_list)} unique sentences to {output_file}")
        print(f"📁 Output file size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
        
        return sentences_list
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def preview_sentences(sentences, count=3):
    """
    Display a preview of sentences.
    
    Args:
        sentences (list): List of sentences
        count (int): Number of sentences to preview
    """
    if not sentences:
        print("No sentences to preview.")
        return
    
    print(f"\n📖 Preview of first {min(count, len(sentences))} sentences:")
    print("-" * 80)
    
    for i, sentence in enumerate(sentences[:count], 1):
        # Truncate very long sentences for preview
        display_sentence = sentence[:100] + "..." if len(sentence) > 100 else sentence
        print(f"{i:2d}. {display_sentence}")
    
    print("-" * 80)

# Main execution
if __name__ == "__main__":
    # Configuration
    INPUT_FILE = r""
    OUTPUT_DIR = r""
    
    # Output files
    all_sentences_file = os.path.join(OUTPUT_DIR, "all_sentences.json")
    unique_sentences_file = os.path.join(OUTPUT_DIR, "unique_sentences.json")
    
    print("🚀 Starting sentence conversion...")
    print(f"📂 Input file: {INPUT_FILE}")
    print(f"📂 Output directory: {OUTPUT_DIR}")
    print("=" * 80)
    
    # Convert all sentences (including duplicates)
    print("\n1️⃣ Converting all sentences...")
    all_sentences = txt_to_json_sentences(INPUT_FILE, all_sentences_file)
    
    if all_sentences:
        preview_sentences(all_sentences, 3)
    
    print("\n" + "=" * 80)
    
    # Convert unique sentences only
    print("\n2️⃣ Converting unique sentences...")
    unique_sentences = txt_to_json_unique_sentences(INPUT_FILE, unique_sentences_file)
    
    if unique_sentences:
        preview_sentences(unique_sentences, 3)
        
        # Statistics
        if all_sentences:
            duplicate_count = len(all_sentences) - len(unique_sentences)
            duplicate_percentage = (duplicate_count / len(all_sentences)) * 100
            
            print(f"\n📊 Statistics:")
            print(f"   Total sentences: {len(all_sentences):,}")
            print(f"   Unique sentences: {len(unique_sentences):,}")
            print(f"   Duplicates removed: {duplicate_count:,} ({duplicate_percentage:.1f}%)")
    
    print("\n🎉 Conversion completed!")
    print("Files created:")
    if os.path.exists(all_sentences_file):
        print(f"   📄 {all_sentences_file}")
    if os.path.exists(unique_sentences_file):
        print(f"   📄 {unique_sentences_file}")