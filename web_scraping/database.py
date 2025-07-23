#!/usr/bin/env python3
"""
Lead Database Creator for AI Chatbot Startup
This script creates a SQLite database for storing and managing leads
"""

import sqlite3
import os
import csv
import json
from datetime import datetime

# Database path
DB_PATH = '/home/ubuntu/lead_generation/data/leads_database.db'

class LeadDatabase:
    def __init__(self, db_path=DB_PATH):
        """Initialize the database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
            ''')
            
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
                    
                    # If we have email, insert into contacts table
                    if 'email' in row and row['email'] != 'N/A':
                        self.insert_contact(company_id, row)
                    
                    # Create initial lead status
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
                    
                    # If we have email, insert into contacts table
                    if 'email' in lead and lead['email'] != 'N/A':
                        self.insert_contact(company_id, lead)
                    
                    # Create initial lead status
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
            address = data.get('address', 'N/A')
            location = data.get('location', '')
            city = state = zipcode = country = 'N/A'
            
            # Try to parse location field if it exists
            if location:
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
                (data.get('company_name', 'N/A'), data.get('website', 'N/A'))
            )
            existing = self.cursor.fetchone()
            
            if existing:
                return existing[0]
            
            # Insert new company
            self.cursor.execute('''
            INSERT INTO companies (
                company_name, website, industry, current_chatbot, 
                address, city, state, zipcode, country, source, scraped_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('company_name', 'N/A'),
                data.get('website', 'N/A'),
                data.get('industry', 'N/A'),
                data.get('current_chatbot', 'Unknown'),
                address,
                city,
                state,
                zipcode,
                country,
                data.get('source', 'N/A'),
                data.get('scraped_date', datetime.now().strftime("%Y-%m-%d"))
            ))
            
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting company: {e}")
            return None
    
    def insert_contact(self, company_id, data):
        """Insert a contact record"""
        try:
            # Parse name from email if available
            email = data.get('email', 'N/A')
            first_name = last_name = 'N/A'
            
            if '@' in email and email != 'N/A':
                # Try to extract name from email
                name_part = email.split('@')[0]
                if '.' in name_part:
                    parts = name_part.split('.')
                    if len(parts) >= 2:
                        first_name = parts[0].capitalize()
                        last_name = parts[1].capitalize()
            
            self.cursor.execute('''
            INSERT INTO contacts (
                company_id, first_name, last_name, email, phone
            ) VALUES (?, ?, ?, ?, ?)
            ''', (
                company_id,
                first_name,
                last_name,
                email,
                data.get('phone', 'N/A')
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
                company_id, status, score
            ) VALUES (?, ?, ?)
            ''', (
                company_id,
                'New',
                0
            ))
            
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting lead status: {e}")
            return None
    
    def get_lead_count(self):
        """Get the total number of leads in the database"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM companies")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error getting lead count: {e}")
            return 0
    
    def get_leads_by_industry(self):
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
            print(f"Error getting leads by industry: {e}")
            return []
    
    def get_leads_by_status(self):
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
            print(f"Error getting leads by status: {e}")
            return []
    
    def export_to_csv(self, output_file):
        """Export all leads to a CSV file"""
        try:
            self.cursor.execute('''
            SELECT c.*, ls.status, ls.score
            FROM companies c
            LEFT JOIN lead_status ls ON c.id = ls.company_id
            ''')
            
            rows = self.cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in self.cursor.description]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(column_names)
                writer.writerows(rows)
            
            print(f"Exported {len(rows)} leads to {output_file}")
            return len(rows)
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return 0
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

def main():
    """Main function to initialize and test the database"""
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Initialize database
    db = LeadDatabase()
    if not db.connect():
        return
    
    # Create tables
    db.create_tables()
    
    # Import test data if available
    data_dir = '/home/ubuntu/lead_generation/data'
    if os.path.exists(data_dir):
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        
        for csv_file in csv_files:
            db.import_from_csv(os.path.join(data_dir, csv_file))
        
        for json_file in json_files:
            db.import_from_json(os.path.join(data_dir, json_file))
    
    # Print some stats
    print(f"Total leads in database: {db.get_lead_count()}")
    
    print("\nLeads by industry:")
    for industry, count in db.get_leads_by_industry():
        print(f"  {industry}: {count}")
    
    print("\nLeads by status:")
    for status, count in db.get_leads_by_status():
        print(f"  {status}: {count}")
    
    # Close connection
    db.close()

if __name__ == "__main__":
    print("Initializing lead database...")
    main()
    print("Database initialization complete.")
