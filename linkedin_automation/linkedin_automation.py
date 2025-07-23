#!/usr/bin/env python3
"""
LinkedIn Automation for Lead Generation
This script automates LinkedIn interactions to generate leads
"""

import os
import sys
import time
import random
import json
import csv
from datetime import datetime
import argparse

# Create necessary directories
os.makedirs('/home/ubuntu/lead_generation/linkedin_automation/data', exist_ok=True)
os.makedirs('/home/ubuntu/lead_generation/linkedin_automation/templates', exist_ok=True)
os.makedirs('/home/ubuntu/lead_generation/linkedin_automation/logs', exist_ok=True)

class LinkedInAutomation:
    def __init__(self):
        """Initialize the LinkedIn automation tool"""
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"/home/ubuntu/lead_generation/linkedin_automation/logs/linkedin_{self.timestamp}.log"
        self.setup_logging()
        
        # Configuration settings
        self.config = {
            'connection_limit_per_day': 25,
            'message_limit_per_day': 20,
            'delay_between_actions': (30, 90),  # Random delay in seconds
            'working_hours': {
                'start': 9,  # 9 AM
                'end': 17    # 5 PM
            },
            'days_off': ['Saturday', 'Sunday'],
            'search_filters': {
                'digital_marketing': [
                    'Marketing Director',
                    'Digital Marketing Manager',
                    'CMO',
                    'Marketing Head'
                ],
                'saas_companies': [
                    'CTO',
                    'Product Manager',
                    'VP of Engineering',
                    'Technical Director'
                ],
                'enterprise_it': [
                    'IT Director',
                    'CIO',
                    'IT Manager',
                    'Digital Transformation Manager'
                ],
                'smes': [
                    'Owner',
                    'Founder',
                    'CEO',
                    'General Manager'
                ],
                'service_businesses': [
                    'Business Owner',
                    'Operations Manager',
                    'Service Manager'
                ]
            }
        }
        
        # Message templates
        self.templates = {
            'connection_request': {
                'default': "Hi {first_name}, I noticed your work in {industry} and thought we could connect. I'm working with AI chatbot solutions that are helping businesses in your industry improve customer service and generate leads.",
                'digital_marketing': "Hi {first_name}, I saw your profile and your experience in digital marketing caught my attention. I'm working with AI chatbot solutions that are helping marketing agencies automate lead generation and improve client engagement. Would love to connect!",
                'saas_companies': "Hi {first_name}, I noticed your work at {company} in the SaaS space. I'm working with AI chatbot technology that's helping SaaS companies improve user onboarding and support. Thought we could connect!",
                'enterprise_it': "Hi {first_name}, I came across your profile and your IT leadership experience is impressive. I'm working with AI solutions that are helping enterprises automate customer interactions and reduce support costs. Would be great to connect!",
                'smes': "Hi {first_name}, I noticed your business and thought we could connect. I'm working with AI chatbot solutions specifically designed for SMEs to improve customer service without increasing headcount.",
                'service_businesses': "Hi {first_name}, I saw your service business and thought we could connect. I'm working with affordable AI chatbot solutions that are helping businesses like yours handle customer inquiries 24/7."
            },
            'follow_up': {
                'default': "Hi {first_name}, thanks for connecting! I wanted to share a bit more about how our AI chatbot solutions are helping businesses in {industry}. Would you be open to a quick chat about how it might help {company}?",
                'digital_marketing': "Hi {first_name}, thanks for connecting! I wanted to share how our AI chatbots are helping marketing agencies generate and qualify leads 24/7. Would you be interested in seeing how it could work for your clients?",
                'saas_companies': "Hi {first_name}, thanks for connecting! I wanted to share how our AI chatbots are helping SaaS companies reduce churn by improving customer support. Would you be open to a quick chat about how it might help {company}?",
                'enterprise_it': "Hi {first_name}, thanks for connecting! I wanted to share how our AI solutions are helping IT departments reduce ticket volume by up to 40%. Would you be interested in learning more about how it could work for {company}?",
                'smes': "Hi {first_name}, thanks for connecting! I wanted to share how our affordable AI chatbots are helping small businesses provide 24/7 customer service. Would you be open to a quick chat about how it might help your business?",
                'service_businesses': "Hi {first_name}, thanks for connecting! I wanted to share how service businesses like yours are using our AI chatbots to book appointments and answer FAQs automatically. Would you be interested in seeing a quick demo?"
            }
        }
        
        # Initialize data storage
        self.leads = []
        self.actions_log = []
    
    def setup_logging(self):
        """Set up logging for the script"""
        # Redirect stdout and stderr to the log file
        sys.stdout = open(self.log_file, 'w')
        sys.stderr = open(self.log_file, 'a')
        
        print(f"LinkedIn automation logging started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Log file: {self.log_file}")
    
    def log_action(self, action_type, target, status, notes=""):
        """Log an action to the actions log"""
        action = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'action_type': action_type,
            'target': target,
            'status': status,
            'notes': notes
        }
        
        self.actions_log.append(action)
        print(f"[{action['timestamp']}] {action_type}: {target} - {status} {notes}")
    
    def save_actions_log(self):
        """Save the actions log to a CSV file"""
        log_file = f"/home/ubuntu/lead_generation/linkedin_automation/logs/actions_log_{self.timestamp}.csv"
        
        try:
            with open(log_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'action_type', 'target', 'status', 'notes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for action in self.actions_log:
                    writer.writerow(action)
            
            print(f"Saved {len(self.actions_log)} actions to {log_file}")
        except Exception as e:
            print(f"Error saving actions log: {e}")
    
    def load_leads_from_csv(self, csv_file):
        """Load leads from a CSV file"""
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                leads_loaded = 0
                
                for row in csv_reader:
                    self.leads.append(row)
                    leads_loaded += 1
                
                print(f"Loaded {leads_loaded} leads from {csv_file}")
                return leads_loaded
        except Exception as e:
            print(f"Error loading leads from CSV: {e}")
            return 0
    
    def load_leads_from_database(self, db_file, industry=None, limit=100):
        """Load leads from the SQLite database"""
        try:
            import sqlite3
            
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            query = """
            SELECT c.id, c.company_name, c.website, c.industry, c.company_size, 
                   c.current_chatbot, c.address, c.city, c.state, c.zipcode, 
                   c.country, ct.first_name, ct.last_name, ct.email, ct.phone
            FROM companies c
            LEFT JOIN contacts ct ON c.id = ct.company_id
            LEFT JOIN lead_status ls ON c.id = ls.company_id
            WHERE ls.status = 'New'
            """
            
            if industry:
                query += f" AND c.industry LIKE '%{industry}%'"
            
            query += f" LIMIT {limit}"
            
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            leads = []
            
            for row in cursor.fetchall():
                lead = dict(zip(columns, row))
                leads.append(lead)
            
            self.leads.extend(leads)
            print(f"Loaded {len(leads)} leads from database")
            
            conn.close()
            return len(leads)
        except Exception as e:
            print(f"Error loading leads from database: {e}")
            return 0
    
    def generate_search_url(self, industry, title):
        """Generate a LinkedIn search URL for a specific industry and title"""
        # This is a template URL for LinkedIn Sales Navigator searches
        # In a real implementation, you would need to use the LinkedIn API or a browser automation tool
        base_url = "https://www.linkedin.com/sales/search/people"
        
        # Encode the search parameters
        params = {
            'keywords': f"{title} {industry}",
            'companySize': ['B', 'C', 'D'],  # B: 11-50, C: 51-200, D: 201-500
            'geoIncluded': 'worldwide',
            'page': 1
        }
        
        # In a real implementation, you would properly encode these parameters
        # For this example, we'll just return a placeholder URL
        return f"{base_url}?keywords={title}+{industry}"
    
    def simulate_connection_request(self, lead, industry):
        """Simulate sending a connection request on LinkedIn"""
        # In a real implementation, this would use the LinkedIn API or browser automation
        
        # Get the appropriate template
        template = self.templates['connection_request'].get(industry, self.templates['connection_request']['default'])
        
        # Format the message
        first_name = lead.get('first_name', 'there')
        if first_name == 'N/A':
            first_name = 'there'
        
        company = lead.get('company_name', 'your company')
        
        message = template.format(
            first_name=first_name,
            company=company,
            industry=industry
        )
        
        # Simulate the action
        time.sleep(random.uniform(*self.config['delay_between_actions']))
        
        # Log the action
        self.log_action(
            action_type="connection_request",
            target=f"{lead.get('first_name', '')} {lead.get('last_name', '')} at {lead.get('company_name', '')}",
            status="sent",
            notes=f"Message: {message}"
        )
        
        return True
    
    def simulate_follow_up_message(self, lead, industry):
        """Simulate sending a follow-up message on LinkedIn"""
        # In a real implementation, this would use the LinkedIn API or browser automation
        
        # Get the appropriate template
        template = self.templates['follow_up'].get(industry, self.templates['follow_up']['default'])
        
        # Format the message
        first_name = lead.get('first_name', 'there')
        if first_name == 'N/A':
            first_name = 'there'
        
        company = lead.get('company_name', 'your company')
        
        message = template.format(
            first_name=first_name,
            company=company,
            industry=industry
        )
        
        # Simulate the action
        time.sleep(random.uniform(*self.config['delay_between_actions']))
        
        # Log the action
        self.log_action(
            action_type="follow_up_message",
            target=f"{lead.get('first_name', '')} {lead.get('last_name', '')} at {lead.get('company_name', '')}",
            status="sent",
            notes=f"Message: {message}"
        )
        
        return True
    
    def run_campaign(self, industry, action_type, limit=10):
        """Run a LinkedIn campaign for a specific industry"""
        print(f"\n{'='*50}\nRunning LinkedIn {action_type} campaign for {industry}\n{'='*50}")
        
        # Filter leads by industry
        industry_leads = [lead for lead in self.leads if industry.lower() in lead.get('industry', '').lower()]
        
        if not industry_leads:
            print(f"No leads found for industry: {industry}")
            return 0
        
        # Limit the number of actions
        if limit > 0 and len(industry_leads) > limit:
            industry_leads = industry_leads[:limit]
            print(f"Limited to {limit} leads for {industry}")
        
        actions_completed = 0
        
        for lead in industry_leads:
            try:
                if action_type == 'connection':
                    success = self.simulate_connection_request(lead, industry)
                elif action_type == 'follow_up':
                    success = self.simulate_follow_up_message(lead, industry)
                else:
                    print(f"Unknown action type: {action_type}")
                    continue
                
                if success:
                    actions_completed += 1
                
                # Add a random delay between actions
                time.sleep(random.uniform(*self.config['delay_between_actions']))
                
            except Exception as e:
                print(f"Error performing {action_type} for lead: {e}")
        
        print(f"Completed {actions_completed} {action_type} actions for {industry}")
        return actions_completed
    
    def run(self, industries=None, action_types=None, limits=None):
        """Run the LinkedIn automation for specified industries and action types"""
        if not industries:
            industries = list(self.config['search_filters'].keys())
        
        if not action_types:
            action_types = ['connection', 'follow_up']
        
        if not limits:
            limits = {
                'connection': self.config['connection_limit_per_day'],
                'follow_up': self.config['message_limit_per_day']
            }
        
        total_actions = 0
        
        for industry in industries:
            for action_type in action_types:
                limit = limits.get(action_type, 10)
                actions = self.run_campaign(industry, action_type, limit)
                total_actions += actions
        
        # Save the actions log
        self.save_actions_log()
        
        print(f"\nLinkedIn automation completed. Total actions: {total_actions}")
        return total_actions

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='LinkedIn Automation for Lead Generation')
    
    parser.add_argument('--industries', nargs='+', 
                        choices=['digital_marketing', 'saas_companies', 'enterprise_it', 'smes', 'service_businesses', 'all'],
                        default=['all'],
                        help='Industries to target (default: all)')
    
    parser.add_argument('--actions', nargs='+',
                        choices=['connection', 'follow_up', 'all'],
                        default=['all'],
                        help='Action types to perform (default: all)')
    
    parser.add_argument('--connection-limit', type=int, default=25,
                        help='Limit the number of connection requests per day (default: 25)')
    
    parser.add_argument('--message-limit', type=int, default=20,
                        help='Limit the number of follow-up messages per day (default: 20)')
    
    parser.add_argument('--input', type=str, default=None,
                        help='Input CSV file with leads data')
    
    parser.add_argument('--database', type=str, 
                        default='/home/ubuntu/lead_generation/data/leads_database.db',
                        help='SQLite database file with leads data')
    
    return parser.parse_args()

def main():
    """Main function to run the LinkedIn automation"""
    print(f"Starting LinkedIn automation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Parse arguments
    args = parse_arguments()
    
    # Initialize the automation
    linkedin = LinkedInAutomation()
    
    # Load leads
    if args.input and os.path.exists(args.input):
        linkedin.load_leads_from_csv(args.input)
    elif args.database and os.path.exists(args.database):
        linkedin.load_leads_from_database(args.database)
    else:
        print("No input data provided. Please specify --input or --database.")
        return 1
    
    # Determine which industries to target
    industries = []
    if 'all' in args.industries:
        industries = list(linkedin.config['search_filters'].keys())
    else:
        industries = args.industries
    
    # Determine which actions to perform
    actions = []
    if 'all' in args.actions:
        actions = ['connection', 'follow_up']
    else:
        actions = args.actions
    
    # Set limits
    limits = {
        'connection': args.connection_limit,
        'follow_up': args.message_limit
    }
    
    # Run the automation
    linkedin.run(industries, actions, limits)
    
    print(f"LinkedIn automation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
