#!/usr/bin/env python3
"""
Lead Generation Automation Master Script
This script orchestrates the entire lead generation process for the AI chatbot startup
"""

import os
import sys
import argparse
import logging
import json
import csv
import time
import random
from datetime import datetime, timedelta
import subprocess
import sqlite3

# Add the project directories to the path
sys.path.append('/home/ubuntu/lead_generation/web_scraping')
sys.path.append('/home/ubuntu/lead_generation/linkedin_automation')
sys.path.append('/home/ubuntu/lead_generation/email_templates')
sys.path.append('/home/ubuntu/lead_generation/database')

# Import modules from other components
try:
    from scraper import LeadScraper
    from database import LeadDatabase
    from linkedin_automation import LinkedInAutomation
    from profile_finder import LinkedInProfileFinder
    from template_generator import TemplateGenerator
    from email_template_generator import EmailTemplateGenerator
    from lead_database import LeadDatabase as MasterDatabase
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all required components are installed.")
    sys.exit(1)

class LeadGenerationAutomation:
    def __init__(self, config_file=None):
        """Initialize the lead generation automation system"""
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.setup_logging()
        
        # Load configuration
        self.config = self.load_config(config_file)
        
        # Initialize components
        self.db_path = self.config.get('database', {}).get('path', '/home/ubuntu/lead_generation/database/leads.db')
        self.db = MasterDatabase(self.db_path)
        
        # Create directories
        self.create_directories()
    
    def setup_logging(self):
        """Set up logging for the automation system"""
        log_dir = '/home/ubuntu/lead_generation/automation/logs'
        os.makedirs(log_dir, exist_ok=True)
        
        self.log_file = f"{log_dir}/automation_{self.timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('lead_generation')
        self.logger.info(f"Lead generation automation started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Log file: {self.log_file}")
    
    def load_config(self, config_file):
        """Load configuration from a JSON file"""
        default_config = {
            'database': {
                'path': '/home/ubuntu/lead_generation/database/leads.db'
            },
            'web_scraping': {
                'enabled': True,
                'target_industries': [
                    'digital_marketing',
                    'saas_companies',
                    'enterprise_it',
                    'smes',
                    'service_businesses'
                ],
                'leads_per_industry': 50,
                'enrich_data': True
            },
            'linkedin_automation': {
                'enabled': True,
                'connection_limit_per_day': 25,
                'message_limit_per_day': 20,
                'profile_finder_enabled': True,
                'profile_finder_limit': 50
            },
            'email_outreach': {
                'enabled': True,
                'emails_per_day': 50,
                'follow_up_days': 3,
                'max_follow_ups': 2
            },
            'scheduling': {
                'web_scraping_frequency': 'weekly',
                'linkedin_frequency': 'daily',
                'email_frequency': 'daily',
                'database_backup_frequency': 'daily'
            }
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                
                # Merge user config with default config
                for key, value in user_config.items():
                    if key in default_config and isinstance(value, dict):
                        default_config[key].update(value)
                    else:
                        default_config[key] = value
                
                self.logger.info(f"Loaded configuration from {config_file}")
            except Exception as e:
                self.logger.error(f"Error loading configuration: {e}")
        else:
            self.logger.info("Using default configuration")
            
            # Save default config for reference
            config_dir = '/home/ubuntu/lead_generation/automation/config'
            os.makedirs(config_dir, exist_ok=True)
            
            default_config_file = f"{config_dir}/default_config.json"
            try:
                with open(default_config_file, 'w') as f:
                    json.dump(default_config, f, indent=4)
                
                self.logger.info(f"Saved default configuration to {default_config_file}")
            except Exception as e:
                self.logger.error(f"Error saving default configuration: {e}")
        
        return default_config
    
    def create_directories(self):
        """Create necessary directories for the automation system"""
        directories = [
            '/home/ubuntu/lead_generation/automation/logs',
            '/home/ubuntu/lead_generation/automation/config',
            '/home/ubuntu/lead_generation/automation/reports',
            '/home/ubuntu/lead_generation/automation/backups',
            '/home/ubuntu/lead_generation/data',
            '/home/ubuntu/lead_generation/database/backups'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.logger.info(f"Created directory: {directory}")
    
    def backup_database(self):
        """Backup the lead database"""
        backup_dir = '/home/ubuntu/lead_generation/database/backups'
        backup_file = f"{backup_dir}/leads_backup_{self.timestamp}.db"
        
        try:
            # Connect to the database
            if not self.db.connect():
                self.logger.error("Failed to connect to database for backup")
                return False
            
            # Close the connection to ensure all changes are written
            self.db.close()
            
            # Copy the database file
            import shutil
            shutil.copy2(self.db_path, backup_file)
            
            self.logger.info(f"Database backed up to {backup_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error backing up database: {e}")
            return False
    
    def run_web_scraping(self):
        """Run the web scraping component"""
        if not self.config.get('web_scraping', {}).get('enabled', True):
            self.logger.info("Web scraping is disabled in configuration")
            return False
        
        self.logger.info("Starting web scraping process")
        
        try:
            # Initialize the scraper
            scraper = LeadScraper()
            
            # Get target industries from config
            target_industries = self.config.get('web_scraping', {}).get('target_industries', [])
            leads_per_industry = self.config.get('web_scraping', {}).get('leads_per_industry', 50)
            enrich_data = self.config.get('web_scraping', {}).get('enrich_data', True)
            
            # Filter industries to scrape
            industries_to_scrape = {}
            for industry in target_industries:
                if industry in scraper.TARGET_INDUSTRIES:
                    industries_to_scrape[industry] = scraper.TARGET_INDUSTRIES[industry]
            
            # Run the scraper
            all_leads = []
            for industry, urls in industries_to_scrape.items():
                self.logger.info(f"Scraping {industry} industry")
                industry_leads = scraper.scrape_industry(industry, urls)
                
                # Apply limit if specified
                if leads_per_industry > 0 and len(industry_leads) > leads_per_industry:
                    industry_leads = industry_leads[:leads_per_industry]
                    self.logger.info(f"Limited to {leads_per_industry} leads for {industry}")
                
                all_leads.extend(industry_leads)
                
                # Save industry-specific leads
                scraper.save_leads_to_csv(industry_leads, f"{industry}_leads_{scraper.timestamp}.csv")
                scraper.save_leads_to_json(industry_leads, f"{industry}_leads_{scraper.timestamp}.json")
                
                self.logger.info(f"Completed scraping {len(industry_leads)} leads for {industry}")
            
            # Save all leads combined
            scraper.save_leads_to_csv(all_leads, f"all_leads_{scraper.timestamp}.csv")
            scraper.save_leads_to_json(all_leads, f"all_leads_{scraper.timestamp}.json")
            
            self.logger.info(f"Web scraping completed. Total leads collected: {len(all_leads)}")
            
            # Enrich data if enabled
            if enrich_data and all_leads:
                self.logger.info("Starting data enrichment process")
                
                # Import to database
                if not self.db.connect():
                    self.logger.error("Failed to connect to database")
                    return False
                
                self.db.create_tables()
                
                # Import leads
                leads_imported = 0
                for lead in all_leads:
                    company_id = self.db.insert_company(lead)
                    
                    if company_id:
                        # If we have contact information, insert into contacts table
                        if lead.get('email') and lead.get('email') != 'N/A':
                            self.db.insert_contact(company_id, lead)
                        
                        # Create initial lead status
                        self.db.insert_lead_status(company_id)
                        leads_imported += 1
                
                self.db.conn.commit()
                self.logger.info(f"Imported {leads_imported} leads to database")
                
                # Close the database connection
                self.db.close()
            
            return True
        except Exception as e:
            self.logger.error(f"Error in web scraping process: {e}")
            return False
    
    def run_linkedin_profile_finder(self):
        """Run the LinkedIn profile finder component"""
        if not self.config.get('linkedin_automation', {}).get('enabled', True):
            self.logger.info("LinkedIn automation is disabled in configuration")
            return False
        
        if not self.config.get('linkedin_automation', {}).get('profile_finder_enabled', True):
            self.logger.info("LinkedIn profile finder is disabled in configuration")
            return False
        
        self.logger.info("Starting LinkedIn profile finder process")
        
        try:
            # Initialize the profile finder
            finder = LinkedInProfileFinder()
            
            # Connect to the database
            if not self.db.connect():
                self.logger.error("Failed to connect to database")
                return False
            
            # Get leads from database
            limit = self.config.get('linkedin_automation', {}).get('profile_finder_limit', 50)
            
            self.logger.info(f"Loading up to {limit} leads from database")
            
            # Get leads with status 'New'
            leads = []
            self.db.cursor.execute('''
            SELECT c.id, c.company_name, c.website, c.industry, c.company_size, 
                   c.current_chatbot, c.address, c.city, c.state, c.zipcode, 
                   c.country, ct.first_name, ct.last_name, ct.email, ct.phone,
                   ct.position
            FROM companies c
            LEFT JOIN contacts ct ON c.id = ct.company_id
            LEFT JOIN lead_status ls ON c.id = ls.company_id
            WHERE ls.status = 'New'
            LIMIT ?
            ''', (limit,))
            
            columns = [column[0] for column in self.db.cursor.description]
            
            for row in self.db.cursor.fetchall():
                lead = dict(zip(columns, row))
                leads.append(lead)
            
            self.logger.info(f"Loaded {len(leads)} leads from database")
            
            # Close the database connection temporarily
            self.db.close()
            
            # Run the profile finder
            if leads:
                finder.leads = leads
                total_processed, output_file = finder.run(limit)
                
                self.logger.info(f"LinkedIn profile finder completed. Processed {total_processed} leads")
                self.logger.info(f"Enriched leads saved to: {output_file}")
                
                # Update the database with enriched lead information
                if output_file and os.path.exists(output_file):
                    # Reconnect to the database
                    if not self.db.connect():
                        self.logger.error("Failed to connect to database")
                        return False
                    
                    # Load enriched leads
                    enriched_leads = []
                    with open(output_file, 'r', encoding='utf-8') as file:
                        csv_reader = csv.DictReader(file)
                        enriched_leads = list(csv_reader)
                    
                    # Update database
                    updates = 0
                    for lead in enriched_leads:
                        if 'id' in lead and lead['id']:
                            company_id = lead['id']
                            
                            # Update contacts table with LinkedIn URL and email
                            if 'linkedin_url' in lead and lead['linkedin_url']:
                                self.db.cursor.execute(
                                    "UPDATE contacts SET linkedin_url = ?, updated_at = CURRENT_TIMESTAMP WHERE company_id = ?",
                                    (lead['linkedin_url'], company_id)
                                )
                            
                            if 'email' in lead and lead['email'] and lead['email'] != 'N/A':
                                self.db.cursor.execute(
                                    "UPDATE contacts SET email = ?, updated_at = CURRENT_TIMESTAMP WHERE company_id = ?",
                                    (lead['email'], company_id)
                                )
                            
                            updates += 1
                    
                    self.db.conn.commit()
                    self.logger.info(f"Updated {updates} leads in the database")
                    
                    # Close the database connection
                    self.db.close()
            
            return True
        except Exception as e:
            self.logger.error(f"Error in LinkedIn profile finder process: {e}")
            return False
    
    def run_linkedin_automation(self):
        """Run the LinkedIn automation component"""
        if not self.config.get('linkedin_automation', {}).get('enabled', True):
            self.logger.info("LinkedIn automation is disabled in configuration")
            return False
        
        self.logger.info("Starting LinkedIn automation process")
        
        try:
            # Initialize the LinkedIn automation
            linkedin = LinkedInAutomation()
            
            # Connect to the database
            if not self.db.connect():
                self.logger.error("Failed to connect to database")
                return False
            
            # Get leads from database
            connection_limit = self.config.get('linkedin_automation', {}).get('connection_limit_per_day', 25)
            message_limit = self.config.get('linkedin_automation', {}).get('message_limit_per_day', 20)
            
            self.logger.info(f"Loading leads from database for LinkedIn automation")
            
            # Get leads with status 'New' or 'Connection Requested'
            leads = []
            self.db.cursor.execute('''
            SELECT c.id, c.company_name, c.website, c.industry, c.company_size, 
                   c.current_chatbot, c.address, c.city, c.state, c.zipcode, 
                   c.country, ct.id as contact_id, ct.first_name, ct.last_name, ct.email, ct.phone,
                   ct.position, ct.linkedin_url, ls.status
            FROM companies c
            LEFT JOIN contacts ct ON c.id = ct.company_id
            LEFT JOIN lead_status ls ON c.id = ls.company_id
            WHERE ls.status IN ('New', 'Connection Requested')
            AND ct.linkedin_url IS NOT NULL
            AND ct.linkedin_url != ''
            ''')
            
            columns = [column[0] for column in self.db.cursor.description]
            
            for row in self.db.cursor.fetchall():
                lead = dict(zip(columns, row))
                leads.append(lead)
            
            self.logger.info(f"Loaded {len(leads)} leads from database")
            
            # Close the database connection temporarily
            self.db.close()
            
            # Run the LinkedIn automation
            if leads:
                linkedin.leads = leads
                
                # Determine which industries to target
                industries = list(linkedin.config['search_filters'].keys())
                
                # Determine which actions to perform
                new_leads = [lead for lead in leads if lead.get('status') == 'New']
                connection_leads = [lead for lead in leads if lead.get('status') == 'Connection Requested']
                
                actions = []
                if new_leads:
                    actions.append('connection')
                if connection_leads:
                    actions.append('follow_up')
                
                # Set limits
                limits = {
                    'connection': min(connection_limit, len(new_leads)),
                    'follow_up': min(message_limit, len(connection_leads))
                }
                
                # Run the automation
                total_actions = linkedin.run(industries, actions, limits)
                
                self.logger.info(f"LinkedIn automation completed. Total actions: {total_actions}")
                
                # Update the database with LinkedIn actions
                if total_actions > 0:
                    # Reconnect to the database
                    if not self.db.connect():
                        self.logger.error("Failed to connect to database")
                        return False
                    
                    # Create a LinkedIn campaign
                    campaign_id = self.db.create_linkedin_campaign(
                        f"LinkedIn Campaign {self.timestamp}",
                        "Automated LinkedIn campaign",
                        "Active"
                    )
                    
                    if campaign_id:
                        # Add templates
                        connection_template_id = self.db.add_linkedin_template(
                            campaign_id,
                            'connection_request',
                            "Connection request template"
                        )
                        
                        followup_template_id = self.db.add_linkedin_template(
                            campaign_id,
                            'follow_up',
                            "Follow-up message template"
                        )
                        
                        # Record actions
                        for action in linkedin.actions_log:
                            if action['action_type'] == 'connection_request':
                                # Find the lead
                                for lead in new_leads:
                                    if f"{lead.get('first_name', '')} {lead.get('last_name', '')}" in action['target']:
                                        # Record the connection request
                                        self.db.record_linkedin_connection_sent(
                                            lead['contact_id'],
                                            connection_template_id,
                                            campaign_id
                                        )
                                        
                                        # Update lead status
                                        self.db.update_lead_status(
                                            lead['id'],
                                            'Connection Requested',
                                            next_action='Check Connection Status',
                                            next_action_date=(datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
                                        )
                                        
                                        break
                            
                            elif action['action_type'] == 'follow_up_message':
                                # Find the lead
                                for lead in connection_leads:
                                    if f"{lead.get('first_name', '')} {lead.get('last_name', '')}" in action['target']:
                                        # Record the interaction
                                        self.db.record_interaction(
                                            lead['id'],
                                            lead['contact_id'],
                                            'LinkedIn Message',
                                            'LinkedIn',
                                            f"Follow-up message sent: {action['notes']}"
                                        )
                                        
                                        # Update lead status
                                        self.db.update_lead_status(
                                            lead['id'],
                                            'Message Sent',
                                            next_action='Check Response',
                                            next_action_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
                                        )
                                        
                                        break
                    
                    self.db.conn.commit()
                    self.logger.info(f"Updated database with LinkedIn actions")
                    
                    # Close the database connection
                    self.db.close()
            
            return True
        except Exception as e:
            self.logger.error(f"Error in LinkedIn automation process: {e}")
            return False
    
    def run_email_outreach(self):
        """Run the email outreach component"""
        if not self.config.get('email_outreach', {}).get('enabled', True):
            self.logger.info("Email outreach is disabled in configuration")
            return False
        
        self.logger.info("Starting email outreach process")
        
        try:
            # Initialize the email template generator
            email_generator = EmailTemplateGenerator()
            
            # Connect to the database
            if not self.db.connect():
                self.logger.error("Failed to connect to database")
                return False
            
            # Get leads from database
            emails_per_day = self.config.get('email_outreach', {}).get('emails_per_day', 50)
            follow_up_days = self.config.get('email_outreach', {}).get('follow_up_days', 3)
            max_follow_ups = self.config.get('email_outreach', {}).get('max_follow_ups', 2)
            
            self.logger.info(f"Loading leads from database for email outreach")
            
            # Get leads with status 'New' or 'Contacted' and valid email addresses
            leads = []
            self.db.cursor.execute('''
            SELECT c.id, c.company_name, c.website, c.industry, c.company_size, 
                   c.current_chatbot, c.address, c.city, c.state, c.zipcode, 
                   c.country, ct.id as contact_id, ct.first_name, ct.last_name, ct.email, ct.phone,
                   ct.position, ls.status, ls.last_contacted,
                   (SELECT COUNT(*) FROM interactions i WHERE i.company_id = c.id AND i.interaction_type = 'Email Sent') as email_count
            FROM companies c
            LEFT JOIN contacts ct ON c.id = ct.company_id
            LEFT JOIN lead_status ls ON c.id = ls.company_id
            WHERE ls.status IN ('New', 'Contacted')
            AND ct.email IS NOT NULL
            AND ct.email != ''
            AND ct.email != 'N/A'
            ''')
            
            columns = [column[0] for column in self.db.cursor.description]
            
            for row in self.db.cursor.fetchall():
                lead = dict(zip(columns, row))
                leads.append(lead)
            
            self.logger.info(f"Loaded {len(leads)} leads from database")
            
            # Filter leads for initial outreach and follow-ups
            initial_outreach_leads = []
            follow_up_leads = []
            
            for lead in leads:
                email_count = int(lead.get('email_count', 0))
                
                if email_count == 0:
                    # No emails sent yet, add to initial outreach
                    initial_outreach_leads.append(lead)
                elif email_count <= max_follow_ups:
                    # Check if it's time for a follow-up
                    last_contacted = lead.get('last_contacted')
                    if last_contacted:
                        last_contacted_date = datetime.strptime(last_contacted, "%Y-%m-%d %H:%M:%S")
                        days_since_contact = (datetime.now() - last_contacted_date).days
                        
                        if days_since_contact >= follow_up_days:
                            follow_up_leads.append(lead)
            
            self.logger.info(f"Found {len(initial_outreach_leads)} leads for initial outreach")
            self.logger.info(f"Found {len(follow_up_leads)} leads for follow-up")
            
            # Limit the number of emails to send
            total_emails = min(emails_per_day, len(initial_outreach_leads) + len(follow_up_leads))
            
            # Allocate emails between initial outreach and follow-ups (prioritize follow-ups)
            follow_up_count = min(len(follow_up_leads), total_emails)
            initial_count = min(len(initial_outreach_leads), total_emails - follow_up_count)
            
            follow_up_leads = follow_up_leads[:follow_up_count]
            initial_outreach_leads = initial_outreach_leads[:initial_count]
            
            self.logger.info(f"Will send {initial_count} initial outreach emails and {follow_up_count} follow-up emails")
            
            # Generate personalized templates
            if initial_outreach_leads or follow_up_leads:
                # Create an email campaign
                campaign_id = self.db.create_email_campaign(
                    f"Email Campaign {self.timestamp}",
                    "Automated email campaign",
                    "Active"
                )
                
                if not campaign_id:
                    self.logger.error("Failed to create email campaign")
                    self.db.close()
                    return False
                
                # Process initial outreach emails
                if initial_outreach_leads:
                    self.logger.info("Processing initial outreach emails")
                    
                    for lead in initial_outreach_leads:
                        # Determine the industry
                        industry = lead.get('industry', '').lower()
                        template_industry = 'smes'  # Default
                        
                        if 'market' in industry or 'digital' in industry or 'agency' in industry:
                            template_industry = 'digital_marketing'
                        elif 'saas' in industry or 'software' in industry or 'tech' in industry:
                            template_industry = 'saas_companies'
                        elif 'enterprise' in industry or 'it' in industry or 'information technology' in industry:
                            template_industry = 'enterprise_it'
                        elif 'service' in industry or 'plumb' in industry or 'electric' in industry:
                            template_industry = 'service_businesses'
                        
                        # Generate personalized template
                        template = email_generator.generate_personalized_template(lead, 'initial_outreach', template_industry)
                        
                        # Add template to campaign
                        template_id = self.db.add_email_template(
                            campaign_id,
                            'initial_outreach',
                            template['subject'],
                            template['body']
                        )
                        
                        if template_id:
                            # Record email sent
                            self.db.record_email_sent(
                                lead['contact_id'],
                                template_id,
                                campaign_id
                            )
                            
                            self.logger.info(f"Recorded initial outreach email to {lead.get('first_name', '')} {lead.get('last_name', '')} at {lead.get('company_name', '')}")
                
                # Process follow-up emails
                if follow_up_leads:
                    self.logger.info("Processing follow-up emails")
                    
                    for lead in follow_up_leads:
                        # Determine the industry
                        industry = lead.get('industry', '').lower()
                        template_industry = 'smes'  # Default
                        
                        if 'market' in industry or 'digital' in industry or 'agency' in industry:
                            template_industry = 'digital_marketing'
                        elif 'saas' in industry or 'software' in industry or 'tech' in industry:
                            template_industry = 'saas_companies'
                        elif 'enterprise' in industry or 'it' in industry or 'information technology' in industry:
                            template_industry = 'enterprise_it'
                        elif 'service' in industry or 'plumb' in industry or 'electric' in industry:
                            template_industry = 'service_businesses'
                        
                        # Determine which follow-up template to use
                        email_count = int(lead.get('email_count', 0))
                        template_type = 'follow_up'
                        
                        if email_count >= max_follow_ups:
                            template_type = 'final_attempt'
                        
                        # Generate personalized template
                        template = email_generator.generate_personalized_template(lead, template_type, template_industry)
                        
                        # Add template to campaign
                        template_id = self.db.add_email_template(
                            campaign_id,
                            template_type,
                            template['subject'],
                            template['body']
                        )
                        
                        if template_id:
                            # Record email sent
                            self.db.record_email_sent(
                                lead['contact_id'],
                                template_id,
                                campaign_id
                            )
                            
                            self.logger.info(f"Recorded {template_type} email to {lead.get('first_name', '')} {lead.get('last_name', '')} at {lead.get('company_name', '')}")
                
                self.db.conn.commit()
                self.logger.info(f"Email outreach completed. Sent {initial_count + follow_up_count} emails")
            
            # Close the database connection
            self.db.close()
            
            return True
        except Exception as e:
            self.logger.error(f"Error in email outreach process: {e}")
            return False
    
    def generate_report(self):
        """Generate a report of the lead generation status"""
        self.logger.info("Generating lead generation report")
        
        try:
            # Connect to the database
            if not self.db.connect():
                self.logger.error("Failed to connect to database")
                return False
            
            # Get lead statistics
            lead_count = self.db.get_lead_count()
            leads_by_status = self.db.get_leads_by_status_count()
            leads_by_industry = self.db.get_leads_by_industry_count()
            
            # Get leads for follow-up
            follow_up_leads = self.db.get_leads_for_follow_up(7)  # Next 7 days
            
            # Create the report
            report_dir = '/home/ubuntu/lead_generation/automation/reports'
            report_file = f"{report_dir}/lead_generation_report_{self.timestamp}.html"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Lead Generation Report - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1, h2 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .summary {{ display: flex; justify-content: space-between; margin-bottom: 20px; }}
        .summary-box {{ background-color: #f2f2f2; padding: 15px; border-radius: 5px; width: 30%; }}
        .chart {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>Lead Generation Report</h1>
    <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="summary">
        <div class="summary-box">
            <h3>Total Leads</h3>
            <p style="font-size: 24px;">{lead_count}</p>
        </div>
        <div class="summary-box">
            <h3>Leads by Status</h3>
            <p>{', '.join([f"{status}: {count}" for status, count in leads_by_status])}</p>
        </div>
        <div class="summary-box">
            <h3>Top Industries</h3>
            <p>{', '.join([f"{industry}: {count}" for industry, count in leads_by_industry[:3]])}</p>
        </div>
    </div>
    
    <h2>Lead Status Breakdown</h2>
    <table>
        <tr>
            <th>Status</th>
            <th>Count</th>
            <th>Percentage</th>
        </tr>
""")
                
                for status, count in leads_by_status:
                    percentage = (count / lead_count) * 100 if lead_count > 0 else 0
                    f.write(f"""        <tr>
            <td>{status}</td>
            <td>{count}</td>
            <td>{percentage:.1f}%</td>
        </tr>
""")
                
                f.write(f"""    </table>
    
    <h2>Industry Breakdown</h2>
    <table>
        <tr>
            <th>Industry</th>
            <th>Count</th>
            <th>Percentage</th>
        </tr>
""")
                
                for industry, count in leads_by_industry:
                    percentage = (count / lead_count) * 100 if lead_count > 0 else 0
                    f.write(f"""        <tr>
            <td>{industry}</td>
            <td>{count}</td>
            <td>{percentage:.1f}%</td>
        </tr>
""")
                
                f.write(f"""    </table>
    
    <h2>Upcoming Follow-ups ({len(follow_up_leads)})</h2>
    <table>
        <tr>
            <th>Company</th>
            <th>Contact</th>
            <th>Status</th>
            <th>Next Action</th>
            <th>Next Action Date</th>
        </tr>
""")
                
                for lead in follow_up_leads:
                    f.write(f"""        <tr>
            <td>{lead['company_name']}</td>
            <td>{lead.get('first_name', '')} {lead.get('last_name', '')}</td>
            <td>{lead['status']}</td>
            <td>{lead['next_action']}</td>
            <td>{lead['next_action_date']}</td>
        </tr>
""")
                
                f.write(f"""    </table>
    
    <h2>Recent Activity</h2>
    <p>The following actions were performed in the last automation run:</p>
    <ul>
        <li>Web scraping: {self.config.get('web_scraping', {}).get('enabled', True)}</li>
        <li>LinkedIn profile finder: {self.config.get('linkedin_automation', {}).get('profile_finder_enabled', True)}</li>
        <li>LinkedIn automation: {self.config.get('linkedin_automation', {}).get('enabled', True)}</li>
        <li>Email outreach: {self.config.get('email_outreach', {}).get('enabled', True)}</li>
    </ul>
    
    <p>For more detailed information, please check the log file: {self.log_file}</p>
</body>
</html>""")
            
            self.logger.info(f"Report generated: {report_file}")
            
            # Export leads to CSV
            export_file = f"{report_dir}/leads_export_{self.timestamp}.csv"
            self.db.export_to_csv(export_file)
            
            # Close the database connection
            self.db.close()
            
            return report_file
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            return False
    
    def run(self):
        """Run the complete lead generation automation process"""
        self.logger.info("Starting lead generation automation process")
        
        # Connect to the database
        if not self.db.connect():
            self.logger.error("Failed to connect to database")
            return False
        
        # Create tables if they don't exist
        self.db.create_tables()
        
        # Close the connection for now
        self.db.close()
        
        # Backup the database
        self.backup_database()
        
        # Run the components
        web_scraping_result = self.run_web_scraping()
        self.logger.info(f"Web scraping completed: {web_scraping_result}")
        
        linkedin_profile_finder_result = self.run_linkedin_profile_finder()
        self.logger.info(f"LinkedIn profile finder completed: {linkedin_profile_finder_result}")
        
        linkedin_automation_result = self.run_linkedin_automation()
        self.logger.info(f"LinkedIn automation completed: {linkedin_automation_result}")
        
        email_outreach_result = self.run_email_outreach()
        self.logger.info(f"Email outreach completed: {email_outreach_result}")
        
        # Generate a report
        report_file = self.generate_report()
        
        self.logger.info("Lead generation automation process completed")
        
        return {
            'web_scraping': web_scraping_result,
            'linkedin_profile_finder': linkedin_profile_finder_result,
            'linkedin_automation': linkedin_automation_result,
            'email_outreach': email_outreach_result,
            'report_file': report_file
        }

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Lead Generation Automation')
    
    parser.add_argument('--config', type=str, default=None,
                        help='Path to configuration file')
    
    parser.add_argument('--web-scraping-only', action='store_true',
                        help='Run only the web scraping component')
    
    parser.add_argument('--linkedin-only', action='store_true',
                        help='Run only the LinkedIn automation component')
    
    parser.add_argument('--email-only', action='store_true',
                        help='Run only the email outreach component')
    
    parser.add_argument('--report-only', action='store_true',
                        help='Generate only the report')
    
    parser.add_argument('--setup-database', action='store_true',
                        help='Set up the database with sample data')
    
    parser.add_argument('--sample-size', type=int, default=50,
                        help='Number of sample companies to generate')
    
    return parser.parse_args()

def main():
    """Main function to run the lead generation automation"""
    print(f"Starting lead generation automation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Parse arguments
    args = parse_arguments()
    
    # Initialize the automation
    automation = LeadGenerationAutomation(args.config)
    
    # Set up the database with sample data if requested
    if args.setup_database:
        print("Setting up database with sample data")
        
        # Connect to the database
        if not automation.db.connect():
            print("Failed to connect to database")
            return 1
        
        # Create tables
        automation.db.create_tables()
        
        # Generate sample data
        automation.db.generate_sample_data(args.sample_size)
        
        # Close the connection
        automation.db.close()
        
        print(f"Database set up with {args.sample_size} sample companies")
        return 0
    
    # Run specific components if requested
    if args.web_scraping_only:
        print("Running only web scraping component")
        result = automation.run_web_scraping()
        print(f"Web scraping completed: {result}")
        return 0
    
    if args.linkedin_only:
        print("Running only LinkedIn automation component")
        profile_result = automation.run_linkedin_profile_finder()
        automation_result = automation.run_linkedin_automation()
        print(f"LinkedIn profile finder completed: {profile_result}")
        print(f"LinkedIn automation completed: {automation_result}")
        return 0
    
    if args.email_only:
        print("Running only email outreach component")
        result = automation.run_email_outreach()
        print(f"Email outreach completed: {result}")
        return 0
    
    if args.report_only:
        print("Generating only report")
        report_file = automation.generate_report()
        print(f"Report generated: {report_file}")
        return 0
    
    # Run the complete automation process
    results = automation.run()
    
    print(f"Lead generation automation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results: {results}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
