# TROPOMI CH₄ Data Download Scripts

Python scripts for downloading TROPOMI (TROPOspheric Monitoring Instrument) Level 2 methane (CH₄) satellite data from NASA's GES DISC (Goddard Earth Sciences Data and Information Services Center).

## Overview

This repository provides tools for bulk downloading TROPOMI CH₄ satellite data for atmospheric methane monitoring research. The scripts handle NASA Earthdata authentication, progress tracking, error handling, and resume capability for large-scale downloads.

## Features

- ✅ **NASA Earthdata Authentication** - Automated credential management via `.netrc`
- ✅ **Wget-based Downloads** - Robust handling of NASA's authentication redirects
- ✅ **Resume Capability** - Automatically skips already downloaded files
- ✅ **Progress Tracking** - Real-time progress with download rate and ETA
- ✅ **Error Handling** - Retry logic and failed file logging
- ✅ **File Validation** - Checks file sizes to detect download errors


### NASA Earthdata Account
1. Register at [NASA Earthdata Login](https://urs.earthdata.nasa.gov/users/new)
2. Approve **GES DISC** application access:
   - Login to [Earthdata](https://urs.earthdata.nasa.gov/home)
   - Go to **Applications → Authorized Apps**
   - Approve **"NASA GESDISC DATA ARCHIVE"** and **"GES DISC"**

## Getting Started

### 1. Get TROPOMI Data URLs

1. Visit [NASA GES DISC](https://disc.gsfc.nasa.gov/)
2. Search for **"S5P_L2__CH4____HiR"** (TROPOMI Level 2 Methane)
3. Select your desired date range
4. Click **"Web Links"** tab (not Direct S3 Links)
5. Download the **subset URL list** as a `.txt` file

### 2. Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/tropomi-data-download.git
cd tropomi-data-download
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Inspect Your Download List

Check what data you'll be downloading and estimate storage needs:

```bash
python inspect_tropomi_list.py
```

**Edit the script** to point to your `.txt` file:
```python
fname = '/path/to/your/subset_S5P_L2__CH4____HiR_2_YYYYMMDD_HHMMSS_.txt'
```

**Output:**
- Total number of files
- Date range coverage
- Files per year
- Estimated download size

### Step 2: Test Single File Download

Verify authentication works before downloading all files:

```bash
python test_download_wget.py
```

**Configure:**
```python
USERNAME = "your_earthdata_username"
PASSWORD = "your_earthdata_password"
fname = '/path/to/your/url_list.txt'
path_save = '/path/to/save/directory/'
```

**Success:** File > 10 MB downloaded ✓

### Step 3: Run Full Download

Download all TROPOMI files:

```bash
# Interactive mode
python download_full_wget.py

# Background mode (recommended)
nohup python download_full_wget.py > download_log.txt 2>&1 &

# Monitor progress
tail -f download_log.txt
```

**Configure the script:**
```python
USERNAME = "your_earthdata_username"
PASSWORD = "your_earthdata_password"
fname = '/path/to/subset_S5P_L2__CH4____HiR_2_YYYYMMDD_HHMMSS_.txt'
path_save = '/path/to/save/directory/'
```

## Scripts Description

### `inspect_tropomi_list.py`
Analyzes download URL lists to provide:
- File counts and date coverage
- Storage size estimates
- Data availability checks

### `test_download_wget.py`
Single-file download test to verify:
- NASA Earthdata authentication
- Network connectivity
- Download functionality

### `download_full_wget.py`
**Main download script** with features:
- Bulk download of all files in URL list
- Progress tracking (updates every 10 seconds)
- Automatic resume (skips existing files)
- Failed file logging
- Performance statistics

### `check_netrc.py`
Utility to verify `.netrc` authentication setup:
- Checks if `.netrc` exists
- Validates NASA Earthdata credentials
- Creates `.netrc` if missing

## Authentication Methods

### Method 1: .netrc File (Recommended)

The scripts automatically create a `.netrc` file with your credentials:

```bash
# Created automatically by scripts at:
~/.netrc

# Format:
machine urs.earthdata.nasa.gov
login your_username
password your_password
```

**Permissions:** Must be `600` (read/write for owner only)

### Method 2: Manual .netrc Setup

```bash
echo "machine urs.earthdata.nasa.gov" > ~/.netrc
echo "login your_username" >> ~/.netrc
echo "password your_password" >> ~/.netrc
chmod 600 ~/.netrc
```

## Storage Requirements

**Example: 2024-2025 Dataset**
- Files: ~10,338 files
- Size: ~1.18 TB
- Average file size: ~120 MB
- Coverage: Daily global CH₄ observations

**Check available space:**
```bash
df -h /your/download/path
```

## Troubleshooting

### Authentication Errors (401)

**Issue:** `wget` returns 401 Unauthorized

**Solutions:**
1. Verify credentials are correct
2. Check GES DISC application approval status
3. Wait 5-10 minutes after approving applications
4. Run `python check_netrc.py` to verify setup

### Connection Issues

**Issue:** Download fails or times out

**Solutions:**
1. Check internet connectivity
2. Try downloading manually with `wget` to test
3. Increase timeout in script (default: 180 seconds)

### Small File Sizes

**Issue:** Downloaded files are < 10 MB (likely HTML error pages)

**Solutions:**
1. Re-check authentication
2. Verify URL list is current (valid for 2 days)
3. Download new URL list from GES DISC

### Special Characters in Password

**Issue:** Password contains special characters causing issues

**Solutions:**
1. Use single quotes in shell: `'password'`
2. Escape special characters: `\$`, `\!`
3. Consider changing password to alphanumeric

## Data Format

Downloaded files are NetCDF format (`.nc`) with naming convention:

```
S5P_OFFL_L2__CH4____YYYYMMDDThhmmss_YYYYMMDDThhmmss_orbit_version.nc
```

**Example:**
```
S5P_OFFL_L2__CH4____20240101T074458_20240101T092629_32219_03_020600_20240102T234559.nc
```

## File Structure

```
tropomi-data-download/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── inspect_tropomi_list.py      # URL list analyzer
├── test_download_wget.py        # Single file test
├── download_full_wget.py        # Main download script
└── check_netrc.py               # Authentication checker
```

**Last Updated:** January 2026
