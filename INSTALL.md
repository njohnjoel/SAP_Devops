# SAP DevOps Installation Guide

## Overview
The `install_devops.py` script automates downloading and installing SAP DevOps from GitHub releases with automatic version management and symbolic linking.

## Installation

### Basic Usage
```bash
python3 /path/to/install_devops.py <version>
```

### Example
```bash
python3 install_devops.py 1.0.0
```

## What It Does

1. **Validates version** - Ensures semantic versioning format (X.Y.Z)
2. **Downloads** - Pulls `sap-devops-{version}.zip` from GitHub releases
3. **Extracts** - Unzips to `/proj/sap/software/devops/{version}/`
4. **Creates symlink** - Links `/proj/sap/software/devops/basis/` to latest version
5. **Verifies** - Confirms installation and symlink are correct

## Directory Structure

After installation, the following structure is created:
```
/proj/sap/software/devops/
├── 1.0.0/
│   ├── sap-devops/
│   │   ├── src/
│   │   ├── pom.xml
│   │   └── ...
│   └── ...
├── 1.0.1/
│   └── ...
└── basis -> 1.0.1/  (symlink to latest)
```

## Version Management

### Installing Multiple Versions
Each version is installed independently:
```bash
python3 install_devops.py 1.0.0
python3 install_devops.py 1.0.1
python3 install_devops.py 1.1.0
```

### Updating Symlink
The `basis` symlink automatically points to the most recently installed version. When you install version 1.0.1 after 1.0.0:
- Old symlink: `basis -> /proj/sap/software/devops/1.0.0/`
- New symlink: `basis -> /proj/sap/software/devops/1.0.1/`

### Accessing Latest Version
```bash
cd /proj/sap/software/devops/basis
# You're now in the latest installed version
```

## Error Handling

The script provides clear error messages for:
- Invalid version format
- Missing release on GitHub
- Network connectivity issues
- File system permission errors
- Corrupted zip files

## Requirements

- Python 3.x
- Network access to GitHub
- Write permissions to `/proj/sap/software/devops/`
- Adequate disk space for extracted artifacts

## Troubleshooting

### Release Not Found
Ensure the release has been created on GitHub:
- Tag format: `v{version}` (e.g., `v1.0.0`)
- Release must include the zip artifact: `sap-devops-{version}.zip`

### Permission Denied
Create the base directory with proper permissions:
```bash
sudo mkdir -p /proj/sap/software/devops
sudo chmod 755 /proj/sap/software/devops
```

### Symlink Already Exists
If `/proj/sap/software/devops/basis` is a regular directory instead of symlink, remove it manually:
```bash
sudo rm -rf /proj/sap/software/devops/basis
# Then re-run the installer
```

## Examples

### Install version 1.0.0
```bash
python3 install_devops.py 1.0.0
```

Expected output:
```
2026-06-22 23:00:36,007 - INFO - Starting installation of SAP DevOps version 1.0.0
2026-06-22 23:00:36,011 - INFO - Created/verified directory: /proj/sap/software/devops/1.0.0
2026-06-22 23:00:36,011 - INFO - Downloading from: https://github.com/njohnjoel/SAP_Devops/releases/download/v1.0.0/sap-devops-1.0.0.zip
2026-06-22 23:00:40,000 - INFO - Successfully downloaded to: sap-devops-1.0.0.zip
2026-06-22 23:00:40,500 - INFO - Extracting sap-devops-1.0.0.zip to /proj/sap/software/devops/1.0.0
2026-06-22 23:00:41,000 - INFO - Successfully extracted archive
2026-06-22 23:00:41,100 - INFO - Created symlink: /proj/sap/software/devops/basis -> /proj/sap/software/devops/1.0.0
2026-06-22 23:00:41,200 - INFO - Installation verified successfully
2026-06-22 23:00:41,300 - INFO - Cleaned up temporary zip file
```

### Upgrade to version 1.0.1
```bash
python3 install_devops.py 1.0.1
```

The `basis` symlink now points to version 1.0.1, while version 1.0.0 remains on disk for rollback if needed.
