"""
Check for existing .netrc file and setup if needed
This is how Yejin's script worked without explicit authentication

Author: Ishi
Date: 2026-01-20
"""

import os
import stat

netrc_path = os.path.expanduser("~/.netrc")

print("="*80)
print("Checking for .netrc file (NASA Earthdata credentials)")
print("="*80)

# Check if .netrc exists
if os.path.exists(netrc_path):
    print(f"\n✓ .netrc file EXISTS at: {netrc_path}")
    
    # Check permissions
    st = os.stat(netrc_path)
    perms = stat.filemode(st.st_mode)
    print(f"  Permissions: {perms}")
    
    # Read and check content
    try:
        with open(netrc_path, 'r') as f:
            content = f.read()
        
        print(f"  Size: {len(content)} bytes")
        
        if 'urs.earthdata.nasa.gov' in content:
            print("  ✓ Contains NASA Earthdata credentials")
            
            # Check if it has your username
            if 'jnkeya' in content:
                print("  ✓ Contains your username (jnkeya)")
                print("\n  This .netrc should work for authentication!")
            else:
                print("  ⚠ Does NOT contain your username")
                print("    Might have someone else's credentials")
                
        else:
            print("  ✗ Does NOT contain NASA Earthdata credentials")
            print("    Needs to be updated")
            
    except Exception as e:
        print(f"  ✗ Cannot read .netrc: {e}")
        
else:
    print(f"\n✗ .netrc file does NOT exist at: {netrc_path}")
    print("  This is why authentication is failing!")
    print("\n  Creating .netrc file now...")
    
    USERNAME = "YOUR_EARTHDATA_USERNAME"
    PASSWORD = "YOUR_EARTHDATA_PASSWORD"
    
    netrc_content = f"""machine urs.earthdata.nasa.gov
login {USERNAME}
password {PASSWORD}
"""
    
    try:
        with open(netrc_path, 'w') as f:
            f.write(netrc_content)
        os.chmod(netrc_path, 0o600)
        print(f"\n  ✓ Created .netrc file at: {netrc_path}")
        print(f"  ✓ Set permissions to 600")
        print("\n  Now Yejin's script style should work!")
        
    except Exception as e:
        print(f"\n  ✗ Failed to create .netrc: {e}")

print("\n" + "="*80)
print("Next step: Run simplified download script (Yejin's style)")
print("="*80)
