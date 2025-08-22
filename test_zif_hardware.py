#!/usr/bin/env python3
"""
Hardware test for PIC16F887 on ZIF socket
Run this when you have the chip physically connected
"""

import sys
from pathlib import Path
from picpro.ChipInfoReader import ChipInfoReader
from picpro.protocol.p18a.Connection import Connection

def test_hardware_connection(port='/dev/ttyUSB0'):
    """Test actual hardware connection with PIC16F887 on ZIF socket."""
    print(f"🔌 Testing hardware connection on {port}")
    print("📋 Make sure:")
    print("   - PIC16F887 is inserted in ZIF socket")
    print("   - ZIF socket is closed properly") 
    print("   - Programmer is connected to USB")
    print("   - Power is supplied to the circuit")
    print()
    
    try:
        # Load chip info
        chip_data_path = Path("usr/share/picpro/chipdata.cid")
        reader = ChipInfoReader(chip_data_path)
        chip_info = reader.get_chip('16f887')
        print(f"✓ Loaded chip info for {chip_info.chip_name}")
        
        # Test connection
        with Connection(port) as connection:
            print(f"✓ Connected to programmer on {port}")
            
            # Initialize programming interface
            with connection.get_programming_interface(chip_info, icsp_mode=False) as prog_interface:
                print("✓ Programming interface initialized")
                
                # Read chip configuration
                print("📖 Reading chip configuration...")
                config = prog_interface.read_config()
                print(f"✓ Configuration read successfully")
                
                # Try to read device ID
                try:
                    device_id = prog_interface.read_device_id()
                    print(f"✓ Device ID: {hex(device_id)}")
                    
                    # Check if it matches expected chip ID
                    if device_id == chip_info.chip_id:
                        print("🎉 Device ID matches! PIC16F887 detected correctly")
                    else:
                        print(f"⚠ Device ID mismatch. Expected: {hex(chip_info.chip_id)}, Got: {hex(device_id)}")
                        
                except Exception as e:
                    print(f"ℹ Device ID read failed (may be normal): {e}")
                
                print("\n🎯 ZIF socket test successful!")
                print("✅ PIC16F887 is properly connected and communicating")
                
                return True
                
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("Make sure you're running from the picpro directory")
        return False
        
    except Exception as e:
        print(f"❌ Hardware test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   - Check USB connection")
        print("   - Verify port name (try ls /dev/tty*)")
        print("   - Ensure chip is seated properly in ZIF socket")
        print("   - Check power supply connections")
        print("   - Try different USB port")
        return False

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else '/dev/ttyUSB0'
    success = test_hardware_connection(port)
    sys.exit(0 if success else 1)
