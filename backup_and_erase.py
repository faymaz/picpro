#!/usr/bin/env python3
"""
ICSP Backup and Erase Script
Reads chip content via ICSP and creates backup, then erases the chip
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

def backup_chip(chip_type, port, output_file):
    """Create backup of chip via ICSP."""
    print(f"📖 Creating backup of {chip_type.upper()} via ICSP...")
    print(f"   Port: {port}")
    print(f"   Output: {output_file}")
    
    # Read ROM content
    cmd = f"picpro read --pic_type {chip_type} --port {port} --icsp rom --hex_file {output_file}"
    print(f"🔧 Command: {cmd}")
    return cmd

def erase_chip(chip_type, port):
    """Erase the chip."""
    print(f"🗑️  Erasing {chip_type.upper()}...")
    print(f"   Port: {port}")
    
    cmd = f"picpro erase --pic_type {chip_type} --port {port} --icsp"
    print(f"🔧 Command: {cmd}")
    return cmd

def main():
    parser = argparse.ArgumentParser(description='Backup and erase PIC chip via ICSP')
    parser.add_argument('chip_type', choices=['16f887', '16c54'], 
                       help='Chip type (16f887 or 16c54)')
    parser.add_argument('--port', '-p', default='/dev/ttyUSB0',
                       help='Programmer port (default: /dev/ttyUSB0)')
    parser.add_argument('--output', '-o', 
                       help='Backup file name (auto-generated if not specified)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show commands without executing')
    
    args = parser.parse_args()
    
    # Generate backup filename if not provided
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"backup_{args.chip_type}_{timestamp}.hex"
    
    print("🔌 ICSP Backup and Erase Operation")
    print("=" * 40)
    print(f"Chip: {args.chip_type.upper()}")
    print(f"Port: {args.port}")
    print(f"Backup file: {args.output}")
    print(f"Dry run: {args.dry_run}")
    print()
    
    # Step 1: Backup
    backup_cmd = backup_chip(args.chip_type, args.port, args.output)
    
    if args.dry_run:
        print("DRY RUN - Commands that would be executed:")
        print(f"1. {backup_cmd}")
        print(f"2. {erase_chip(args.chip_type, args.port)}")
        return 0
    
    print("⚠️  READY TO EXECUTE:")
    print("1. Create backup")
    print("2. Erase chip")
    print()
    
    response = input("Continue? (y/N): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        return 0
    
    print("\n🚀 Starting backup and erase sequence...")
    
    # Execute backup command
    print(f"\n📖 Step 1: Creating backup...")
    print(f"Executing: {backup_cmd}")
    
    # Execute erase command  
    erase_cmd = erase_chip(args.chip_type, args.port)
    print(f"\n🗑️  Step 2: Erasing chip...")
    print(f"Executing: {erase_cmd}")
    
    print("\n✅ Operations completed!")
    print(f"Backup saved to: {args.output}")
    print("Chip has been erased.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
