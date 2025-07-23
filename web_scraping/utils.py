#!/usr/bin/env python3
"""
Web Scraping Utility Functions for Lead Generation
This script provides helper functions for the main scraper
"""

import re
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urlparse, urljoin

def extract_contact_info(html):
    """
    Extract contact information from HTML content
    Returns a dictionary with extracted contact details
    """
    if not html:
        return {}
    
    contact_info = {
        'emails': [],
        'phones': [],
        'social_links': {
            'linkedin': [],
            'twitter': [],
            'facebook': []
        }
    }
    
    # Extract emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, html)
    
    # Filter out common false positives
    filtered_emails = [
        email for email in emails 
        if not any(x in email.lower() for x in [
            'example.com', 'yourdomain', 'domain.com', 'email@', 
            'user@', 'name@', 'someone@', 'john.doe@'
        ])
    ]
    contact_info['emails'] = list(set(filtered_emails))  # Remove duplicates
    
    # Extract phone numbers
    # This pattern looks for various phone number formats
    phone_pattern = r'(?:\+\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, html)
    contact_info['phones'] = list(set(phones))  # Remove duplicates
    
    # Extract social media links using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # LinkedIn links
    linkedin_links = soup.select('a[href*="linkedin.com"]')
    contact_info['social_links']['linkedin'] = [link['href'] for link in linkedin_links if link.has_attr('href')]
    
    # Twitter links
    twitter_links = soup.select('a[href*="twitter.com"], a[href*="x.com"]')
    contact_info['social_links']['twitter'] = [link['href'] for link in twitter_links if link.has_attr('href')]
    
    # Facebook links
    facebook_links = soup.select('a[href*="facebook.com"]')
    contact_info['social_links']['facebook'] = [link['href'] for link in facebook_links if link.has_attr('href')]
    
    return contact_info

def find_contact_page(base_url, html):
    """
    Find the contact page URL from a website's homepage
    """
    if not html or not base_url:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Common patterns for contact page links
    contact_patterns = [
        'contact', 'kontakt', 'contacto', 'get in touch', 'reach us', 
        'talk to us', 'connect', 'about us', 'about'
    ]
    
    # Look for links containing contact-related text
    for link in soup.find_all('a', href=True):
        link_text = link.text.lower().strip()
        link_href = link['href'].lower()
        
        for pattern in contact_patterns:
            if pattern in link_text or pattern in link_href:
                # Convert relative URL to absolute
                full_url = urljoin(base_url, link['href'])
                return full_url
    
    return None

def detect_company_size(html):
    """
    Attempt to detect company size from website content
    Returns an estimated size category
    """
    if not html:
        return "Unknown"
    
    html_lower = html.lower()
    
    # Look for team page
    soup = BeautifulSoup(html, 'html.parser')
    team_links = soup.select('a[href*="team"], a[href*="about"], a[href*="people"]')
    
    team_size_indicators = {
        'small': ['small team', 'small business', 'startup', 'founder', 'co-founder'],
        'medium': ['growing team', 'medium-sized', 'mid-sized'],
        'large': ['large team', 'enterprise', 'corporation', 'global']
    }
    
    # Check for size indicators in the HTML
    for size, indicators in team_size_indicators.items():
        for indicator in indicators:
            if indicator in html_lower:
                return size.capitalize()
    
    # Count team members if possible
    team_member_count = len(soup.select('.team-member, .employee, .staff, .person'))
    if team_member_count > 0:
        if team_member_count < 10:
            return "Small (1-10)"
        elif team_member_count < 50:
            return "Medium (11-50)"
        else:
            return "Large (50+)"
    
    return "Unknown"

def detect_technologies(html):
    """
    Detect technologies used on the website
    Returns a list of detected technologies
    """
    if not html:
        return []
    
    html_lower = html.lower()
    detected_tech = []
    
    # Common web technologies
    technologies = {
        'CMS': {
            'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
            'Drupal': ['drupal', 'sites/all', 'sites/default'],
            'Joomla': ['joomla', 'com_content', 'com_users'],
            'Shopify': ['shopify', 'cdn.shopify.com'],
            'Wix': ['wix.com', 'wixsite.com'],
            'Squarespace': ['squarespace', 'static.squarespace.com']
        },
        'Analytics': {
            'Google Analytics': ['google-analytics.com', 'ga.js', 'analytics.js', 'gtag'],
            'Hotjar': ['hotjar', 'static.hotjar.com'],
            'Mixpanel': ['mixpanel'],
            'Segment': ['segment.com', 'segment.io']
        },
        'Marketing': {
            'HubSpot': ['hubspot', 'js.hs-scripts.com'],
            'Marketo': ['marketo', 'munchkin.js'],
            'Mailchimp': ['mailchimp', 'mc.js', 'list-manage.com'],
            'Intercom': ['intercom', 'widget.intercom.io']
        },
        'Frameworks': {
            'React': ['react', 'reactjs'],
            'Angular': ['angular', 'ng-'],
            'Vue': ['vue', 'vuejs'],
            'Bootstrap': ['bootstrap'],
            'jQuery': ['jquery']
        }
    }
    
    # Check for each technology
    for category, techs in technologies.items():
        for tech_name, indicators in techs.items():
            for indicator in indicators:
                if indicator in html_lower:
                    detected_tech.append(f"{tech_name}")
                    break
    
    return list(set(detected_tech))  # Remove duplicates

