#!/usr/bin/env python3
"""
Simple script to list all available PIC chip types in the chipdata.cid file.
"""

import sys
from pathlib import Path
from picpro.ChipInfoReader import ChipInfoReader

def find_chip_data():
    """Find the chipdata.cid file in common locations."""
    possible_paths = [
        Path(__file__).parent / "usr/share/picpro/chipdata.cid",
        Path("/usr/share/picpro/chipdata.cid"),
        Path("chipdata.cid")
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    raise FileNotFoundError("chipdata.cid file not found")

def main():
    try:
        chip_data_path = find_chip_data()
        print(f"Reading chip data from: {chip_data_path}")
        
        reader = ChipInfoReader(chip_data_path)
        
        chip_names = sorted(reader.chip_entries.keys())
        
        print(f"\nFound {len(chip_names)} supported PIC chips:")
        print("=" * 50)
        
        for chip in chip_names:
            print(chip)
            
        # Look for chips similar to 16f887
        print(f"\n16F series chips containing '8':")
        print("-" * 30)
        for chip in chip_names:
            if chip.startswith('16f') and '8' in chip:
                print(chip)
                
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
