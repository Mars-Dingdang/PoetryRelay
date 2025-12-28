import json
import os
import glob
from src.utils import clean_sentence, split_into_sentences, to_simplified

def load_sentences(data_dir):
    """
    Load sentences from all JSON files in the data directory.
    Returns a set of unique, cleaned sentences.
    """
    sentences = set()
    files = glob.glob(os.path.join(data_dir, "*.json"))
    
    print(f"Found {len(files)} data files.")
    
    for fpath in files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for item in data:
                # Handle different field names
                paragraphs = item.get("paragraphs") or item.get("content") or []
                
                for p in paragraphs:
                    # Convert to simplified Chinese first
                    p_simp = to_simplified(p)
                    
                    # Split paragraph into sentences
                    parts = split_into_sentences(p_simp)
                    for part in parts:
                        cleaned = clean_sentence(part)
                        if len(cleaned) >= 2: # Filter out very short fragments
                            sentences.add(cleaned)
        except Exception as e:
            print(f"Error reading {fpath}: {e}")
            
    print(f"Loaded {len(sentences)} unique sentences.")
    return list(sentences)
