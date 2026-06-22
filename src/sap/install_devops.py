import sys
import os
import urllib.request
import urllib.error
import zipfile
import shutil
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

GITHUB_REPO = "njohnjoel/SAP_Devops"
BASE_INSTALL_PATH = "/proj/sap/software/devops"
SYMLINK_NAME = "basis"


def validate_version(version: str) -> bool:
    parts = version.split('.')
    if len(parts) != 3:
        return False
    return all(part.isdigit() for part in parts)


def construct_download_url(version: str) -> str:
    return f"https://github.com/{GITHUB_REPO}/releases/download/v{version}/sap-devops-{version}.zip"


def download_release(version: str, output_file: str) -> bool:
    url = construct_download_url(version)
    logger.info(f"Downloading from: {url}")
    
    try:
        urllib.request.urlretrieve(url, output_file)
        logger.info(f"Successfully downloaded to: {output_file}")
        return True
    except urllib.error.URLError as e:
        logger.error(f"Download failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during download: {e}")
        return False


def setup_directories(version: str) -> str:
    install_dir = os.path.join(BASE_INSTALL_PATH, version)
    
    try:
        os.makedirs(install_dir, exist_ok=True)
        logger.info(f"Created/verified directory: {install_dir}")
        return install_dir
    except OSError as e:
        logger.error(f"Failed to create directory {install_dir}: {e}")
        return None


def extract_zip(zip_file: str, extract_to: str) -> bool:
    try:
        logger.info(f"Extracting {zip_file} to {extract_to}")
        
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        logger.info(f"Successfully extracted archive")
        return True
    except zipfile.BadZipFile:
        logger.error(f"Invalid zip file: {zip_file}")
        return False
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return False


def manage_symlink(version: str, target_dir: str) -> bool:
    symlink_path = os.path.join(BASE_INSTALL_PATH, SYMLINK_NAME)
    
    try:
        if os.path.islink(symlink_path):
            old_target = os.readlink(symlink_path)
            logger.info(f"Existing symlink points to: {old_target}")
            os.remove(symlink_path)
            logger.info(f"Removed old symlink")
        elif os.path.exists(symlink_path):
            logger.error(f"{symlink_path} exists but is not a symlink. Remove manually.")
            return False
        
        os.symlink(target_dir, symlink_path)
        logger.info(f"Created symlink: {symlink_path} -> {target_dir}")
        return True
        
    except OSError as e:
        logger.error(f"Failed to manage symlink: {e}")
        return False


def verify_installation(version: str, install_dir: str) -> bool:
    try:
        if not os.path.isdir(install_dir):
            logger.error(f"Installation directory not found: {install_dir}")
            return False
        
        symlink_path = os.path.join(BASE_INSTALL_PATH, SYMLINK_NAME)
        if not os.path.islink(symlink_path):
            logger.error(f"Symlink not found: {symlink_path}")
            return False
        
        actual_target = os.path.realpath(symlink_path)
        expected_target = os.path.realpath(install_dir)
        
        if actual_target != expected_target:
            logger.error(f"Symlink points to wrong location. Expected: {expected_target}, Got: {actual_target}")
            return False
        
        logger.info(f"Installation verified successfully")
        return True
        
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        logger.error("Usage: python3 install_devops.py <version>")
        logger.error("Example: python3 install_devops.py 1.0.0")
        sys.exit(1)
    
    version = sys.argv[1].strip()
    
    if not validate_version(version):
        logger.error(f"Invalid version format: {version}")
        logger.error("Version must be in semantic format (e.g., 1.0.0)")
        sys.exit(1)
    
    logger.info(f"Starting installation of SAP DevOps version {version}")
    
    install_dir = setup_directories(version)
    if not install_dir:
        sys.exit(1)
    
    zip_file = f"sap-devops-{version}.zip"
    
    if not download_release(version, zip_file):
        sys.exit(1)
    
    try:
        if not extract_zip(zip_file, install_dir):
            sys.exit(1)
        
        if not manage_symlink(version, install_dir):
            sys.exit(1)
        
        if not verify_installation(version, install_dir):
            sys.exit(1)
        
        logger.info(f"Installation complete!")
        logger.info(f"Installed to: {install_dir}")
        logger.info(f"Symlink: {os.path.join(BASE_INSTALL_PATH, SYMLINK_NAME)} -> {version}")
        
    finally:
        if os.path.exists(zip_file):
            os.remove(zip_file)
            logger.info(f"Cleaned up temporary zip file")


if __name__ == '__main__':
    main()
