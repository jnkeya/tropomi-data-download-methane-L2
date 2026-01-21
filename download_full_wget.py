"""
TROPOMI CH4 Download - Threading for 2024-2025 data
Date: 2026-01-20
"""

import os
import subprocess
import pandas as pd
import numpy as np
import time
import sys
from datetime import datetime
from threading import Thread, Lock
from queue import Queue

# ============================================================================
# Configuration
# ============================================================================

USERNAME = "YOUR_EARTHDATA_USERNAME"
PASSWORD = "YOUR_EARTHDATA_PASSWORD"

path_save = '/share/geosat-4/TROPOMI/00raw/CH4_new/'
fname = '/share/geosat-4/TROPOMI/00raw/CH4_new/subset_S5P_L2__CH4____HiR_2_20260120_094804_.txt'

NUM_THREADS = 10
TIMEOUT = 600  # 10 minutes
UPDATE_INTERVAL = 600  # Update display every 10 minutes

# ============================================================================
# Setup
# ============================================================================

print("="*80)
print("TROPOMI CH4 FULL DOWNLOAD - 2024-2025")
print("="*80)
print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Threads: {NUM_THREADS}")
print(f"Timeout: {TIMEOUT}s per file")
print(f"Display updates: Every {UPDATE_INTERVAL/60:.0f} minutes")

# Setup .netrc
netrc_path = os.path.expanduser("~/.netrc")
netrc_content = f"""machine urs.earthdata.nasa.gov
login {USERNAME}
password {PASSWORD}
"""
with open(netrc_path, 'w') as f:
    f.write(netrc_content)
os.chmod(netrc_path, 0o600)
print("✓ Authentication configured")

urs_cookies_path = os.path.expanduser("~/.urs_cookies")

# ============================================================================
# Load URLs
# ============================================================================

print("\nLoading URL list...")
flist = np.array(pd.read_csv(fname, header=None))
flist = np.sort(flist)
nflist = len(flist)

print(f"  Total entries: {nflist}")
print(f"  Data files: {nflist - 3}")

# Check existing
existing_count = 0
for i in range(3, nflist):
    URL = flist[i, 0]
    FILENAME = os.path.join(path_save, URL[-86:])
    if os.path.isfile(FILENAME):
        existing_count += 1

print(f"  Already downloaded: {existing_count}")

# Build queue
download_queue = Queue()
for i in range(3, nflist):
    URL = flist[i, 0]
    FILENAME = os.path.join(path_save, URL[-86:])
    if not os.path.isfile(FILENAME):
        download_queue.put((i, URL, FILENAME))

total_to_download = download_queue.qsize()
print(f"  To download: {total_to_download}")
print("\n" + "="*80)
print("Starting download... Monitor will appear in 10 minutes")
print("="*80 + "\n")

time.sleep(3)

# ============================================================================
# Shared State
# ============================================================================

stats_lock = Lock()
downloaded = 0
failed = 0
timeouts = 0
errors = 0
failed_files = []
start_time = time.time()
num_lines_printed = 0

# ============================================================================
# Download Worker
# ============================================================================

def download_worker(thread_id):
    global downloaded, failed, timeouts, errors, failed_files
    
    while not download_queue.empty():
        try:
            idx, url, filename = download_queue.get(timeout=1)
        except:
            break
        
        wget_cmd = [
            'wget', '--load-cookies', urs_cookies_path,
            '--save-cookies', urs_cookies_path,
            '--keep-session-cookies', '--no-check-certificate',
            '--auth-no-challenge', '-q', '-O', filename, url
        ]
        
        try:
            result = subprocess.run(wget_cmd, capture_output=True, timeout=TIMEOUT)
            
            if result.returncode == 0 and os.path.isfile(filename):
                file_size = os.path.getsize(filename)
                if file_size > 10 * 1024:
                    with stats_lock:
                        downloaded += 1
                else:
                    os.remove(filename)
                    with stats_lock:
                        failed += 1
                        failed_files.append(('small', url[-86:]))
            else:
                if os.path.isfile(filename):
                    os.remove(filename)
                with stats_lock:
                    failed += 1
                    failed_files.append(('wget_err', url[-86:]))
        except subprocess.TimeoutExpired:
            if os.path.isfile(filename):
                os.remove(filename)
            with stats_lock:
                timeouts += 1
                failed_files.append(('timeout', url[-86:]))
        except:
            with stats_lock:
                errors += 1
                failed_files.append(('error', url[-86:]))
        
        download_queue.task_done()

# ============================================================================
# Progress Monitor
# ============================================================================