def extract_company_info(html):
    """
    Extract general company information from website
    Returns a dictionary with company details
    """
    if not html:
        return {}
    
    company_info = {
        'company_size': detect_company_size(html),
        'technologies': detect_technologies(html),
        'social_presence': False,
        'has_blog': False,
        'industries': []
    }
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check for social media presence
    social_links = soup.select('a[href*="linkedin.com"], a[href*="twitter.com"], a[href*="facebook.com"], a[href*="instagram.com"]')
    company_info['social_presence'] = len(social_links) > 0
    
    # Check for blog
    blog_links = soup.select('a[href*="blog"], a[href*="/news"], a[href*="/articles"]')
    company_info['has_blog'] = len(blog_links) > 0
    
    # Try to identify industries
    industry_keywords = {
        'Technology': ['tech', 'software', 'digital', 'IT', 'information technology'],
        'Healthcare': ['health', 'medical', 'healthcare', 'pharma', 'wellness'],
        'Finance': ['finance', 'banking', 'investment', 'insurance', 'fintech'],
        'Education': ['education', 'learning', 'school', 'university', 'training'],
        'E-commerce': ['ecommerce', 'e-commerce', 'shop', 'store', 'retail'],
        'Manufacturing': ['manufacturing', 'production', 'factory', 'industrial'],
        'Real Estate': ['real estate', 'property', 'housing', 'construction'],
        'Marketing': ['marketing', 'advertising', 'branding', 'PR', 'media']
    }
    
    html_text = soup.get_text().lower()
    
    for industry, keywords in industry_keywords.items():
        for keyword in keywords:
            if keyword.lower() in html_text:
                company_info['industries'].append(industry)
                break
    
    company_info['industries'] = list(set(company_info['industries']))  # Remove duplicates
    
    return company_info

def safe_request(url, headers=None, max_retries=3, backoff_factor=0.5):
    """
    Make a safe HTTP request with retries and backoff
    """
    if not headers:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    for attempt in range(max_retries):
        try:
            # Add jitter to avoid detection
            time.sleep(random.uniform(1, 3) * (backoff_factor ** attempt))
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt == max_retries - 1:
                print(f"All retries failed for {url}")
                return None
    
    return None

def is_valid_company_website(url):
    """
    Check if a URL is likely to be a valid company website
    """
    if not url or url == 'N/A':
        return False
    
    # Parse the URL
    try:
        parsed = urlparse(url)
        
        # Check for valid scheme
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Check for suspicious domains
        suspicious_domains = [
            'facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com',
            'youtube.com', 'github.com', 'medium.com', 'pinterest.com',
            'example.com', 'test.com', 'localhost'
        ]
        
        if any(domain in parsed.netloc for domain in suspicious_domains):
            return False
        
        # Check for common file extensions
        if parsed.path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip')):
            return False
        
        return True
    except:
        return False

def normalize_company_name(name):
    """
    Normalize company name by removing common suffixes and standardizing format
    """
    if not name or name == 'N/A':
        return name
    
    # Remove common legal suffixes
    suffixes = [
        ' Inc', ' LLC', ' Ltd', ' Limited', ' Corp', ' Corporation',
        ' GmbH', ' Co', ' Company', ' LLP', ' LP', ' Group', ' Holdings',
        ' International', ' Incorporated', ' Pty', ' AG', ' SA', ' SRL', ' BV'
    ]
    
    normalized = name
    for suffix in suffixes:
        pattern = f"{suffix}\.?$|{suffix}\.?,"
        normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
    
    # Remove extra whitespace and punctuation
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    normalized = re.sub(r'[,\.]+$', '', normalized).strip()
    
    return normalized

def extract_meta_description(html):
    """
    Extract meta description from HTML
    """
    if not html:
        return ""
    
    soup = BeautifulSoup(html, 'html.parser')
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    
    if meta_desc and meta_desc.has_attr('content'):
        return meta_desc['content']
    
    return ""

def extract_company_description(html):
    """
    Extract a company description from the website
    """
    if not html:
        return ""
    
    # First try meta description
    meta_desc = extract_meta_description(html)
    if meta_desc and len(meta_desc) > 50:
        return meta_desc
    
    # Then try to find about section
    soup = BeautifulSoup(html, 'html.parser')
    
    # Look for common about section selectors
    about_selectors = [
        '#about', '.about', 'section.about', 'div.about-us',
        'section.about-us', '#about-us', '.about-us', 
        'section[id*="about"]', 'div[id*="about"]'
    ]
    
    for selector in about_selectors:
        about_section = soup.select_one(selector)
        if about_section:
            # Get text and clean it
            text = about_section.get_text(separator=' ', strip=True)
            # Limit to a reasonable length
            if len(text) > 30:
                return text[:500] + ('...' if len(text) > 500 else '')
    
    # If no about section found, try to get the first paragraph
    paragraphs = soup.select('p')
    for p in paragraphs:
        text = p.get_text(strip=True)
        if len(text) > 100:
            return text[:500] + ('...' if len(text) > 500 else '')
    
    return ""
