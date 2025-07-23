#!/usr/bin/env python3
"""
README for AI Startup Lead Generation Automation System
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime

def print_header():
    """Print the header for the README"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║             AI STARTUP LEAD GENERATION AUTOMATION SYSTEM              ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """)

def print_section(title):
    """Print a section title"""
    print(f"\n=== {title} ===\n")

def check_installation():
    """Check if all required components are installed"""
    print_section("Checking Installation")
    
    # Check Python version
    python_version = sys.version.split()[0]
    print(f"Python version: {python_version}")
    
    # Check if required directories exist
    directories = [
        '/home/ubuntu/lead_generation/web_scraping',
        '/home/ubuntu/lead_generation/linkedin_automation',
        '/home/ubuntu/lead_generation/email_templates',
        '/home/ubuntu/lead_generation/database',
        '/home/ubuntu/lead_generation/automation'
    ]
    
    all_dirs_exist = True
    for directory in directories:
        if os.path.exists(directory):
            print(f"✓ {directory} exists")
        else:
            print(f"✗ {directory} does not exist")
            all_dirs_exist = False
    
    # Check if key files exist
    key_files = [
        '/home/ubuntu/lead_generation/web_scraping/scraper.py',
        '/home/ubuntu/lead_generation/linkedin_automation/linkedin_automation.py',
        '/home/ubuntu/lead_generation/email_templates/email_template_generator.py',
        '/home/ubuntu/lead_generation/database/lead_database.py',
        '/home/ubuntu/lead_generation/automation/lead_generation_automation.py',
        '/home/ubuntu/lead_generation/install_requirements.py',
        '/home/ubuntu/lead_generation/user_guide.md'
    ]
    
    all_files_exist = True
    for file in key_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} does not exist")
            all_files_exist = False
    
    if all_dirs_exist and all_files_exist:
        print("\n✓ All required components are installed")
    else:
        print("\n✗ Some components are missing")

def show_quick_start():
    """Show quick start instructions"""
    print_section("Quick Start Guide")
    
    print("""
1. Install Dependencies:
   python3 /home/ubuntu/lead_generation/install_requirements.py

2. Set Up Database with Sample Data:
   cd /home/ubuntu/lead_generation/automation
   python3 lead_generation_automation.py --setup-database --sample-size 20

3. Run Full Automation:
   cd /home/ubuntu/lead_generation/automation
   python3 lead_generation_automation.py

4. View Reports:
   Reports are saved in /home/ubuntu/lead_generation/automation/reports

For detailed instructions, see the User Guide:
   /home/ubuntu/lead_generation/user_guide.md
""")

def show_component_summary():
    """Show a summary of the components"""
    print_section("System Components")
    
    components = [
        ("Web Scraping", "Automatically collects company information from business directories"),
        ("LinkedIn Automation", "Finds and enriches lead profiles, sends connection requests"),
        ("Email Outreach", "Creates personalized email templates for different stages"),
        ("Lead Database", "Tracks all leads, interactions, and campaign performance"),
        ("End-to-End Automation", "Orchestrates all components to work together")
    ]
    
    for name, description in components:
        print(f"• {name}: {description}")

def main():
    """Main function to display the README"""
    parser = argparse.ArgumentParser(description='AI Startup Lead Generation Automation System README')
    
    parser.add_argument('--check-installation', action='store_true',
                        help='Check if all required components are installed')
    
    parser.add_argument('--open-user-guide', action='store_true',
                        help='Open the user guide in a text editor')
    
    args = parser.parse_args()
    
    print_header()
    
    print(f"Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nWelcome to the AI Startup Lead Generation Automation System!")
    print("This system helps you generate high-quality leads for your AI chatbot, voicebot, and agents startup.")
    
    if args.check_installation:
        check_installation()
    else:
        show_quick_start()
        show_component_summary()
    
    if args.open_user_guide:
        try:
            subprocess.run(['less', '/home/ubuntu/lead_generation/user_guide.md'])
        except Exception as e:
            print(f"Error opening user guide: {e}")
            print("You can open it manually with: less /home/ubuntu/lead_generation/user_guide.md")
    
    print_section("Next Steps")
    print("""
1. Read the User Guide for detailed instructions
2. Configure the system to match your requirements
3. Start generating leads for your AI startup!

For any questions or issues, refer to the troubleshooting section in the User Guide.
""")

if __name__ == "__main__":
    main()