def progress_monitor():
    global num_lines_printed
    last_downloaded = 0
    
    while True:
        time.sleep(UPDATE_INTERVAL)
        
        with stats_lock:
            curr_down = downloaded
            curr_fail = failed
            curr_timeout = timeouts
            curr_error = errors
            
            total_processed = curr_down + curr_fail + curr_timeout + curr_error
            
            if total_processed >= total_to_download:
                break
            
            elapsed = time.time() - start_time
            rate = curr_down / elapsed if elapsed > 0 else 0
            progress = total_processed / total_to_download * 100
            remaining = total_to_download - total_processed
            eta_seconds = remaining / rate if rate > 0 else 0
            
            files_since_last = curr_down - last_downloaded
            recent_rate = files_since_last / (UPDATE_INTERVAL/60) if files_since_last > 0 else 0
            
            # Move cursor up
            if num_lines_printed > 0:
                sys.stdout.write(f'\033[{num_lines_printed}A')
            
            # Build display
            output = []
            output.append("="*80)
            output.append("TROPOMI CH4 Download - LIVE MONITOR")
            output.append("="*80)
            output.append("")
            output.append(f"Started:  {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
            output.append(f"Current:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            output.append(f"Elapsed:  {elapsed/3600:.2f} hours ({elapsed/60:.1f} minutes)")
            output.append("")
            output.append("="*80)
            output.append("PROGRESS")
            output.append("="*80)
            output.append(f"  Completion:    [{progress:6.2f}%]")
            output.append(f"  ETA:           {eta_seconds/3600:.1f} hours ({eta_seconds/60:.0f} minutes)")
            output.append("")
            output.append("="*80)
            output.append("STATISTICS")
            output.append("="*80)
            output.append(f"  Downloaded:    {curr_down:7d} files")
            output.append(f"  Failed:        {curr_fail:7d} files")
            output.append(f"  Timeouts:      {curr_timeout:7d} files")
            output.append(f"  Errors:        {curr_error:7d} files")
            output.append(f"  Remaining:     {remaining:7d} files")
            output.append("")
            output.append("="*80)
            output.append("PERFORMANCE")
            output.append("="*80)
            output.append(f"  Overall rate:  {rate*60:.2f} files/min ({rate:.4f} files/sec)")
            output.append(f"  Recent rate:   {recent_rate:.2f} files/min (last {UPDATE_INTERVAL/60:.0f} min)")
            
            if failed_files and len(failed_files) > 0:
                output.append("")
                output.append("="*80)
                output.append("RECENT FAILURES (last 3)")
                output.append("="*80)
                for fail_type, fname in failed_files[-3:]:
                    output.append(f"  [{fail_type:10s}] {fname[:60]}")
            
            output.append("")
            output.append("="*80)
            output.append(f"Next update in {UPDATE_INTERVAL/60:.0f} minutes | Press Ctrl+C to stop")
            output.append("="*80)
            
            # Print with line clearing
            for line in output:
                sys.stdout.write(line + '\033[K\n')
            
            sys.stdout.flush()
            num_lines_printed = len(output)
            last_downloaded = curr_down

# ============================================================================
# Start Download
# ============================================================================

threads = []
for i in range(NUM_THREADS):
    t = Thread(target=download_worker, args=(i,), daemon=True)
    t.start()
    threads.append(t)

monitor = Thread(target=progress_monitor, daemon=True)
monitor.start()

try:
    for t in threads:
        t.join()
    time.sleep(2)
except KeyboardInterrupt:
    print("\n\n" + "="*80)
    print("⚠️  Download interrupted by user!")
    print("="*80)
    print("Progress saved. Re-run to resume.")
    sys.exit(0)

# ============================================================================
# Final Summary
# ============================================================================

end_time = time.time()
total_time = end_time - start_time

print("\n\n" + "="*80)
print("DOWNLOAD COMPLETE!")
print("="*80)
print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total time: {total_time/3600:.2f} hours ({total_time/60:.1f} minutes)")

print(f"\n" + "="*80)
print("FINAL RESULTS")
print("="*80)
print(f"Downloaded:  {downloaded:7d} files")
print(f"Failed:      {failed:7d} files")
print(f"Timeouts:    {timeouts:7d} files")
print(f"Errors:      {errors:7d} files")
print(f"Total:       {downloaded+failed+timeouts+errors:7d} files")

if downloaded > 0:
    print(f"\n" + "="*80)
    print("PERFORMANCE")
    print("="*80)
    print(f"Average rate: {downloaded/total_time*60:.2f} files/min")
    print(f"Avg time/file: {total_time/downloaded:.1f} seconds")

# Save failed files
if failed_files:
    failed_list = os.path.join(path_save, 'failed_downloads.txt')
    with open(failed_list, 'w') as f:
        f.write(f"# Failed TROPOMI Downloads\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total: {len(failed_files)}\n\n")
        for fail_type, fname in failed_files:
            f.write(f"[{fail_type:10s}] {fname}\n")
    
    print(f"\n" + "="*80)
    print("FAILED FILES")
    print("="*80)
    print(f"Saved to: {failed_list}")
    
    failure_types = {}
    for fail_type, _ in failed_files:
        failure_types[fail_type] = failure_types.get(fail_type, 0) + 1
    
    print("\nBreakdown:")
    for ftype, count in sorted(failure_types.items()):
        print(f"  {ftype:10s}: {count:5d} files")

success_rate = (downloaded / (downloaded + failed + timeouts + errors) * 100) if (downloaded + failed + timeouts + errors) > 0 else 0

print(f"\n" + "="*80)
print(f"SUCCESS RATE: {success_rate:.1f}%")
print("="*80)

if success_rate >= 90:
    print("✓✓✓ EXCELLENT!")
elif success_rate >= 70:
    print("✓✓ GOOD!")
else:
    print("⚠ Re-run for failed files")

print("\n" + "="*80)
print("Done! Failed files can be retried by re-running this script.")
print("="*80)
