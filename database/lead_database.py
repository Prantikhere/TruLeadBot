#!/usr/bin/env python3
"""
Lead Tracking Database for AI Chatbot Startup
This script creates and manages a comprehensive lead tracking database
"""

import os
import sys
import sqlite3
import csv
import json
from datetime import datetime, timedelta
import argparse
import random

class LeadDatabase:
    def __init__(self, db_path=None):
        """Initialize the lead tracking database"""
        if not db_path:
            db_path = '/home/ubuntu/lead_generation/database/leads.db'
        
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def connect(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # This enables column access by name
            self.cursor = self.conn.cursor()
            print(f"Connected to database at {self.db_path}")
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def create_tables(self):
        """Create the necessary tables if they don't exist"""
        try:
            # Companies table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                website TEXT,
                industry TEXT,
                company_size TEXT,
                current_chatbot TEXT,
                description TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zipcode TEXT,
                country TEXT,
                source TEXT,
                scraped_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Contacts table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                first_name TEXT,
                last_name TEXT,
                position TEXT,
                email TEXT,
                phone TEXT,
                linkedin_url TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
            ''')
            
            # Interactions table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                contact_id INTEGER,
                interaction_type TEXT,
                channel TEXT,
                interaction_date TIMESTAMP,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                FOREIGN KEY (contact_id) REFERENCES contacts (id)
            )
            ''')
            
            # Lead status table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lead_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                status TEXT,
                score INTEGER,
                last_contacted TIMESTAMP,
                next_action TEXT,
                next_action_date TIMESTAMP,
                assigned_to TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
            ''')
            
            # Email campaigns table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Email templates table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                template_type TEXT,
                subject TEXT,
                body TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES email_campaigns (id)
            )
            ''')
            
            # Email tracking table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                template_id INTEGER,
                campaign_id INTEGER,
                sent_date TIMESTAMP,
                opened BOOLEAN DEFAULT 0,
                opened_date TIMESTAMP,
                clicked BOOLEAN DEFAULT 0,
                clicked_date TIMESTAMP,
                replied BOOLEAN DEFAULT 0,
                replied_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contact_id) REFERENCES contacts (id),
                FOREIGN KEY (template_id) REFERENCES email_templates (id),
                FOREIGN KEY (campaign_id) REFERENCES email_campaigns (id)
            )
            ''')
            
            # LinkedIn campaigns table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS linkedin_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # LinkedIn message templates table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS linkedin_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                template_type TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES linkedin_campaigns (id)
            )
            ''')
            
            # LinkedIn tracking table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS linkedin_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                template_id INTEGER,
                campaign_id INTEGER,
                connection_sent BOOLEAN DEFAULT 0,
                connection_sent_date TIMESTAMP,
                connection_accepted BOOLEAN DEFAULT 0,
                connection_accepted_date TIMESTAMP,
                message_sent BOOLEAN DEFAULT 0,
                message_sent_date TIMESTAMP,
                replied BOOLEAN DEFAULT 0,
                replied_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contact_id) REFERENCES contacts (id),
                FOREIGN KEY (template_id) REFERENCES linkedin_templates (id),
                FOREIGN KEY (campaign_id) REFERENCES linkedin_campaigns (id)
            )
            ''')
            
            # Tags table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Company tags junction table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS company_tags (
                company_id INTEGER,
                tag_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (company_id, tag_id),
                FOREIGN KEY (company_id) REFERENCES companies (id),
                FOREIGN KEY (tag_id) REFERENCES tags (id)
            )
            ''')
            
            # Create indexes for better performance
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_companies_industry ON companies (industry)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_company_id ON contacts (company_id)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_lead_status_company_id ON lead_status (company_id)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_lead_status_status ON lead_status (status)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_interactions_company_id ON interactions (company_id)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_interactions_contact_id ON interactions (contact_id)')
            
            self.conn.commit()
            print("Database tables created successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            return False
    
    def import_from_csv(self, csv_file):
        """Import leads from a CSV file"""
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                leads_imported = 0
                
                for row in csv_reader:
                    # Insert into companies table
                    company_id = self.insert_company(row)
                    
                    # If we have contact information, insert into contacts table
                    if company_id and (row.get('first_name') or row.get('email') or row.get('phone')):
                        self.insert_contact(company_id, row)
                    
                    # Create initial lead status
                    if company_id:
                        self.insert_lead_status(company_id)
                        leads_imported += 1
                
                self.conn.commit()
                print(f"Imported {leads_imported} leads from {csv_file}")
                return leads_imported
        except Exception as e:
            print(f"Error importing from CSV: {e}")
            return 0
    
    def import_from_json(self, json_file):
        """Import leads from a JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                leads = json.load(file)
                leads_imported = 0
                
                for lead in leads:
                    # Insert into companies table
                    company_id = self.insert_company(lead)
                    
                    # If we have contact information, insert into contacts table
                    if company_id and (lead.get('first_name') or lead.get('email') or lead.get('phone')):
                        self.insert_contact(company_id, lead)
                    
                    # Create initial lead status
                    if company_id:
                        self.insert_lead_status(company_id)
                        leads_imported += 1
                
                self.conn.commit()
                print(f"Imported {leads_imported} leads from {json_file}")
                return leads_imported
        except Exception as e:
            print(f"Error importing from JSON: {e}")
            return 0
    
    def insert_company(self, data):
        """Insert a company record and return the ID"""
        try:
            # Extract location data if available
            address = data.get('address', '')
            location = data.get('location', '')
            city = data.get('city', '')
            state = data.get('state', '')
            zipcode = data.get('zipcode', '')
            country = data.get('country', '')
            
            # Try to parse location field if it exists and other fields are empty
            if location and not (city or state or country):
                parts = location.split(',')
                if len(parts) >= 1:
                    city = parts[0].strip()
                if len(parts) >= 2:
                    state = parts[1].strip()
                if len(parts) >= 3:
                    country = parts[2].strip()
            
            # Check if company already exists
            self.cursor.execute(
                "SELECT id FROM companies WHERE company_name = ? AND website = ?",
                (data.get('company_name', ''), data.get('website', ''))
            )
            existing = self.cursor.fetchone()
            
            if existing:
                return existing[0]
            
            # Insert new company
            self.cursor.execute('''
            INSERT INTO companies (
                company_name, website, industry, company_size, current_chatbot, 
                description, address, city, state, zipcode, country, source, scraped_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('company_name', ''),
                data.get('website', ''),
                data.get('industry', ''),
                data.get('company_size', ''),
                data.get('current_chatbot', ''),
                data.get('description', ''),
                address,
                city,
                state,
                zipcode,
                country,
                data.get('source', ''),
                data.get('scraped_date', datetime.now().strftime("%Y-%m-%d"))
            ))
            
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting company: {e}")
            return None
    
    def insert_contact(self, company_id, data):
        """Insert a contact record"""
        try:
            # Parse name from email if first_name and last_name are not provided
            email = data.get('email', '')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            
            if not first_name and not last_name and '@' in email:
                # Try to extract name from email
                name_part = email.split('@')[0]
                if '.' in name_part:
                    parts = name_part.split('.')
                    if len(parts) >= 2:
                        first_name = parts[0].capitalize()
                        last_name = parts[1].capitalize()
            
            self.cursor.execute('''
            INSERT INTO contacts (
                company_id, first_name, last_name, position, email, phone, linkedin_url, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                company_id,
                first_name,
                last_name,
                data.get('position', ''),
                email,
                data.get('phone', ''),
                data.get('linkedin_url', ''),
                data.get('notes', '')
            ))
            
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting contact: {e}")
            return None
    
    def insert_lead_status(self, company_id):
        """Insert initial lead status"""
        try:
            self.cursor.execute('''
            INSERT INTO lead_status (
                company_id, status, score, next_action, next_action_date
            ) VALUES (?, ?, ?, ?, ?)
            ''', (
                company_id,
                'New',
                0,
                'Initial Outreach',
                (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            ))
            
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting lead status: {e}")
            return None
    
    def record_interaction(self, company_id, contact_id, interaction_type, channel, notes=''):
        """Record an interaction with a lead"""
        try:
            self.cursor.execute('''
            INSERT INTO interactions (
                company_id, contact_id, interaction_type, channel, interaction_date, notes
            ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                company_id,
                contact_id,
                interaction_type,
                channel,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                notes
            ))
            
            # Update lead status
            self.cursor.execute('''
            UPDATE lead_status 
            SET last_contacted = ?, updated_at = CURRENT_TIMESTAMP
            WHERE company_id = ?
            ''', (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                company_id
            ))
            
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error recording interaction: {e}")
            return None
    
    def update_lead_status(self, company_id, status, score=None, next_action=None, next_action_date=None, assigned_to=None):
        """Update the status of a lead"""
        try:
            # Build the update query dynamically based on provided parameters
            update_parts = ["status = ?", "updated_at = CURRENT_TIMESTAMP"]
            params = [status]
            
            if score is not None:
                update_parts.append("score = ?")
                params.append(score)
            
            if next_action:
                update_parts.append("next_action = ?")
                params.append(next_action)
            
            if next_action_date:
                update_parts.append("next_action_date = ?")
                params.append(next_action_date)
            
            if assigned_to:
                update_parts.append("assigned_to = ?")
                params.append(assigned_to)
            
            # Add the company_id parameter
            params.append(company_id)
            
            # Execute the update query
            self.cursor.execute(f'''
            UPDATE lead_status 
            SET {", ".join(update_parts)}
            WHERE company_id = ?
            ''', params)
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating lead status: {e}")
            return False
    
    def create_email_campaign(self, name, description='', status='Draft'):
        """Create a new email campaign"""
        try:
            self.cursor.execute('''
            INSERT INTO email_campaigns (
                name, description, status, start_date
            ) VALUES (?, ?, ?, ?)
            ''', (
                name,
                description,
                status,
                datetime.now().strftime("%Y-%m-%d")
            ))
            
            campaign_id = self.cursor.lastrowid
            self.conn.commit()
            return campaign_id
        except sqlite3.Error as e:
            print(f"Error creating email campaign: {e}")
            return None
    
    def add_email_template(self, campaign_id, template_type, subject, body):
        """Add an email template to a campaign"""
        try:
            self.cursor.execute('''
            INSERT INTO email_templates (
                campaign_id, template_type, subject, body
            ) VALUES (?, ?, ?, ?)
            ''', (
                campaign_id,
                template_type,
                subject,
                body
            ))
            
            template_id = self.cursor.lastrowid
            self.conn.commit()
            return template_id
        except sqlite3.Error as e:
            print(f"Error adding email template: {e}")
            return None
    
    def record_email_sent(self, contact_id, template_id, campaign_id):
        """Record that an email was sent to a contact"""
        try:
            self.cursor.execute('''
            INSERT INTO email_tracking (
                contact_id, template_id, campaign_id, sent_date
            ) VALUES (?, ?, ?, ?)
            ''', (
                contact_id,
                template_id,
                campaign_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            
            tracking_id = self.cursor.lastrowid
            
            # Get the company_id for this contact
            self.cursor.execute("SELECT company_id FROM contacts WHERE id = ?", (contact_id,))
            result = self.cursor.fetchone()
            
            if result:
                company_id = result[0]
                
                # Record the interaction
                self.record_interaction(
                    company_id,
                    contact_id,
                    'Email Sent',
                    'Email',
                    f"Email sent as part of campaign {campaign_id}, template {template_id}"
                )
                
                # Update lead status
                self.update_lead_status(
                    company_id,
                    'Contacted',
                    next_action='Follow Up',
                    next_action_date=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
                )
            
            self.conn.commit()
            return tracking_id
        except sqlite3.Error as e:
            print(f"Error recording email sent: {e}")
            return None
    
    def create_linkedin_campaign(self, name, description='', status='Draft'):
        """Create a new LinkedIn campaign"""
        try:
            self.cursor.execute('''
            INSERT INTO linkedin_campaigns (
                name, description, status, start_date
            ) VALUES (?, ?, ?, ?)
            ''', (
                name,
                description,
                status,
                datetime.now().strftime("%Y-%m-%d")
            ))
            
            campaign_id = self.cursor.lastrowid
            self.conn.commit()
            return campaign_id
        except sqlite3.Error as e:
            print(f"Error creating LinkedIn campaign: {e}")
            return None
    
    def add_linkedin_template(self, campaign_id, template_type, message):
        """Add a LinkedIn message template to a campaign"""
        try:
            self.cursor.execute('''
            INSERT INTO linkedin_templates (
                campaign_id, template_type, message
            ) VALUES (?, ?, ?)
            ''', (
                campaign_id,
                template_type,
                message
            ))
            
            template_id = self.cursor.lastrowid
            self.conn.commit()
            return template_id
        except sqlite3.Error as e:
            print(f"Error adding LinkedIn template: {e}")
            return None
    
    def record_linkedin_connection_sent(self, contact_id, template_id, campaign_id):
        """Record that a LinkedIn connection request was sent to a contact"""
        try:
            self.cursor.execute('''
            INSERT INTO linkedin_tracking (
                contact_id, template_id, campaign_id, connection_sent, connection_sent_date
            ) VALUES (?, ?, ?, ?, ?)
            ''', (
                contact_id,
                template_id,
                campaign_id,
                1,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            
            tracking_id = self.cursor.lastrowid
            
            # Get the company_id for this contact
            self.cursor.execute("SELECT company_id FROM contacts WHERE id = ?", (contact_id,))
            result = self.cursor.fetchone()
            
            if result:
                company_id = result[0]
                
                # Record the interaction
                self.record_interaction(
                    company_id,
                    contact_id,
                    'LinkedIn Connection Request',
                    'LinkedIn',
                    f"Connection request sent as part of campaign {campaign_id}, template {template_id}"
                )
                
                # Update lead status
                self.update_lead_status(
                    company_id,
                    'Connection Requested',
                    next_action='Check Connection Status',
                    next_action_date=(datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
                )
            
            self.conn.commit()
            return tracking_id
        except sqlite3.Error as e:
            print(f"Error recording LinkedIn connection sent: {e}")
            return None
    
    def add_tag(self, name, description=''):
        """Add a new tag"""
        try:
            self.cursor.execute('''
            INSERT OR IGNORE INTO tags (name, description)
            VALUES (?, ?)
            ''', (name, description))
            
            # Get the tag ID (either the new one or the existing one)
            self.cursor.execute("SELECT id FROM tags WHERE name = ?", (name,))
            result = self.cursor.fetchone()
            
            self.conn.commit()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error adding tag: {e}")
            return None
    
    def tag_company(self, company_id, tag_name):
        """Tag a company with a specific tag"""
        try:
            # Make sure the tag exists
            tag_id = self.add_tag(tag_name)
            
            if not tag_id:
                return False
            
            # Add the tag to the company
            self.cursor.execute('''
            INSERT OR IGNORE INTO company_tags (company_id, tag_id)
            VALUES (?, ?)
            ''', (company_id, tag_id))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error tagging company: {e}")
            return False
    
    def get_companies_by_tag(self, tag_name):
        """Get all companies with a specific tag"""
        try:
            self.cursor.execute('''
            SELECT c.* FROM companies c
            JOIN company_tags ct ON c.id = ct.company_id
            JOIN tags t ON ct.tag_id = t.id
            WHERE t.name = ?
            ''', (tag_name,))
            
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting companies by tag: {e}")
            return []
    
    def get_leads_by_status(self, status):
        """Get all leads with a specific status"""
        try:
            self.cursor.execute('''
            SELECT c.*, ls.status, ls.score, ls.next_action, ls.next_action_date, ls.assigned_to
            FROM companies c
            JOIN lead_status ls ON c.id = ls.company_id
            WHERE ls.status = ?
            ''', (status,))
            
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting leads by status: {e}")
            return []
    
    def get_leads_by_industry(self, industry):
        """Get all leads in a specific industry"""
        try:
            self.cursor.execute('''
            SELECT c.*, ls.status, ls.score, ls.next_action, ls.next_action_date, ls.assigned_to
            FROM companies c
            JOIN lead_status ls ON c.id = ls.company_id
            WHERE c.industry LIKE ?
            ''', (f'%{industry}%',))
            
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting leads by industry: {e}")
            return []
    
    def get_leads_for_follow_up(self, days=3):
        """Get all leads that need follow-up within the specified number of days"""
        try:
            cutoff_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            
            self.cursor.execute('''
            SELECT c.*, ls.status, ls.score, ls.next_action, ls.next_action_date, ls.assigned_to
            FROM companies c
            JOIN lead_status ls ON c.id = ls.company_id
            WHERE ls.next_action_date <= ?
            ORDER BY ls.next_action_date ASC
            ''', (cutoff_date,))
            
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting leads for follow-up: {e}")
            return []
    
    def get_company_with_contacts(self, company_id):
        """Get a company and all its contacts"""
        try:
            # Get the company
            self.cursor.execute('''
            SELECT c.*, ls.status, ls.score, ls.next_action, ls.next_action_date, ls.assigned_to
            FROM companies c
            JOIN lead_status ls ON c.id = ls.company_id
            WHERE c.id = ?
            ''', (company_id,))
            
            company = self.cursor.fetchone()
            
            if not company:
                return None
            
            # Get the contacts
            self.cursor.execute('''
            SELECT * FROM contacts
            WHERE company_id = ?
            ''', (company_id,))
            
            contacts = self.cursor.fetchall()
            
            # Get the interactions
            self.cursor.execute('''
            SELECT * FROM interactions
            WHERE company_id = ?
            ORDER BY interaction_date DESC
            ''', (company_id,))
            
            interactions = self.cursor.fetchall()
            
            # Get the tags
            self.cursor.execute('''
            SELECT t.name FROM tags t
            JOIN company_tags ct ON t.id = ct.tag_id
            WHERE ct.company_id = ?
            ''', (company_id,))
            
            tags = [row[0] for row in self.cursor.fetchall()]
            
            # Combine everything into a single result
            result = {
                'company': dict(company),
                'contacts': [dict(contact) for contact in contacts],
                'interactions': [dict(interaction) for interaction in interactions],
                'tags': tags
            }
            
            return result
        except sqlite3.Error as e:
            print(f"Error getting company with contacts: {e}")
            return None
    
    def get_lead_count(self):
        """Get the total number of leads in the database"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM companies")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error getting lead count: {e}")
            return 0
    
    def get_leads_by_status_count(self):
        """Get lead counts grouped by status"""
        try:
            self.cursor.execute('''
            SELECT ls.status, COUNT(*) as count 
            FROM lead_status ls
            GROUP BY ls.status
            ORDER BY count DESC
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting leads by status count: {e}")
            return []
    
    def get_leads_by_industry_count(self):
        """Get lead counts grouped by industry"""
        try:
            self.cursor.execute('''
            SELECT industry, COUNT(*) as count 
            FROM companies 
            GROUP BY industry
            ORDER BY count DESC
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting leads by industry count: {e}")
            return []
    
    def export_to_csv(self, output_file):
        """Export all leads to a CSV file"""
        try:
            self.cursor.execute('''
            SELECT c.*, ls.status, ls.score, ls.next_action, ls.next_action_date, ls.assigned_to
            FROM companies c
            LEFT JOIN lead_status ls ON c.id = ls.company_id
            ''')
            
            rows = self.cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in self.cursor.description]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(column_names)
                writer.writerows([tuple(row) for row in rows])
            
            print(f"Exported {len(rows)} leads to {output_file}")
            return len(rows)
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return 0
    
    def generate_sample_data(self, num_companies=50):
        """Generate sample data for testing"""
        try:
            # Sample industries
            industries = [
                'Digital Marketing Agency',
                'SaaS Company',
                'Enterprise IT Solutions',
                'Small Business',
                'Service Business',
                'Plumbing',
                'Electrical Services',
                'Marketing Consultancy',
                'Software Development',
                'IT Support'
            ]
            
            # Sample company sizes
            company_sizes = [
                'Small (1-10)',
                'Medium (11-50)',
                'Large (51-200)',
                'Enterprise (201+)'
            ]
            
            # Sample chatbot platforms
            chatbot_platforms = [
                'None detected',
                'Intercom',
                'Drift',
                'Zendesk',
                'Freshchat',
                'HubSpot',
                'Tidio',
                'Tawk.to',
                'Custom solution'
            ]
            
            # Sample cities
            cities = [
                'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
                'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'San Francisco'
            ]
            
            # Sample states
            states = [
                'NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'FL', 'OH', 'NC', 'GA',
                'MI', 'NJ', 'VA', 'WA', 'MA'
            ]
            
            # Sample positions
            positions = [
                'CEO', 'CTO', 'CMO', 'Marketing Director', 'IT Director',
                'Owner', 'Founder', 'Marketing Manager', 'Digital Marketing Manager',
                'Head of IT', 'VP of Engineering', 'Product Manager', 'Operations Manager'
            ]
            
            # Sample first names
            first_names = [
                'John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Jennifer',
                'William', 'Elizabeth', 'James', 'Linda', 'Richard', 'Patricia', 'Thomas'
            ]
            
            # Sample last names
            last_names = [
                'Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson',
                'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris'
            ]
            
            # Sample statuses
            statuses = [
                'New', 'Contacted', 'Engaged', 'Qualified', 'Proposal Sent',
                'Negotiation', 'Won', 'Lost', 'On Hold'
            ]
            
            # Sample next actions
            next_actions = [
                'Initial Outreach', 'Follow Up', 'Schedule Demo', 'Send Proposal',
                'Check In', 'Schedule Meeting', 'Send Information', 'Qualify Need'
            ]
            
            # Sample tags
            tags = [
                'Hot Lead', 'Cold Lead', 'Referral', 'Website Visitor', 'Event Contact',
                'High Budget', 'Low Budget', 'Urgent Need', 'Long-term Prospect',
                'Competitor User', 'Technical Decision Maker', 'Business Decision Maker'
            ]
            
            # Generate companies
            for i in range(num_companies):
                company_name = f"Company {i+1}"
                website = f"https://www.company{i+1}.com"
                industry = random.choice(industries)
                company_size = random.choice(company_sizes)
                current_chatbot = random.choice(chatbot_platforms)
                city = random.choice(cities)
                state = random.choice(states)
                
                # Insert company
                self.cursor.execute('''
                INSERT INTO companies (
                    company_name, website, industry, company_size, current_chatbot, 
                    city, state, country, source, scraped_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    company_name,
                    website,
                    industry,
                    company_size,
                    current_chatbot,
                    city,
                    state,
                    'USA',
                    'Sample Data',
                    datetime.now().strftime("%Y-%m-%d")
                ))
                
                company_id = self.cursor.lastrowid
                
                # Generate 1-3 contacts per company
                num_contacts = random.randint(1, 3)
                for j in range(num_contacts):
                    first_name = random.choice(first_names)
                    last_name = random.choice(last_names)
                    position = random.choice(positions)
                    email = f"{first_name.lower()}.{last_name.lower()}@company{i+1}.com"
                    phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
                    
                    # Insert contact
                    self.cursor.execute('''
                    INSERT INTO contacts (
                        company_id, first_name, last_name, position, email, phone
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        company_id,
                        first_name,
                        last_name,
                        position,
                        email,
                        phone
                    ))
                    
                    contact_id = self.cursor.lastrowid
                    
                    # Generate 0-5 interactions per contact
                    num_interactions = random.randint(0, 5)
                    for k in range(num_interactions):
                        interaction_type = random.choice(['Email', 'Phone Call', 'LinkedIn', 'Meeting', 'Demo'])
                        channel = random.choice(['Email', 'Phone', 'LinkedIn', 'In Person', 'Video Call'])
                        interaction_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
                        notes = f"Sample interaction {k+1} with {first_name} {last_name}"
                        
                        # Insert interaction
                        self.cursor.execute('''
                        INSERT INTO interactions (
                            company_id, contact_id, interaction_type, channel, interaction_date, notes
                        ) VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                            company_id,
                            contact_id,
                            interaction_type,
                            channel,
                            interaction_date,
                            notes
                        ))
                
                # Insert lead status
                status = random.choice(statuses)
                score = random.randint(0, 100)
                next_action = random.choice(next_actions)
                next_action_date = (datetime.now() + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")
                
                self.cursor.execute('''
                INSERT INTO lead_status (
                    company_id, status, score, next_action, next_action_date
                ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    company_id,
                    status,
                    score,
                    next_action,
                    next_action_date
                ))
                
                # Add 1-3 tags per company
                num_tags = random.randint(1, 3)
                selected_tags = random.sample(tags, num_tags)
                for tag in selected_tags:
                    self.tag_company(company_id, tag)
            
            self.conn.commit()
            print(f"Generated sample data: {num_companies} companies")
            return num_companies
        except sqlite3.Error as e:
            print(f"Error generating sample data: {e}")
            return 0
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Lead Tracking Database')
    
    parser.add_argument('--db-path', type=str, 
                        default='/home/ubuntu/lead_generation/database/leads.db',
                        help='Path to the SQLite database file')
    
    parser.add_argument('--import-csv', type=str, default=None,
                        help='Import leads from a CSV file')
    
    parser.add_argument('--import-json', type=str, default=None,
                        help='Import leads from a JSON file')
    
    parser.add_argument('--export-csv', type=str, default=None,
                        help='Export leads to a CSV file')
    
    parser.add_argument('--generate-sample', action='store_true',
                        help='Generate sample data for testing')
    
    parser.add_argument('--sample-size', type=int, default=50,
                        help='Number of sample companies to generate')
    
    return parser.parse_args()

def main():
    """Main function to run the lead tracking database"""
    print(f"Starting lead tracking database at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Parse arguments
    args = parse_arguments()
    
    # Initialize the database
    db = LeadDatabase(args.db_path)
    if not db.connect():
        return 1
    
    # Create tables
    db.create_tables()
    
    # Import data if requested
    if args.import_csv and os.path.exists(args.import_csv):
        db.import_from_csv(args.import_csv)
    
    if args.import_json and os.path.exists(args.import_json):
        db.import_from_json(args.import_json)
    
    # Generate sample data if requested
    if args.generate_sample:
        db.generate_sample_data(args.sample_size)
    
    # Export data if requested
    if args.export_csv:
        db.export_to_csv(args.export_csv)
    
    # Print some stats
    print(f"\nTotal leads in database: {db.get_lead_count()}")
    
    print("\nLeads by status:")
    for status, count in db.get_leads_by_status_count():
        print(f"  {status}: {count}")
    
    print("\nLeads by industry:")
    for industry, count in db.get_leads_by_industry_count():
        print(f"  {industry}: {count}")
    
    # Close connection
    db.close()
    
    print(f"Lead tracking database completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
