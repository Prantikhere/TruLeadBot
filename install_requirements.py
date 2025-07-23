#!/usr/bin/env python3
"""
Install requirements for lead generation automation
"""

import subprocess
import sys

def install_requirements():
    """Install all required packages for the lead generation automation system"""
    requirements = [
        # Web scraping
        'beautifulsoup4',
        'requests',
        'lxml',
        'selenium',
        'webdriver-manager',
        
        # Data processing
        'pandas',
        'numpy',
        
        # Utilities
        'tqdm',
        'python-dotenv',
        'argparse',
        'fake-useragent',
        
        # Email
        'email-validator',
        
        # LinkedIn
        'linkedin-api',
    ]
    
    print("Installing required packages...")
    
    for package in requirements:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except Exception as e:
            print(f"Error installing {package}: {e}")
    
    print("All required packages installed.")

if __name__ == "__main__":
    install_requirements()
