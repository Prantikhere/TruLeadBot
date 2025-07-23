#!/usr/bin/env python3
"""
Lead Generation Web Scraper for AI Chatbot Startup
This script scrapes business directories and websites to collect lead information
for digital marketing agencies, SaaS companies, enterprise IT solutions, SMEs, and service businesses.
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import random
import os
from datetime import datetime
import re
from urllib.parse import urlparse

# Create a directory for storing the scraped data
os.makedirs('/home/ubuntu/lead_generation/data', exist_ok=True)

# User agent list to rotate and avoid being blocked
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

# Target industries and their corresponding directories
TARGET_INDUSTRIES = {
    'digital_marketing': [
        'https://clutch.co/agencies/digital-marketing',
        'https://www.sortlist.com/marketing-agencies',
        'https://www.designrush.com/agency/digital-marketing'
    ],
    'saas_companies': [
        'https://www.g2.com/categories/saas-management',
        'https://www.capterra.com/saas-software/',
        'https://www.goodfirms.co/directory/platform/list-of-software-companies'
    ],
    'enterprise_it': [
        'https://clutch.co/it-services',
        'https://www.goodfirms.co/directory/services/list-of-it-services-companies',
        'https://www.itfirms.co/top-it-companies/'
    ],
    'smes': [
        'https://www.chamberofcommerce.com/',
        'https://www.manta.com/',
        'https://www.thomasnet.com/'
    ],
    'service_businesses': [
        'https://www.yelp.com/c/plumbing',
        'https://www.homeadvisor.com/c.html',
        'https://www.angieslist.com/'
    ]
}

class LeadScraper:
    def __init__(self):
        self.session = requests.Session()
        self.leads = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def get_random_user_agent(self):
        """Return a random user agent from the list"""
        return random.choice(USER_AGENTS)
    
    def make_request(self, url):
        """Make an HTTP request with rotating user agents and error handling"""
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        try:
            # Add random delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_clutch_digital_marketing(self, html):
        """Parse Clutch.co digital marketing agencies page"""
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        companies = []
        
        # Find all company listings
        provider_rows = soup.select('li.provider-row')
        
        for row in provider_rows:
            try:
                company_name = row.select_one('h3.company_info__name a')
                website_elem = row.select_one('a.website-link__item')
                location_elem = row.select_one('span.locality')
                
                company = {
                    'company_name': company_name.text.strip() if company_name else 'N/A',
                    'website': website_elem['href'] if website_elem and website_elem.has_attr('href') else 'N/A',
                    'location': location_elem.text.strip() if location_elem else 'N/A',
                    'industry': 'Digital Marketing Agency',
                    'source': 'clutch.co',
                    'scraped_date': datetime.now().strftime("%Y-%m-%d")
                }
                
                companies.append(company)
            except Exception as e:
                print(f"Error parsing company: {e}")
                continue
        
        return companies
    
    def parse_g2_saas(self, html):
        """Parse G2 SaaS companies page"""
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        companies = []
        
        # Find all product cards
        product_cards = soup.select('div.product-card')
        
        for card in product_cards:
            try:
                company_name_elem = card.select_one('div.product-card__title')
                website_elem = card.select_one('a.product-card__link')
                
                company = {
                    'company_name': company_name_elem.text.strip() if company_name_elem else 'N/A',
                    'website': 'https://www.g2.com' + website_elem['href'] if website_elem and website_elem.has_attr('href') else 'N/A',
                    'industry': 'SaaS Company',
                    'source': 'g2.com',
                    'scraped_date': datetime.now().strftime("%Y-%m-%d")
                }
                
                companies.append(company)
            except Exception as e:
                print(f"Error parsing company: {e}")
                continue
        
        return companies
    
    def parse_yelp_service_businesses(self, html):
        """Parse Yelp service businesses page"""
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        companies = []
        
        # Find all business listings
        business_listings = soup.select('div.businessName__09f24__EYSZE')
        
        for listing in business_listings:
            try:
                name_elem = listing.select_one('a.businessName__09f24__EYSZE span')
                link_elem = listing.select_one('a')
                address_elem = soup.select_one('address')
                
                company = {
                    'company_name': name_elem.text.strip() if name_elem else 'N/A',
                    'website': 'https://www.yelp.com' + link_elem['href'] if link_elem and link_elem.has_attr('href') else 'N/A',
                    'location': address_elem.text.strip() if address_elem else 'N/A',
                    'industry': 'Service Business',
                    'source': 'yelp.com',
                    'scraped_date': datetime.now().strftime("%Y-%m-%d")
                }
                
                companies.append(company)
            except Exception as e:
                print(f"Error parsing company: {e}")
                continue
        
        return companies
    
    def extract_email_from_website(self, website_url):
        """Extract email addresses from a website"""
        if website_url == 'N/A':
            return 'N/A'
        
        try:
            html = self.make_request(website_url)
            if not html:
                return 'N/A'
            
            # Simple regex pattern to find email addresses
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, html)
            
            # Filter out common false positives
            filtered_emails = [email for email in emails if not any(x in email.lower() for x in ['example.com', 'yourdomain', 'domain.com'])]
            
            return filtered_emails[0] if filtered_emails else 'N/A'
        except Exception as e:
            print(f"Error extracting email from {website_url}: {e}")
            return 'N/A'
    
    def detect_chatbot(self, website_url):
        """Detect if a website is using a chatbot"""
        if website_url == 'N/A':
            return 'Unknown'
        
        try:
            html = self.make_request(website_url)
            if not html:
                return 'Unknown'
            
            # Common chatbot indicators in page source
            chatbot_indicators = [
                'intercom', 'drift', 'zendesk', 'livechat', 'tawk', 'crisp', 
                'freshchat', 'hubspot', 'chatbot', 'liveperson', 'olark',
                'tidio', 'userlike', 'livechatinc', 'purechat', 'snapengage',
                'chatra', 'kommunicate', 'botpress', 'dialogflow', 'chatfuel'
            ]
            
            html_lower = html.lower()
            detected_platforms = []
            
            for indicator in chatbot_indicators:
                if indicator in html_lower:
                    detected_platforms.append(indicator)
            
            if detected_platforms:
                return ', '.join(detected_platforms)
            else:
                return 'None detected'
        except Exception as e:
            print(f"Error detecting chatbot on {website_url}: {e}")
            return 'Unknown'
    
    def scrape_industry(self, industry, urls):
        """Scrape leads for a specific industry"""
        industry_leads = []
        
        for url in urls:
            print(f"Scraping {url} for {industry}...")
            html = self.make_request(url)
            
            if not html:
                continue
            
            # Select the appropriate parser based on the URL
            if 'clutch.co/agencies/digital-marketing' in url:
                companies = self.parse_clutch_digital_marketing(html)
            elif 'g2.com/categories/saas-management' in url:
                companies = self.parse_g2_saas(html)
            elif 'yelp.com/c/plumbing' in url:
                companies = self.parse_yelp_service_businesses(html)
            else:
                # Generic parser for other sites
                companies = self.generic_parser(html, industry, url)
            
            # Enrich the data with emails and chatbot detection
            for company in companies:
                if company['website'] != 'N/A':
                    company['email'] = self.extract_email_from_website(company['website'])
                    company['current_chatbot'] = self.detect_chatbot(company['website'])
                else:
                    company['email'] = 'N/A'
                    company['current_chatbot'] = 'Unknown'
                
                industry_leads.append(company)
            
            # Save progress after each URL
            self.save_leads_to_csv(industry_leads, f"{industry}_{self.timestamp}.csv")
            
            # Add a longer delay between different sites
            time.sleep(random.uniform(3, 5))
        
        return industry_leads
    
    def generic_parser(self, html, industry, source_url):
        """Generic parser for websites without specific parsers"""
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        companies = []
        
        # Look for common patterns in business listings
        # This is a simplified approach and may need refinement for specific sites
        company_elements = soup.select('div.company, div.business, div.listing, .provider, .vendor, .partner, article')
        
        if not company_elements:
            # Try alternative selectors if the first attempt yields no results
            company_elements = soup.select('h2 a, h3 a, .title a, .name a')
        
        domain = urlparse(source_url).netloc
        
        for element in company_elements[:20]:  # Limit to first 20 to avoid excessive processing
            try:
                # Try to find company name
                name_elem = element.select_one('h2, h3, h4, .name, .title, strong')
                if not name_elem:
                    name_elem = element
                
                # Try to find website link
                link_elem = element.select_one('a[href*="http"], a.website, .website a, .url a')
                
                company = {
                    'company_name': name_elem.text.strip() if name_elem else 'N/A',
                    'website': link_elem['href'] if link_elem and link_elem.has_attr('href') else 'N/A',
                    'industry': industry.replace('_', ' ').title(),
                    'source': domain,
                    'scraped_date': datetime.now().strftime("%Y-%m-%d")
                }
                
                companies.append(company)
            except Exception as e:
                print(f"Error in generic parser: {e}")
                continue
        
        return companies
    
    def save_leads_to_csv(self, leads, filename):
        """Save leads to a CSV file"""
        if not leads:
            print(f"No leads to save for {filename}")
            return
        
        filepath = os.path.join('/home/ubuntu/lead_generation/data', filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = leads[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for lead in leads:
                    writer.writerow(lead)
            
            print(f"Saved {len(leads)} leads to {filepath}")
        except Exception as e:
            print(f"Error saving leads to CSV: {e}")
    
    def save_leads_to_json(self, leads, filename):
        """Save leads to a JSON file"""
        if not leads:
            print(f"No leads to save for {filename}")
            return
        
        filepath = os.path.join('/home/ubuntu/lead_generation/data', filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(leads, jsonfile, indent=4)
            
            print(f"Saved {len(leads)} leads to {filepath}")
        except Exception as e:
            print(f"Error saving leads to JSON: {e}")
    
    def run(self):
        """Run the scraper for all target industries"""
        all_leads = []
        
        for industry, urls in TARGET_INDUSTRIES.items():
            print(f"\n{'='*50}\nScraping {industry} industry\n{'='*50}")
            industry_leads = self.scrape_industry(industry, urls)
            all_leads.extend(industry_leads)
            
            # Save industry-specific leads
            self.save_leads_to_csv(industry_leads, f"{industry}_leads_{self.timestamp}.csv")
            self.save_leads_to_json(industry_leads, f"{industry}_leads_{self.timestamp}.json")
            
            print(f"Completed scraping {len(industry_leads)} leads for {industry}")
        
        # Save all leads combined
        self.save_leads_to_csv(all_leads, f"all_leads_{self.timestamp}.csv")
        self.save_leads_to_json(all_leads, f"all_leads_{self.timestamp}.json")
        
        print(f"\nScraping completed. Total leads collected: {len(all_leads)}")
        return all_leads

if __name__ == "__main__":
    print("Starting lead generation web scraper...")
    scraper = LeadScraper()
    leads = scraper.run()
    print(f"Scraping complete. Collected {len(leads)} leads.")
