#!/usr/bin/env python3
"""
LinkedIn Message Template Generator
This script generates personalized LinkedIn message templates for different industries
"""

import os
import sys
import json
import csv
from datetime import datetime
import argparse

# Create necessary directories
os.makedirs('/home/ubuntu/lead_generation/linkedin_automation/templates', exist_ok=True)

class TemplateGenerator:
    def __init__(self):
        """Initialize the template generator"""
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Base templates for different industries
        self.templates = {
            'connection_request': {
                'digital_marketing': [
                    "Hi {first_name}, I noticed your work in digital marketing and thought we could connect. I'm working with AI chatbot solutions that are helping marketing agencies automate lead generation and improve client engagement.",
                    "Hello {first_name}, I came across your profile while researching digital marketing professionals. I'm working with AI chatbots that are helping agencies like {company} generate qualified leads 24/7. Would love to connect!",
                    "Hi {first_name}, your experience in digital marketing caught my attention. I'm working with AI solutions that are helping agencies automate client communication and lead qualification. Thought we could connect!"
                ],
                'saas_companies': [
                    "Hi {first_name}, I noticed your work at {company} in the SaaS space. I'm working with AI chatbot technology that's helping SaaS companies improve user onboarding and support. Thought we could connect!",
                    "Hello {first_name}, I saw your profile and your experience in SaaS caught my eye. I'm working with AI chatbots that are helping companies reduce churn through better customer support. Would love to connect!",
                    "Hi {first_name}, your role at {company} caught my attention. I'm working with AI solutions that are helping SaaS businesses automate customer interactions and improve retention. Thought we could connect!"
                ],
                'enterprise_it': [
                    "Hi {first_name}, I came across your profile and your IT leadership experience is impressive. I'm working with AI solutions that are helping enterprises automate customer interactions and reduce support costs. Would be great to connect!",
                    "Hello {first_name}, your experience in enterprise IT caught my attention. I'm working with AI chatbots that are helping companies like {company} reduce ticket volume by up to 40%. Would love to connect!",
                    "Hi {first_name}, I noticed your work in IT at {company}. I'm working with AI solutions that are helping enterprises scale their customer support without increasing headcount. Thought we could connect!"
                ],
                'smes': [
                    "Hi {first_name}, I noticed your business and thought we could connect. I'm working with AI chatbot solutions specifically designed for SMEs to improve customer service without increasing headcount.",
                    "Hello {first_name}, I came across {company} and was impressed with what you're doing. I'm working with affordable AI solutions that are helping small businesses provide 24/7 customer service. Would love to connect!",
                    "Hi {first_name}, your business caught my attention. I'm working with AI chatbots that are helping SMEs like yours automate customer interactions and generate more leads. Thought we could connect!"
                ],
                'service_businesses': [
                    "Hi {first_name}, I saw your service business and thought we could connect. I'm working with affordable AI chatbot solutions that are helping businesses like yours handle customer inquiries 24/7.",
                    "Hello {first_name}, I noticed {company} and was impressed with your services. I'm working with AI solutions that are helping service businesses automate appointment booking and answer FAQs. Would love to connect!",
                    "Hi {first_name}, your business caught my eye. I'm working with AI chatbots that are helping service providers like you handle customer inquiries even after business hours. Thought we could connect!"
                ]
            },
            'follow_up': {
                'digital_marketing': [
                    "Hi {first_name}, thanks for connecting! I wanted to share how our AI chatbots are helping marketing agencies generate and qualify leads 24/7. Would you be interested in seeing how it could work for your clients?",
                    "Hello {first_name}, appreciate the connection! I thought you might be interested in how our AI chatbots are helping marketing agencies like yours automate lead qualification and improve response times. Would you have 15 minutes for a quick chat?",
                    "Hi {first_name}, thanks for connecting! I'm curious - are you currently using any automation tools for lead generation at {company}? Our AI chatbots are helping agencies increase qualified leads by 30% on average."
                ],
                'saas_companies': [
                    "Hi {first_name}, thanks for connecting! I wanted to share how our AI chatbots are helping SaaS companies reduce churn by improving customer support. Would you be open to a quick chat about how it might help {company}?",
                    "Hello {first_name}, appreciate the connection! I thought you might be interested in how our AI solutions are helping SaaS businesses like yours automate onboarding and reduce time-to-value. Would you have 15 minutes to discuss?",
                    "Hi {first_name}, thanks for connecting! I'm curious - what tools are you currently using for customer support at {company}? Our AI chatbots are helping SaaS companies reduce support tickets by up to 40%."
                ],
                'enterprise_it': [
                    "Hi {first_name}, thanks for connecting! I wanted to share how our AI solutions are helping IT departments reduce ticket volume by up to 40%. Would you be interested in learning more about how it could work for {company}?",
                    "Hello {first_name}, appreciate the connection! I thought you might be interested in how our AI chatbots are helping enterprises like yours automate routine IT support tasks. Would you have 15 minutes for a quick discussion?",
                    "Hi {first_name}, thanks for connecting! I'm curious - what's your biggest challenge with IT support volume at {company}? Our AI solutions are helping enterprises scale support without increasing headcount."
                ],
                'smes': [
                    "Hi {first_name}, thanks for connecting! I wanted to share how our affordable AI chatbots are helping small businesses provide 24/7 customer service. Would you be open to a quick chat about how it might help your business?",
                    "Hello {first_name}, appreciate the connection! I thought you might be interested in how our AI solutions are helping SMEs like yours automate customer interactions without breaking the bank. Would you have 15 minutes to discuss?",
                    "Hi {first_name}, thanks for connecting! I'm curious - how are you currently handling customer inquiries outside business hours? Our AI chatbots are helping small businesses be available to customers 24/7."
                ],
                'service_businesses': [
                    "Hi {first_name}, thanks for connecting! I wanted to share how service businesses like yours are using our AI chatbots to book appointments and answer FAQs automatically. Would you be interested in seeing a quick demo?",
                    "Hello {first_name}, appreciate the connection! I thought you might be interested in how our AI solutions are helping service providers like you handle customer inquiries even after business hours. Would you have 15 minutes to discuss?",
                    "Hi {first_name}, thanks for connecting! I'm curious - how are you currently handling appointment scheduling at {company}? Our AI chatbots are helping service businesses reduce no-shows by 25% on average."
                ]
            },
            'value_proposition': {
                'digital_marketing': [
                    "Our AI chatbots help marketing agencies qualify leads 24/7, even when your team is offline. On average, our clients see a 30% increase in qualified leads without adding staff.",
                    "We help marketing agencies automate lead qualification and nurturing, reducing response times from hours to seconds and increasing conversion rates by 25% on average.",
                    "Our AI solution integrates with your existing marketing tools to capture, qualify, and nurture leads automatically, freeing your team to focus on strategy and client relationships."
                ],
                'saas_companies': [
                    "Our AI chatbots help SaaS companies reduce churn by providing instant, 24/7 customer support. On average, our clients see a 15% reduction in churn within the first 3 months.",
                    "We help SaaS businesses automate onboarding and technical support, reducing time-to-value for new users and decreasing support tickets by up to 40%.",
                    "Our AI solution integrates with your product to provide contextual help exactly when users need it, increasing feature adoption and user satisfaction."
                ],
                'enterprise_it': [
                    "Our AI chatbots help IT departments reduce ticket volume by automating responses to common questions and issues. On average, our clients see a 40% reduction in level 1 support tickets.",
                    "We help enterprises scale their IT support without increasing headcount, providing 24/7 automated assistance for password resets, access requests, and common troubleshooting.",
                    "Our AI solution integrates with your existing IT service management tools to provide instant support while capturing all interactions in your system of record."
                ],
                'smes': [
                    "Our affordable AI chatbots help small businesses provide 24/7 customer service without hiring additional staff. Starting at just $49/month with no setup fees.",
                    "We help SMEs compete with larger companies by providing enterprise-level customer service automation at a price point designed for small businesses.",
                    "Our AI solution is specifically designed for small businesses, with easy setup and no technical expertise required. Most clients are up and running in less than a day."
                ],
                'service_businesses': [
                    "Our AI chatbots help service businesses book appointments and answer FAQs 24/7, even when you're with clients or after hours. On average, our clients see a 25% reduction in no-shows.",
                    "We help service providers like you handle customer inquiries automatically, freeing you to focus on delivering your services rather than answering the same questions repeatedly.",
                    "Our AI solution integrates with your existing calendar and booking systems to provide seamless appointment scheduling and reminders, reducing administrative work by up to 30%."
                ]
            }
        }
    
    def generate_templates(self, output_dir=None):
        """Generate and save all templates"""
        if not output_dir:
            output_dir = '/home/ubuntu/lead_generation/linkedin_automation/templates'
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save templates as JSON
        template_file = os.path.join(output_dir, f"linkedin_templates_{self.timestamp}.json")
        
        try:
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=4)
            
            print(f"Saved templates to {template_file}")
        except Exception as e:
            print(f"Error saving templates: {e}")
        
        # Also save as individual text files for easy reference
        for message_type, industries in self.templates.items():
            type_dir = os.path.join(output_dir, message_type)
            os.makedirs(type_dir, exist_ok=True)
            
            for industry, templates in industries.items():
                industry_file = os.path.join(type_dir, f"{industry}.txt")
                
                try:
                    with open(industry_file, 'w', encoding='utf-8') as f:
                        f.write(f"# {message_type.replace('_', ' ').title()} Templates for {industry.replace('_', ' ').title()}\n\n")
                        
                        for i, template in enumerate(templates, 1):
                            f.write(f"## Template {i}\n\n")
                            f.write(f"{template}\n\n")
                    
                    print(f"Saved {industry} {message_type} templates to {industry_file}")
                except Exception as e:
                    print(f"Error saving {industry} {message_type} templates: {e}")
        
        return template_file
    
    def generate_personalized_template(self, lead, message_type, industry):
        """Generate a personalized template for a specific lead"""
        if industry not in self.templates[message_type]:
            industry = list(self.templates[message_type].keys())[0]  # Use the first industry as fallback
        
        templates = self.templates[message_type][industry]
        template = templates[0]  # Use the first template by default
        
        # Format the template with lead information
        first_name = lead.get('first_name', 'there')
        if first_name == 'N/A':
            first_name = 'there'
        
        company = lead.get('company_name', 'your company')
        if company == 'N/A':
            company = 'your company'
        
        personalized = template.format(
            first_name=first_name,
            company=company
        )
        
        return personalized
    
    def generate_personalized_templates_for_leads(self, leads, output_file=None):
        """Generate personalized templates for a list of leads"""
        if not output_file:
            output_file = f"/home/ubuntu/lead_generation/linkedin_automation/templates/personalized_templates_{self.timestamp}.csv"
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'company_name', 'first_name', 'last_name', 'industry', 
                             'connection_request', 'follow_up', 'value_proposition']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for lead in leads:
                    industry = lead.get('industry', '').lower()
                    
                    # Map the industry to one of our template categories
                    template_industry = 'smes'  # Default to SMEs
                    
                    if 'market' in industry or 'digital' in industry or 'agency' in industry:
                        template_industry = 'digital_marketing'
                    elif 'saas' in industry or 'software' in industry or 'tech' in industry:
                        template_industry = 'saas_companies'
                    elif 'enterprise' in industry or 'it' in industry or 'information technology' in industry:
                        template_industry = 'enterprise_it'
                    elif 'service' in industry or 'plumb' in industry or 'electric' in industry:
                        template_industry = 'service_businesses'
                    
                    # Generate personalized templates
                    connection_request = self.generate_personalized_template(lead, 'connection_request', template_industry)
                    follow_up = self.generate_personalized_template(lead, 'follow_up', template_industry)
                    value_proposition = self.templates['value_proposition'][template_industry][0]
                    
                    writer.writerow({
                        'id': lead.get('id', ''),
                        'company_name': lead.get('company_name', ''),
                        'first_name': lead.get('first_name', ''),
                        'last_name': lead.get('last_name', ''),
                        'industry': industry,
                        'connection_request': connection_request,
                        'follow_up': follow_up,
                        'value_proposition': value_proposition
                    })
            
            print(f"Saved personalized templates for {len(leads)} leads to {output_file}")
            return output_file
        except Exception as e:
            print(f"Error saving personalized templates: {e}")
            return None

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='LinkedIn Message Template Generator')
    
    parser.add_argument('--output-dir', type=str, 
                        default='/home/ubuntu/lead_generation/linkedin_automation/templates',
                        help='Output directory for templates')
    
    parser.add_argument('--input', type=str, default=None,
                        help='Input CSV file with leads data for personalized templates')
    
    parser.add_argument('--output-file', type=str, default=None,
                        help='Output CSV file for personalized templates')
    
    return parser.parse_args()

def main():
    """Main function to run the template generator"""
    print(f"Starting LinkedIn message template generator at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Parse arguments
    args = parse_arguments()
    
    # Initialize the template generator
    generator = TemplateGenerator()
    
    # Generate and save templates
    template_file = generator.generate_templates(args.output_dir)
    
    # Generate personalized templates if input file is provided
    if args.input and os.path.exists(args.input):
        try:
            with open(args.input, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                leads = list(csv_reader)
            
            personalized_file = generator.generate_personalized_templates_for_leads(leads, args.output_file)
            print(f"Personalized templates saved to: {personalized_file}")
        except Exception as e:
            print(f"Error generating personalized templates: {e}")
    
    print(f"LinkedIn message template generator completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Templates saved to: {template_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
