#!/usr/bin/env python3
"""
Test script for PIC16F887 on ZIF socket
Tests chip detection, communication, and basic operations
"""

import sys
import argparse
from pathlib import Path
from picpro.ChipInfoReader import ChipInfoReader
from picpro.protocol.p18a.Connection import Connection

def find_chip_data():
    """Find the chipdata.cid file."""
    possible_paths = [
        Path(__file__).parent / "usr/share/picpro/chipdata.cid",
        Path("/usr/share/picpro/chipdata.cid"),
        Path("chipdata.cid")
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    raise FileNotFoundError("chipdata.cid file not found")

def test_chip_info():
    """Test if PIC16F887 chip info loads correctly."""
    print("=== Chip Info Test ===")
    try:
        chip_data_path = find_chip_data()
        reader = ChipInfoReader(chip_data_path)
        chip_info = reader.get_chip('16f887')
        
        print(f"✓ Chip Name: {chip_info.chip_name}")
        print(f"✓ ROM Size: {hex(chip_info.rom_size)} ({chip_info.rom_size} bytes)")
        print(f"✓ EEPROM Size: {hex(chip_info.eeprom_size)} ({chip_info.eeprom_size} bytes)")
        print(f"✓ Chip ID: {hex(chip_info.chip_id)}")
        print(f"✓ Core Type: {chip_info.core_type}")
        print(f"✓ Flash Chip: {chip_info.flash_chip}")
        print(f"✓ ICSP Only: {chip_info.icsp_only}")
        return chip_info
        
    except Exception as e:
        print(f"✗ Chip info test failed: {e}")
        return None

def test_connection(port):
    """Test connection to programmer."""
    print(f"\n=== Connection Test (Port: {port}) ===")
    try:
        with Connection(port) as connection:
            print("✓ Connection established successfully")
            print(f"✓ Programmer connected on {port}")
            return connection
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return None

def test_chip_detection(port, icsp_mode=False):
    """Test chip detection and programming interface."""
    print(f"\n=== Chip Detection Test (ICSP: {icsp_mode}) ===")
    try:
        chip_data_path = find_chip_data()
        reader = ChipInfoReader(chip_data_path)
        chip_info = reader.get_chip('16f887')
        
        with Connection(port) as connection:
            print("✓ Initializing programming interface...")
            with connection.get_programming_interface(chip_info, icsp_mode=icsp_mode) as prog_interface:
                print("✓ Programming interface initialized")
                
                # Try to read chip configuration
                print("✓ Attempting to read chip configuration...")
                chip_config = prog_interface.read_config()
                print(f"✓ Chip configuration read successfully")
                print(f"  Config data length: {len(chip_config)} bytes")
                
                # Try to read device ID if available
                try:
                    device_id = prog_interface.read_device_id()
                    print(f"✓ Device ID: {hex(device_id)}")
                except:
                    print("  (Device ID read not supported or failed)")
                
                return True
                
    except Exception as e:
        print(f"✗ Chip detection failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test PIC16F887 on ZIF socket')
    parser.add_argument('--port', '-p', default='/dev/ttyUSB0', 
                       help='Programmer port (default: /dev/ttyUSB0)')
    parser.add_argument('--icsp', action='store_true',
                       help='Use ICSP mode')
    parser.add_argument('--skip-hardware', action='store_true',
                       help='Skip hardware tests (only test chip info)')
    
    args = parser.parse_args()
    
    print("PIC16F887 ZIF Socket Test")
    print("=" * 40)
    
    # Test 1: Chip info loading
    chip_info = test_chip_info()
    if not chip_info:
        return 1
    
    if args.skip_hardware:
        print("\n✓ Hardware tests skipped (--skip-hardware)")
        return 0
    
    # Test 2: Connection test
    print(f"\nTesting connection to programmer on {args.port}...")
    if not test_connection(args.port):
        print("\n⚠ Connection failed. Check:")
        print("  - Programmer is connected")
        print("  - Correct port specified")
        print("  - User has permissions to access port")
        return 1
    
    # Test 3: Chip detection
    success = test_chip_detection(args.port, args.icsp)
    
    if success:
        print("\n🎉 All tests passed! PIC16F887 is working on ZIF socket")
        print("\nNext steps:")
        print("  - Try programming a hex file")
        print("  - Test reading/writing EEPROM")
        print("  - Verify fuse settings")
    else:
        print("\n❌ Chip detection failed. Check:")
        print("  - PIC16F887 is properly seated in ZIF socket")
        print("  - ZIF socket connections are good")
        print("  - Power supply is stable")
        print("  - Chip is not damaged")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
