"""
TROPOMI CH4 Data Download using wget
wget handles NASA Earthdata authentication redirects better than requests

Author: Ishi
Date: 2026-01-20
"""

import os
import subprocess
import pandas as pd
import numpy as np

# ============================================================================
# Credentials
# ============================================================================

USERNAME = "YOUR_EARTHDATA_USERNAME"
PASSWORD = "YOUR_EARTHDATA_PASSWORD"

# ============================================================================
# Setup .netrc file
# ============================================================================

print("="*80)
print("TROPOMI CH4 Download - Using wget")
print("="*80)

netrc_path = os.path.expanduser("~/.netrc")

print("\nSetting up .netrc authentication...")

netrc_content = f"""machine urs.earthdata.nasa.gov
login {USERNAME}
password {PASSWORD}
"""

try:
    with open(netrc_path, 'w') as f:
        f.write(netrc_content)
    os.chmod(netrc_path, 0o600)
    print(f"✓ Created .netrc file")
except Exception as e:
    print(f"✗ Failed: {e}")
    exit(1)

# Also create .urs_cookies file for session management
urs_cookies_path = os.path.expanduser("~/.urs_cookies")
print(f"✓ Will use cookies file: {urs_cookies_path}")

# ============================================================================
# Load URL List
# ============================================================================

path_save = '/share/geosat-4/TROPOMI/00raw/CH4_new/'
fname = '/share/geosat-4/TROPOMI/00raw/CH4_new/subset_S5P_L2__CH4____HiR_2_20260120_094804_.txt'

print("\nLoading URL list...")
flist = np.array(pd.read_csv(fname, header=None))
flist = np.sort(flist)
nflist = len(flist)

print(f"Total entries: {nflist}")

# ============================================================================
# Test Download ONE file with wget
# ============================================================================

print("\n" + "="*80)
print("Testing download with wget...")
print("="*80)

test_index = 3
test_url = flist[test_index, 0]
test_filename = os.path.join(path_save, test_url[-86:])

print(f"\nTest URL: {test_url[:80]}...")
print(f"Save to: {test_filename}")

# Remove if exists
if os.path.isfile(test_filename):
    print("\nRemoving existing file for clean test...")
    os.remove(test_filename)

print("\nDownloading with wget...")

# wget command with proper NASA Earthdata settings
wget_cmd = [
    'wget',
    '--load-cookies', urs_cookies_path,
    '--save-cookies', urs_cookies_path,
    '--keep-session-cookies',
    '--no-check-certificate',  # Some NASA servers have certificate issues
    '--auth-no-challenge',
    '-O', test_filename,
    test_url
]

try:
    result = subprocess.run(
        wget_cmd,
        capture_output=True,
        text=True,
        timeout=300
    )
    
    if result.returncode == 0:
        if os.path.isfile(test_filename):
            file_size = os.path.getsize(test_filename) / (1024**2)
            print(f"\n✓ Download successful!")
            print(f"  File size: {file_size:.2f} MB")
            
            # Check if it's a real file (not HTML error page)
            if file_size < 1:
                print("\n  ⚠ Warning: File is very small, might be an error page")
                with open(test_filename, 'r') as f:
                    print(f"  First 200 chars: {f.read(200)}")
        else:
            print("\n✗ Download failed - file not created")
    else:
        print(f"\n✗ wget failed with return code: {result.returncode}")
        print(f"\nSTDOUT:\n{result.stdout}")
        print(f"\nSTDERR:\n{result.stderr}")
        
except subprocess.TimeoutExpired:
    print("\n✗ Download timed out after 5 minutes")
except Exception as e:
    print(f"\n✗ Error: {e}")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "="*80)
print("Test Complete!")
print("="*80)

if os.path.isfile(test_filename):
    file_size = os.path.getsize(test_filename) / (1024**2)
    if file_size > 10:  # At least 10 MB means it's probably real data
        print("\n✓ SUCCESS - wget authentication working!")
        print("\nNext: Run full download with wget")
    else:
        print("\n✗ File downloaded but too small - likely authentication error")
        print("  Check if file contains HTML error message")
else:
    print("\n✗ Test failed - no file created")

print("="*80)
