# GitHub Repository Setup Instructions

Complete guide to upload your TROPOMI download scripts to GitHub.

## Method 1: Web Interface (Easiest)

### Step 1: Create Repository on GitHub

1. Go to https://github.com and log in
2. Click the **"+"** icon (top-right) → **"New repository"**
3. Fill in:
   - **Repository name:** `tropomi-data-download`
   - **Description:** `Python scripts for downloading TROPOMI CH4 satellite data from NASA GES DISC`
   - **Visibility:** Public (or Private if you prefer)
   - **DON'T** check "Add a README file" (we already have one)
   - **DON'T** add .gitignore or license (we have those too)
4. Click **"Create repository"**

### Step 2: Upload Files via Web

After creating the repository, GitHub shows an empty page. Look for:

**"uploading an existing file"** link

Click it and upload these files:
- `README.md`
- `requirements.txt`
- `.gitignore`
- `LICENSE`
- `inspect_tropomi_list.py`
- `test_download_wget.py`
- `download_full_wget.py`
- `check_netrc.py`

**Commit message:** `Initial commit: TROPOMI CH4 download scripts`

Click **"Commit changes"**

### Step 3: Remove Credentials from Scripts (IMPORTANT!)

Before uploading, **remove your actual credentials** from the Python scripts:

In `test_download_wget.py` and `download_full_wget.py`, change:
```python
USERNAME = "jnkeya"
PASSWORD = "Q,,UrD!79$TUA6i"
```

To:
```python
USERNAME = "YOUR_EARTHDATA_USERNAME"
PASSWORD = "YOUR_EARTHDATA_PASSWORD"
```

Or use environment variables:
```python
import os
USERNAME = os.getenv('EARTHDATA_USER', 'YOUR_EARTHDATA_USERNAME')
PASSWORD = os.getenv('EARTHDATA_PASS', 'YOUR_EARTHDATA_PASSWORD')
```

**⚠️ NEVER commit real credentials to GitHub! ⚠️**

---

## Method 2: Command Line (Advanced)

### Prerequisites
- Git installed on your system
- GitHub account

### Step 1: Initialize Git Repository

```bash
cd /path/to/tropomi-data-download

# Initialize git
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: TROPOMI CH4 download scripts"
```

### Step 2: Create Repository on GitHub

1. Go to https://github.com
2. Click "+" → "New repository"
3. Name: `tropomi-data-download`
4. **DON'T** initialize with README
5. Click "Create repository"

### Step 3: Connect and Push

```bash
# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/tropomi-data-download.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### Authentication

**If using HTTPS and it asks for password:**

GitHub no longer accepts passwords for git operations. Use a **Personal Access Token**:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Select scopes: `repo` (all)
4. Copy the token
5. Use token as password when pushing

**Or use SSH:**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy output and add to GitHub → Settings → SSH Keys

# Change remote to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/tropomi-data-download.git
```

---

## Method 3: GitHub Desktop (Mac/Windows)

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Sign in to GitHub
3. File → Add Local Repository → Select your folder
4. Click "Publish repository"
5. Choose name, description, and visibility
6. Click "Publish repository"

---

## Post-Upload Checklist

After uploading, verify:

- ✅ README.md displays correctly on the repository page
- ✅ No credentials visible in any files
- ✅ All Python scripts are present
- ✅ .gitignore is working (no .nc files, .netrc, or logs committed)
- ✅ LICENSE file is present

## Updating Your Repository

When you make changes:

```bash
# Stage changes
git add .

# Commit with message
git commit -m "Update: describe your changes"

# Push to GitHub
git push
```

## Making Repository Professional

### Add Topics/Tags
1. Go to your repository on GitHub
2. Click "⚙️ About" (top right)
3. Add topics: `tropomi`, `satellite-data`, `methane`, `nasa`, `atmospheric-science`, `remote-sensing`

### Add Repository Description
In the "About" section, add:
> Python scripts for downloading TROPOMI CH4 satellite data from NASA GES DISC for atmospheric methane monitoring research

### Enable Issues
Settings → Features → ✅ Issues

### Add GitHub Actions (Optional)
Create `.github/workflows/python-test.yml` for automated testing

---

## Troubleshooting

### "Authentication failed"
- Use Personal Access Token instead of password
- Or set up SSH keys

### "Remote repository already exists"
- The repository name is taken
- Choose a different name or use your existing repository

### "Permission denied"
- Check if you're logged into the correct GitHub account
- Verify repository permissions

### Large files rejected
- GitHub has 100MB file limit
- Don't commit data files (they're in .gitignore)
- Only commit Python scripts and documentation

---

## Your Repository URL

After setup, your repository will be at:
```
https://github.com/YOUR_USERNAME/tropomi-data-download
```

Share this link in your research papers or with colleagues!

---

## Optional: Add GitHub Pages Documentation

Create beautiful documentation website:

1. Settings → Pages
2. Source: Deploy from branch → `main` → `/docs`
3. Create `/docs/index.md` with your documentation
4. Your site will be at: `https://YOUR_USERNAME.github.io/tropomi-data-download/`

---

**Questions?**

- GitHub Help: https://docs.github.com/
- Git Guide: https://git-scm.com/book/en/v2

**Done! Your repository is now live! 🎉**
