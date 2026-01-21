# TROPOMI CH₄ Data Download Tool

Automated Python tool for downloading TROPOMI (TROPOspheric Monitoring Instrument) Level 2 methane (CH₄) satellite data from NASA's GES DISC.

## Features

- ✅ Multi-threaded parallel downloads 
- ✅ Live updating progress monitor 
- ✅ Automatic resume capability
- ✅ Failed file logging and retry support
- ✅ NASA Earthdata authentication handling


## Performance

**For 2 years ** (10,338 files):
- **Download time**: ~14 hours
- **Success rate**: 99.7%
- **Average speed**: 12.5 files/min
- **Total data**: ~1.2 TB

### System specifications:

256 CPU cores
504 GB RAM
10 parallel download threads
## Requirements

### System
- Linux/Unix environment
- Python 3.7+
- `wget` command-line tool

### Python Packages
```bash
pip install pandas numpy
```

### NASA Earthdata Account
1. Register at [NASA Earthdata](https://urs.earthdata.nasa.gov/users/new)
2. Approve **"NASA GESDISC DATA ARCHIVE"** and **"GES DISC"** applications
3. Wait 5-10 minutes for approval to propagate

## Quick Start

### 1. Get TROPOMI Data URLs

1. Visit [NASA GES DISC](https://disc.gsfc.nasa.gov/)
2. Search for: `S5P_L2__CH4____HiR`
3. Select date range
4. Click **"Web Links"** tab
5. Download subset URL list (`.txt` file)

### 2. Configure Script

Edit `download_tropomi.py`:

```python
USERNAME = "your_earthdata_username"
PASSWORD = "your_earthdata_password"

fname = '/path/to/your/url_list.txt'
path_save = '/path/to/save/directory/'
```

### 3. Run Download

**In tmux (recommended):**

## Configuration Options

```python
NUM_THREADS = 10        # Parallel downloads (optimal: 10)
TIMEOUT = 600           # Timeout per file (10 minutes)
UPDATE_INTERVAL = 60    # Progress update frequency (seconds)
```

## Output

### Progress Monitor (Live Updates)
```
================================================================================
TROPOMI CH4 Download - LIVE MONITOR
================================================================================

Started:  2026-01-21 00:00:00
Current:  2026-01-21 06:30:15
Elapsed:  6.50 hours

================================================================================
PROGRESS
================================================================================
  Completion:    [ 50.25%]
  ETA:           6.2 hours

================================================================================
STATISTICS
================================================================================
  Downloaded:       5195 files
  Failed:              12 files
  Timeouts:             5 files
  Remaining:        5131 files

================================================================================
PERFORMANCE
================================================================================
  Overall rate:  13.31 files/min
  Recent rate:   13.55 files/min (last 1 min)
```

### Final Summary
```
================================================================================
DOWNLOAD COMPLETE!
================================================================================

Finished: 2026-01-21 13:42:09
Total time: 13.70 hours

================================================================================
FINAL RESULTS
================================================================================
Downloaded:   10307 files
Failed:           3 files
Timeouts:        28 files
Total:        10338 files

================================================================================
SUCCESS RATE: 99.7%
================================================================================

```

## Failed Files

Failed files are automatically saved to:
```
failed_downloads.txt
```

Format:
```
[timeout    ] S5P_OFFL_L2__CH4____20240315T120159_...nc
[wget_err   ] S5P_OFFL_L2__CH4____20240622T084329_...nc
```

**To retry**: Simply re-run the script. It automatically skips existing files and only downloads failed ones.

## Troubleshooting

### Authentication Errors (401)
1. Verify Earthdata credentials
2. Check GES DISC application approval
3. Wait 10 minutes after approval
4. Verify `.netrc` file permissions (600)

### Timeouts
- Increase `TIMEOUT` value (default: 600s)
- Re-run script to retry




## File Format

Downloaded files: NetCDF (`.nc`)

Naming convention:
```
S5P_OFFL_L2__CH4____YYYYMMDDThhmmss_YYYYMMDDThhmmss_orbit_version.nc
```

Example:
```
S5P_OFFL_L2__CH4____20240101T074458_20240101T092629_32219_03_020600_20240102T234559.nc
```


```



