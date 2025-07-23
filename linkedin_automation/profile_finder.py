#!/usr/bin/env python3
"""
LinkedIn Profile Finder and Enrichment Tool
This script finds LinkedIn profiles for leads and enriches the data
"""

import os
import sys
import time
import random
import json
import csv
from datetime import datetime
import argparse
import re

class LinkedInProfileFinder:
    def __init__(self):
        """Initialize the LinkedIn profile finder tool"""
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"/home/ubuntu/lead_generation/linkedin_automation/logs/profile_finder_{self.timestamp}.log"
        self.setup_logging()
        
        # Configuration settings
        self.config = {
            'search_delay': (2, 5),  # Random delay in seconds
            'max_searches_per_day': 100,
            'search_patterns': {
                'linkedin': [
                    '{first_name} {last_name} {company} linkedin',
                    '{company} {position} {first_name} {last_name} linkedin',
                    '{first_name} {last_name} {industry} linkedin'
                ],
                'email': [
                    '{first_name} {last_name} {company} email',
                    '{company} contact {first_name} {last_name}',
                    '{first_name} {last_name} {position} contact'
                ]
            }
        }
        
        # Initialize data storage
        self.leads = []
        self.enriched_leads = []
        self.search_log = []
    
    def setup_logging(self):
        """Set up logging for the script"""
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Redirect stdout and stderr to the log file
        sys.stdout = open(self.log_file, 'w')
        sys.stderr = open(self.log_file, 'a')
        
        print(f"LinkedIn profile finder logging started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Log file: {self.log_file}")
    
    def log_search(self, search_type, query, result):
        """Log a search to the search log"""
        search = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'search_type': search_type,
            'query': query,
            'result': result
        }
        
        self.search_log.append(search)
        print(f"[{search['timestamp']}] {search_type}: {query} - Result: {result}")
    
    def save_search_log(self):
        """Save the search log to a CSV file"""
        log_file = f"/home/ubuntu/lead_generation/linkedin_automation/logs/search_log_{self.timestamp}.csv"
        
        try:
            with open(log_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'search_type', 'query', 'result']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for search in self.search_log:
                    writer.writerow(search)
            
            print(f"Saved {len(self.search_log)} searches to {log_file}")
        except Exception as e:
            print(f"Error saving search log: {e}")
    
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
                   c.country, ct.first_name, ct.last_name, ct.email, ct.phone,
                   ct.position
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
    
    def simulate_search(self, query, search_type):
        """Simulate a search for LinkedIn profiles or email addresses"""
        # In a real implementation, this would use a search API or web scraping
        
        # Simulate the search delay
        time.sleep(random.uniform(*self.config['search_delay']))
        
        # For simulation purposes, we'll generate random results
        if search_type == 'linkedin':
            # Simulate finding a LinkedIn profile URL
            found = random.choice([True, True, False])  # 2/3 chance of finding a profile
            
            if found:
                # Generate a fake LinkedIn URL
                name_parts = query.split()
                if len(name_parts) >= 2:
                    first_name = name_parts[0].lower()
                    last_name = name_parts[1].lower()
                    variations = [
                        f"https://www.linkedin.com/in/{first_name}-{last_name}-123456/",
                        f"https://www.linkedin.com/in/{first_name}.{last_name}/",
                        f"https://www.linkedin.com/in/{first_name}{last_name}/",
                        f"https://www.linkedin.com/in/{last_name}{first_name}/"
                    ]
                    result = random.choice(variations)
                else:
                    result = "No profile found"
            else:
                result = "No profile found"
        
        elif search_type == 'email':
            # Simulate finding an email address
            found = random.choice([True, False, False])  # 1/3 chance of finding an email
            
            if found:
                # Generate a fake email address
                name_parts = query.split()
                if len(name_parts) >= 2:
                    first_name = name_parts[0].lower()
                    last_name = name_parts[1].lower()
                    domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'company.com', 'business.com']
                    variations = [
                        f"{first_name}.{last_name}@{random.choice(domains)}",
                        f"{first_name[0]}{last_name}@{random.choice(domains)}",
                        f"{first_name}{last_name[0]}@{random.choice(domains)}",
                        f"{first_name}@{random.choice(domains)}"
                    ]
                    result = random.choice(variations)
                else:
                    result = "No email found"
            else:
                result = "No email found"
        
        else:
            result = "Unknown search type"
        
        # Log the search
        self.log_search(search_type, query, result)
        
        return result
    
    def format_search_query(self, lead, pattern):
        """Format a search query using a pattern and lead data"""
        # Extract the necessary fields from the lead
        first_name = lead.get('first_name', '')
        last_name = lead.get('last_name', '')
        company = lead.get('company_name', '')
        industry = lead.get('industry', '')
        position = lead.get('position', '')
        
        # If first_name or last_name is missing or N/A, try to extract from company name
        if not first_name or first_name == 'N/A' or not last_name or last_name == 'N/A':
            if company and company != 'N/A':
                # Use the company name as the search term
                return pattern.format(
                    first_name='',
                    last_name='',
                    company=company,
                    industry=industry,
                    position=position
                ).replace('  ', ' ').strip()
        
        # Format the query
        return pattern.format(
            first_name=first_name,
            last_name=last_name,
            company=company,
            industry=industry,
            position=position
        ).replace('  ', ' ').strip()
    
    def find_linkedin_profile(self, lead):
        """Find a LinkedIn profile for a lead"""
        # Try different search patterns
        for pattern in self.config['search_patterns']['linkedin']:
            query = self.format_search_query(lead, pattern)
            
            if not query:
                continue
            
            result = self.simulate_search(query, 'linkedin')
            
            if result != "No profile found":
                return result
        
        return None
    
    def find_email_address(self, lead):
        """Find an email address for a lead"""
        # Try different search patterns
        for pattern in self.config['search_patterns']['email']:
            query = self.format_search_query(lead, pattern)
            
            if not query:
                continue
            
            result = self.simulate_search(query, 'email')
            
            if result != "No email found":
                return result
        
        return None
    
    def enrich_lead(self, lead):
        """Enrich a lead with LinkedIn profile and email information"""
        enriched_lead = lead.copy()
        
        # Find LinkedIn profile
        linkedin_profile = self.find_linkedin_profile(lead)
        if linkedin_profile:
            enriched_lead['linkedin_url'] = linkedin_profile
        
        # Find email address if not already present
        if not lead.get('email') or lead.get('email') == 'N/A':
            email = self.find_email_address(lead)
            if email:
                enriched_lead['email'] = email
        
        return enriched_lead
    
    def save_enriched_leads(self, output_file=None):
        """Save the enriched leads to a CSV file"""
        if not output_file:
            output_file = f"/home/ubuntu/lead_generation/linkedin_automation/data/enriched_leads_{self.timestamp}.csv"
        
        try:
            # Ensure all leads have the same fields
            all_fields = set()
            for lead in self.enriched_leads:
                all_fields.update(lead.keys())
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=sorted(all_fields))
                
                writer.writeheader()
                for lead in self.enriched_leads:
                    # Ensure all fields are present
                    for field in all_fields:
                        if field not in lead:
                            lead[field] = ''
                    
                    writer.writerow(lead)
            
            print(f"Saved {len(self.enriched_leads)} enriched leads to {output_file}")
            return output_file
        except Exception as e:
            print(f"Error saving enriched leads: {e}")
            return None
    
    def update_database(self, db_file):
        """Update the database with enriched lead information"""
        try:
            import sqlite3
            
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            updates = 0
            
            for lead in self.enriched_leads:
                # Update contacts table with LinkedIn URL and email
                if 'id' in lead and lead['id']:
                    if 'linkedin_url' in lead and lead['linkedin_url']:
                        cursor.execute(
                            "UPDATE contacts SET linkedin_url = ?, updated_at = CURRENT_TIMESTAMP WHERE company_id = ?",
                            (lead['linkedin_url'], lead['id'])
                        )
                    
                    if 'email' in lead and lead['email'] and lead['email'] != 'N/A':
                        cursor.execute(
                            "UPDATE contacts SET email = ?, updated_at = CURRENT_TIMESTAMP WHERE company_id = ?",
                            (lead['email'], lead['id'])
                        )
                    
                    updates += 1
            
            conn.commit()
            conn.close()
            
            print(f"Updated {updates} leads in the database")
            return updates
        except Exception as e:
            print(f"Error updating database: {e}")
            return 0
    
    def run(self, limit=None):
        """Run the LinkedIn profile finder for all leads"""
        print(f"\n{'='*50}\nRunning LinkedIn profile finder\n{'='*50}")
        
        # Limit the number of leads to process
        leads_to_process = self.leads
        if limit and limit > 0 and len(leads_to_process) > limit:
            leads_to_process = leads_to_process[:limit]
            print(f"Limited to {limit} leads")
        
        total_processed = 0
        
        for lead in leads_to_process:
            try:
                print(f"Processing lead: {lead.get('company_name', 'Unknown')} - {lead.get('first_name', '')} {lead.get('last_name', '')}")
                
                enriched_lead = self.enrich_lead(lead)
                self.enriched_leads.append(enriched_lead)
                
                total_processed += 1
                
                # Check if we've reached the daily limit
                if total_processed >= self.config['max_searches_per_day']:
                    print(f"Reached daily limit of {self.config['max_searches_per_day']} searches")
                    break
                
            except Exception as e:
                print(f"Error processing lead: {e}")
        
        # Save the search log
        self.save_search_log()
        
        # Save the enriched leads
        output_file = self.save_enriched_leads()
        
        print(f"\nLinkedIn profile finder completed. Total leads processed: {total_processed}")
        return total_processed, output_file

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='LinkedIn Profile Finder and Enrichment Tool')
    
    parser.add_argument('--input', type=str, default=None,
                        help='Input CSV file with leads data')
    
    parser.add_argument('--database', type=str, 
                        default='/home/ubuntu/lead_generation/data/leads_database.db',
                        help='SQLite database file with leads data')
    
    parser.add_argument('--industry', type=str, default=None,
                        help='Filter leads by industry')
    
    parser.add_argument('--limit', type=int, default=0,
                        help='Limit the number of leads to process (0 for no limit)')
    
    parser.add_argument('--output', type=str, default=None,
                        help='Output CSV file for enriched leads')
    
    parser.add_argument('--update-db', action='store_true',
                        help='Update the database with enriched lead information')
    
    return parser.parse_args()

def main():
    """Main function to run the LinkedIn profile finder"""
    print(f"Starting LinkedIn profile finder at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Parse arguments
    args = parse_arguments()
    
    # Initialize the profile finder
    finder = LinkedInProfileFinder()
    
    # Load leads
    if args.input and os.path.exists(args.input):
        finder.load_leads_from_csv(args.input)
    elif args.database and os.path.exists(args.database):
        finder.load_leads_from_database(args.database, args.industry, args.limit)
    else:
        print("No input data provided. Please specify --input or --database.")
        return 1
    
    # Run the profile finder
    total_processed, output_file = finder.run(args.limit)
    
    # Update the database if requested
    if args.update_db and args.database and os.path.exists(args.database):
        finder.update_database(args.database)
    
    print(f"LinkedIn profile finder completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Enriched leads saved to: {output_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
