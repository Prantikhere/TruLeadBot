#!/usr/bin/env python3
"""
Main script to run the complete web scraping lead generation process
"""

import os
import sys
import argparse
from datetime import datetime
import time

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import LeadScraper
from database import LeadDatabase
import utils

def setup_directories():
    """Create necessary directories for the project"""
    dirs = [
        '/home/ubuntu/lead_generation/data',
        '/home/ubuntu/lead_generation/logs',
        '/home/ubuntu/lead_generation/exports'
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def setup_logging():
    """Set up logging for the script"""
    log_file = f"/home/ubuntu/lead_generation/logs/scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Redirect stdout and stderr to the log file
    sys.stdout = open(log_file, 'w')
    sys.stderr = open(log_file, 'a')
    
    print(f"Logging started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Log file: {log_file}")
    
    return log_file

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Lead Generation Web Scraper')
    
    parser.add_argument('--industries', nargs='+', 
                        choices=['digital_marketing', 'saas_companies', 'enterprise_it', 'smes', 'service_businesses', 'all'],
                        default=['all'],
                        help='Industries to scrape (default: all)')
    
    parser.add_argument('--limit', type=int, default=0,
                        help='Limit the number of leads per industry (0 for no limit)')
    
    parser.add_argument('--export', action='store_true',
                        help='Export results to CSV after scraping')
    
    parser.add_argument('--enrich', action='store_true',
                        help='Enrich lead data with additional information')
    
    return parser.parse_args()

def run_scraper(args):
    """Run the lead scraper with the specified arguments"""
    print(f"Starting lead generation scraper at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize the scraper
    scraper = LeadScraper()
    
    # Determine which industries to scrape
    industries_to_scrape = {}
    if 'all' in args.industries:
        industries_to_scrape = scraper.TARGET_INDUSTRIES
    else:
        for industry in args.industries:
            if industry in scraper.TARGET_INDUSTRIES:
                industries_to_scrape[industry] = scraper.TARGET_INDUSTRIES[industry]
    
    # Run the scraper
    all_leads = []
    for industry, urls in industries_to_scrape.items():
        print(f"\n{'='*50}\nScraping {industry} industry\n{'='*50}")
        industry_leads = scraper.scrape_industry(industry, urls)
        
        # Apply limit if specified
        if args.limit > 0 and len(industry_leads) > args.limit:
            industry_leads = industry_leads[:args.limit]
            print(f"Limited to {args.limit} leads for {industry}")
        
        all_leads.extend(industry_leads)
        
        # Save industry-specific leads
        scraper.save_leads_to_csv(industry_leads, f"{industry}_leads_{scraper.timestamp}.csv")
        scraper.save_leads_to_json(industry_leads, f"{industry}_leads_{scraper.timestamp}.json")
        
        print(f"Completed scraping {len(industry_leads)} leads for {industry}")
    
    # Save all leads combined
    scraper.save_leads_to_csv(all_leads, f"all_leads_{scraper.timestamp}.csv")
    scraper.save_leads_to_json(all_leads, f"all_leads_{scraper.timestamp}.json")
    
    print(f"\nScraping completed. Total leads collected: {len(all_leads)}")
    
    return all_leads, scraper.timestamp

def enrich_leads(leads):
    """Enrich lead data with additional information"""
    print(f"\n{'='*50}\nEnriching lead data\n{'='*50}")
    
    enriched_leads = []
    total_leads = len(leads)
    
    for i, lead in enumerate(leads):
        print(f"Enriching lead {i+1}/{total_leads}: {lead.get('company_name', 'Unknown')}")
        
        # Skip if no website
        if lead.get('website', 'N/A') == 'N/A' or not utils.is_valid_company_website(lead.get('website')):
            print(f"Skipping lead with invalid website: {lead.get('website', 'N/A')}")
            enriched_leads.append(lead)
            continue
        
        try:
            # Get the website HTML
            html = utils.safe_request(lead['website'])
            
            if not html:
                print(f"Could not fetch website: {lead['website']}")
                enriched_leads.append(lead)
                continue
            
            # Extract contact information
            contact_info = utils.extract_contact_info(html)
            if contact_info.get('emails'):
                lead['email'] = contact_info['emails'][0]  # Use the first email
            if contact_info.get('phones'):
                lead['phone'] = contact_info['phones'][0]  # Use the first phone
            
            # Find and check contact page if no email found
            if lead.get('email', 'N/A') == 'N/A':
                contact_page_url = utils.find_contact_page(lead['website'], html)
                if contact_page_url:
                    print(f"Checking contact page: {contact_page_url}")
                    contact_html = utils.safe_request(contact_page_url)
                    if contact_html:
                        contact_info = utils.extract_contact_info(contact_html)
                        if contact_info.get('emails'):
                            lead['email'] = contact_info['emails'][0]
                        if contact_info.get('phones'):
                            lead['phone'] = contact_info['phones'][0]
            
            # Extract company information
            company_info = utils.extract_company_info(html)
            lead['company_size'] = company_info.get('company_size', 'Unknown')
            lead['technologies'] = ', '.join(company_info.get('technologies', []))
            lead['description'] = utils.extract_company_description(html)
            
            # Normalize company name
            lead['company_name'] = utils.normalize_company_name(lead['company_name'])
            
            enriched_leads.append(lead)
            
            # Add a delay to avoid overloading servers
            time.sleep(2)
            
        except Exception as e:
            print(f"Error enriching lead: {e}")
            enriched_leads.append(lead)
    
    print(f"Enrichment completed for {len(enriched_leads)} leads")
    return enriched_leads

def import_to_database(leads, timestamp):
    """Import leads to the database"""
    print(f"\n{'='*50}\nImporting leads to database\n{'='*50}")
    
    # Initialize the database
    db = LeadDatabase()
    if not db.connect():
        print("Failed to connect to database")
        return False
    
    # Create tables
    db.create_tables()
    
    # Import leads
    leads_imported = 0
    for lead in leads:
        company_id = db.insert_company(lead)
        
        if company_id:
            # If we have email, insert into contacts table
            if 'email' in lead and lead['email'] != 'N/A':
                db.insert_contact(company_id, lead)
            
            # Create initial lead status
            db.insert_lead_status(company_id)
            
            leads_imported += 1
    
    db.conn.commit()
    
    # Print some stats
    print(f"Imported {leads_imported} leads to database")
    print(f"Total leads in database: {db.get_lead_count()}")
    
    print("\nLeads by industry:")
    for industry, count in db.get_leads_by_industry():
        print(f"  {industry}: {count}")
    
    print("\nLeads by status:")
    for status, count in db.get_leads_by_status():
        print(f"  {status}: {count}")
    
    # Export to CSV if needed
    export_file = f"/home/ubuntu/lead_generation/exports/all_leads_export_{timestamp}.csv"
    db.export_to_csv(export_file)
    
    # Close connection
    db.close()
    
    return True

def main():
    """Main function to run the complete process"""
    # Set up directories and logging
    setup_directories()
    log_file = setup_logging()
    
    # Parse arguments
    args = parse_arguments()
    
    # Run the scraper
    leads, timestamp = run_scraper(args)
    
    # Enrich leads if requested
    if args.enrich and leads:
        leads = enrich_leads(leads)
        
        # Save enriched leads
        enriched_file_csv = f"/home/ubuntu/lead_generation/data/enriched_leads_{timestamp}.csv"
        enriched_file_json = f"/home/ubuntu/lead_generation/data/enriched_leads_{timestamp}.json"
        
        scraper = LeadScraper()  # Create a new instance just to use the save methods
        scraper.save_leads_to_csv(leads, enriched_file_csv)
        scraper.save_leads_to_json(leads, enriched_file_json)
    
    # Import to database
    import_to_database(leads, timestamp)
    
    # Export if requested
    if args.export:
        export_file = f"/home/ubuntu/lead_generation/exports/leads_export_{timestamp}.csv"
        print(f"\nExporting leads to {export_file}")
        
        # We already exported in the import_to_database function
        print(f"Export completed. File saved at: {export_file}")
    
    print(f"\nLead generation process completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Log file: {log_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
