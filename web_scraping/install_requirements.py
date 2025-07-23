#!/usr/bin/env python3
"""
Requirements installer for web scraping lead generation
Installs all necessary Python packages
"""

import subprocess
import sys

def install_requirements():
    """Install all required packages"""
    requirements = [
        'requests',
        'beautifulsoup4',
        'pandas',
        'tqdm',
        'lxml',
        'fake-useragent',
        'python-dotenv'
    ]
    
    print("Installing required packages...")
    
    for package in requirements:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            return False
    
    print("All required packages installed successfully!")
    return True

if __name__ == "__main__":
    install_requirements()
