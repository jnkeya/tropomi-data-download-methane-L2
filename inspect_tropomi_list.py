#!/usr/bin/env python3
"""
Inspect TROPOMI download URL list to understand what data will be downloaded
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re

# Path to the download list
fname = '/share/geosat-4/TROPOMI/00raw/CH4_new/subset_S5P_L2__CH4____HiR_2_20251205_044405_.txt'

print("="*80)
print("TROPOMI Download List Analysis")
print("="*80)

# Read the file
try:
    with open(fname, 'r') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    print(f"\nTotal lines in file: {total_lines}")
    
    # Show first few lines
    print("\n" + "-"*80)
    print("First 10 lines:")
    print("-"*80)
    for i, line in enumerate(lines[:10]):
        print(f"{i}: {line.strip()}")
    
    # Count data files (skip documentation, usually first 3 lines)
    data_urls = [line.strip() for line in lines[3:] if line.strip()]
    num_data_files = len(data_urls)
    
    print("\n" + "-"*80)
    print(f"Estimated data files to download: {num_data_files} (skipping first 3 documentation lines)")
    print("-"*80)
    
    # Try to extract dates from filenames
    print("\n" + "-"*80)
    print("Analyzing date coverage...")
    print("-"*80)
    
    dates = []
    for url in data_urls:  # Check all URLs
        # TROPOMI files typically have date format: YYYYMMDD
        match = re.search(r'(\d{8})', url)
        if match:
            dates.append(match.group(1))
    
    if dates:
        print(f"Total dates found: {len(dates)}")
        
        # Parse dates
        date_objs = [datetime.strptime(d, '%Y%m%d') for d in dates if len(d) == 8]
        if date_objs:
            print(f"  Earliest: {min(date_objs).strftime('%Y-%m-%d')}")
            print(f"  Latest:   {max(date_objs).strftime('%Y-%m-%d')}")
            
            # Count by year
            years = {}
            for d in date_objs:
                year = d.year
                years[year] = years.get(year, 0) + 1
            
            print("\nFiles per year:")
            for year in sorted(years.keys()):
                print(f"  {year}: {years[year]} files")
    
    # Estimate download size
    # Typical TROPOMI CH4 file is ~100-150 MB
    avg_file_size_mb = 120  # MB
    total_size_gb = (num_data_files * avg_file_size_mb) / 1024
    total_size_tb = total_size_gb / 1024
    
    print("\n" + "="*80)
    print("Download Size Estimate:")
    print("="*80)
    print(f"  Number of files: {num_data_files}")
    print(f"  Avg file size:   ~{avg_file_size_mb} MB (typical TROPOMI CH4)")
    print(f"  Total estimate:  ~{total_size_gb:.2f} GB (~{total_size_tb:.3f} TB)")
    print("\n  Available space: 10.22 TB")
    if total_size_tb < 10.22:
        print(f"  ✓ Sufficient space (need ~{total_size_tb:.3f} TB)")
    else:
        print(f"  ✗ WARNING: May not have enough space!")
    print("="*80)
    
except FileNotFoundError:
    print(f"\nERROR: File not found at {fname}")
    print("Make sure you're running this on the server with access to /share/geosat-4/")
except Exception as e:
    print(f"\nERROR: {e}")
