"""
TROPOMI CH4 Data Download - Full Dataset (2024-2025)
Using wget with NASA Earthdata authentication

Author: Ishi
Date: 2026-01-20
"""

import os
import subprocess
import pandas as pd
import numpy as np
import time
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================

USERNAME = "YOUR_EARTHDATA_USERNAME"
PASSWORD = "YOUR_EARTHDATA_PASSWORD"

path_save = '/share/geosat-4/TROPOMI/00raw/CH4_new/'
fname = '/share/geosat-4/TROPOMI/00raw/CH4_new/subset_S5P_L2__CH4____HiR_2_20260120_094804_.txt'

# ============================================================================
# Setup Authentication
# ============================================================================

print("="*80)
print("TROPOMI CH4 Full Download - 2024-2025")
print("="*80)
print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Setup .netrc
netrc_path = os.path.expanduser("~/.netrc")
netrc_content = f"""machine urs.earthdata.nasa.gov
login {USERNAME}
password {PASSWORD}
"""

try:
    with open(netrc_path, 'w') as f:
        f.write(netrc_content)
    os.chmod(netrc_path, 0o600)
    print(f"✓ Authentication configured")
except Exception as e:
    print(f"✗ Failed to setup .netrc: {e}")
    exit(1)

urs_cookies_path = os.path.expanduser("~/.urs_cookies")

# ============================================================================
# Load URL List
# ============================================================================

print("\nLoading URL list...")
flist = np.array(pd.read_csv(fname, header=None))
flist = np.sort(flist)
nflist = len(flist)

print(f"  Total entries: {nflist}")
print(f"  Data files: {nflist - 3} (skipping 3 documentation files)")

# ============================================================================
# Check Existing Files
# ============================================================================

print("\nChecking existing files...")
existing_count = 0
for i in range(3, nflist):
    URL = flist[i, 0]
    FILENAME = os.path.join(path_save, URL[-86:])
    if os.path.isfile(FILENAME):
        existing_count += 1

print(f"  Already downloaded: {existing_count} files")
print(f"  Remaining to download: {nflist - 3 - existing_count} files")

# ============================================================================
# Start Download
# ============================================================================

print("\n" + "="*80)
print("Starting download process...")
print("="*80)

downloaded = 0
skipped = 0
failed = 0
failed_files = []

start_time = time.time()
last_print_time = start_time

for i in range(3, nflist):
    
    URL = flist[i, 0]
    FILENAME = os.path.join(path_save, URL[-86:])
    
    # Skip if exists
    if os.path.isfile(FILENAME):
        skipped += 1
        continue
    
    # Download with wget
    wget_cmd = [
        'wget',
        '--load-cookies', urs_cookies_path,
        '--save-cookies', urs_cookies_path,
        '--keep-session-cookies',
        '--no-check-certificate',
        '--auth-no-challenge',
        '-q',  # Quiet mode
        '-O', FILENAME,
        URL
    ]
    
    try:
        result = subprocess.run(
            wget_cmd,
            capture_output=True,
            timeout=180  # 3 minutes per file
        )
        
        if result.returncode == 0 and os.path.isfile(FILENAME):
            file_size = os.path.getsize(FILENAME)
            
            # Check if it's a real file (at least 10 MB)
            if file_size > 10 * 1024 * 1024:
                downloaded += 1
            else:
                # Probably an error page
                os.remove(FILENAME)
                failed += 1
                failed_files.append(URL[-86:])
        else:
            failed += 1
            failed_files.append(URL[-86:])
            if os.path.isfile(FILENAME):
                os.remove(FILENAME)  # Remove failed download
        
    except subprocess.TimeoutExpired:
        failed += 1
        failed_files.append(URL[-86:])
        if os.path.isfile(FILENAME):
            os.remove(FILENAME)
    except Exception as e:
        failed += 1
        failed_files.append(URL[-86:])
    
    # Progress update every 10 seconds
    current_time = time.time()
    if current_time - last_print_time > 10:
        elapsed = current_time - start_time
        total_processed = downloaded + skipped + failed
        progress = total_processed / (nflist - 3) * 100
        
        if downloaded > 0:
            rate = downloaded / elapsed
            remaining = nflist - 3 - total_processed
            eta = remaining / rate if rate > 0 else 0
            
            print(f"[{progress:6.2f}%] Downloaded: {downloaded:5d} | Skipped: {skipped:5d} | "
                  f"Failed: {failed:3d} | Rate: {rate:.2f} files/s | ETA: {eta/60:.0f} min")
        else:
            print(f"[{progress:6.2f}%] Processed: {total_processed} | Skipped: {skipped}")
        
        last_print_time = current_time

# ============================================================================
# Final Summary
# ============================================================================

end_time = time.time()
total_time = end_time - start_time

print("\n" + "="*80)
print("Download Complete!")
print("="*80)
print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total time: {total_time/60:.1f} minutes ({total_time/3600:.2f} hours)")
print(f"\nResults:")
print(f"  Downloaded: {downloaded} files")
print(f"  Skipped (already existed): {skipped} files")
print(f"  Failed: {failed} files")

if downloaded > 0:
    avg_rate = downloaded / total_time
    print(f"\nPerformance:")
    print(f"  Average rate: {avg_rate:.2f} files/second")
    print(f"  Average time per file: {total_time/downloaded:.2f} seconds")

if failed > 0:
    failed_list_file = os.path.join(path_save, 'failed_downloads.txt')
    with open(failed_list_file, 'w') as f:
        for fname_failed in failed_files:
            f.write(fname_failed + '\n')
    
    print(f"\n  Failed files list saved to: {failed_list_file}")
    print(f"  First 10 failed files:")
    for f in failed_files[:10]:
        print(f"    {f}")

print("\n" + "="*80)
print("All done!")
print("="*80)
