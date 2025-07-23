#!/usr/bin/env python3
"""
Email Template Generator for AI Chatbot Startup Lead Generation
This script generates personalized email templates for different industries and stages
"""

import os
import sys
import json
import csv
from datetime import datetime
import argparse
import random

# Create necessary directories
os.makedirs('/home/ubuntu/lead_generation/email_templates/output', exist_ok=True)

class EmailTemplateGenerator:
    def __init__(self):
        """Initialize the email template generator"""
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Base templates for different industries and stages
        self.templates = {
            'initial_outreach': {
                'digital_marketing': [
                    {
                        'subject': "AI Chatbots for {company} - Boost Lead Generation 24/7",
                        'body': """Hello {first_name},

I hope this email finds you well. I came across {company} while researching leading digital marketing agencies and was impressed with your work in {industry_specific}.

I'm reaching out because our AI chatbot solution is helping marketing agencies like yours generate and qualify leads 24/7, even when your team is offline. On average, our clients see a 30% increase in qualified leads without adding staff.

Would you be interested in a quick 15-minute call to see if our solution could help {company} boost lead generation and improve client engagement?

Some quick benefits our marketing agency clients are seeing:
• 24/7 lead capture and qualification
• Automated follow-up with prospects
• Integration with your existing CRM and marketing tools
• Detailed analytics on visitor behavior

I'd be happy to share some case studies from other marketing agencies we've worked with.

Looking forward to your response,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    },
                    {
                        'subject': "Helping {company} Automate Lead Qualification",
                        'body': """Hi {first_name},

I noticed {company}'s impressive work in the digital marketing space, particularly your focus on {industry_specific}.

I'm reaching out because we've developed an AI chatbot specifically designed to help marketing agencies automate lead qualification and nurturing, reducing response times from hours to seconds and increasing conversion rates by 25% on average.

Many marketing agencies struggle with:
• Responding quickly to new leads outside business hours
• Qualifying leads efficiently without tying up staff
• Maintaining consistent follow-up
• Scaling lead generation without increasing headcount

Our solution addresses these challenges by providing 24/7 automated lead capture and qualification that integrates with your existing tools.

Would you be open to a brief conversation to explore how this might benefit {company}?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'saas_companies': [
                    {
                        'subject': "Reducing Customer Support Costs at {company} with AI",
                        'body': """Hello {first_name},

I hope this email finds you well. I've been following {company}'s growth in the SaaS space and was particularly impressed with your {industry_specific} solution.

I'm reaching out because our AI chatbot technology is helping SaaS companies like yours reduce churn by providing instant, 24/7 customer support. On average, our clients see a 15% reduction in churn within the first 3 months and a 40% decrease in support tickets.

Would you be interested in a quick 15-minute call to see if our solution could help {company} improve customer satisfaction while reducing support costs?

Some quick benefits our SaaS clients are seeing:
• 24/7 automated customer support
• Faster resolution of common issues
• Reduced burden on support teams
• Detailed analytics on customer pain points

I'd be happy to share some case studies from other SaaS companies we've worked with.

Looking forward to your response,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    },
                    {
                        'subject': "Improving User Onboarding at {company} with AI",
                        'body': """Hi {first_name},

I've been exploring {company}'s platform and am impressed with your innovation in the {industry_specific} space.

I'm reaching out because we've developed an AI chatbot specifically designed to help SaaS companies automate onboarding and technical support, reducing time-to-value for new users and decreasing support tickets by up to 40%.

Many SaaS companies struggle with:
• Providing immediate support to new users
• Scaling customer support without increasing headcount
• Reducing churn caused by unresolved issues
• Identifying common user pain points

Our solution addresses these challenges by providing contextual help exactly when users need it, increasing feature adoption and user satisfaction.

Would you be open to a brief conversation to explore how this might benefit {company}?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'enterprise_it': [
                    {
                        'subject': "Reducing IT Support Tickets at {company} with AI",
                        'body': """Hello {first_name},

I hope this email finds you well. I came across {company} while researching leading enterprises and was impressed with your IT infrastructure.

I'm reaching out because our AI chatbot solution is helping IT departments like yours reduce ticket volume by automating responses to common questions and issues. On average, our clients see a 40% reduction in level 1 support tickets.

Would you be interested in a quick 15-minute call to see if our solution could help {company} improve IT support efficiency?

Some quick benefits our enterprise clients are seeing:
• 24/7 automated IT support for common issues
• Password reset automation
• Reduced burden on IT support staff
• Detailed analytics on common support requests

I'd be happy to share some case studies from other enterprises we've worked with.

Looking forward to your response,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    },
                    {
                        'subject': "Scaling IT Support at {company} Without Adding Headcount",
                        'body': """Hi {first_name},

I noticed {company}'s impressive growth and wanted to reach out about a solution that's helping enterprises scale their IT support without increasing headcount.

Our AI chatbot technology is helping IT departments provide 24/7 automated assistance for password resets, access requests, and common troubleshooting, integrating seamlessly with existing IT service management tools.

Many enterprise IT departments struggle with:
• High volume of repetitive support requests
• Providing support outside business hours
• Maintaining consistent response times during peak periods
• Documenting solutions for common problems

Our solution addresses these challenges while capturing all interactions in your system of record.

Would you be open to a brief conversation to explore how this might benefit {company}'s IT operations?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'smes': [
                    {
                        'subject': "24/7 Customer Service for {company} - Affordable AI Solution",
                        'body': """Hello {first_name},

I hope this email finds you well. I came across {company} and was impressed with your business, particularly your focus on {industry_specific}.

I'm reaching out because our affordable AI chatbot solution is helping small businesses like yours provide 24/7 customer service without hiring additional staff. Starting at just $49/month with no setup fees, it's designed specifically for SMEs.

Would you be interested in a quick 15-minute call to see if our solution could help {company} improve customer service while keeping costs down?

Some quick benefits our SME clients are seeing:
• 24/7 customer service automation
• Instant responses to common questions
• Lead capture outside business hours
• No technical expertise required to set up

I'd be happy to show you a quick demo of how it would work for your business.

Looking forward to your response,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    },
                    {
                        'subject': "Helping {company} Compete with Larger Businesses",
                        'body': """Hi {first_name},

I noticed {company} while researching successful small businesses in the {industry_specific} space.

I'm reaching out because we've developed an AI chatbot specifically designed to help SMEs compete with larger companies by providing enterprise-level customer service automation at a price point designed for small businesses.

Many small businesses struggle with:
• Responding to customer inquiries outside business hours
• Handling high volumes of similar questions
• Capturing leads when no one is available
• Competing with larger companies' 24/7 availability

Our solution addresses these challenges with easy setup and no technical expertise required. Most clients are up and running in less than a day.

Would you be open to a brief conversation to explore how this might benefit {company}?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'service_businesses': [
                    {
                        'subject': "Automating Appointment Booking for {company}",
                        'body': """Hello {first_name},

I hope this email finds you well. I came across {company} while researching service businesses and was impressed with your {industry_specific} services.

I'm reaching out because our AI chatbot solution is helping service businesses like yours book appointments and answer FAQs 24/7, even when you're with clients or after hours. On average, our clients see a 25% reduction in no-shows.

Would you be interested in a quick 15-minute call to see if our solution could help {company} streamline appointment booking and customer service?

Some quick benefits our service business clients are seeing:
• 24/7 automated appointment booking
• Instant responses to common questions
• Reduced phone interruptions during service delivery
• Automated appointment reminders

I'd be happy to show you a quick demo of how it would work for your business.

Looking forward to your response,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    },
                    {
                        'subject': "Helping {company} Handle Customer Inquiries 24/7",
                        'body': """Hi {first_name},

I noticed {company}'s excellent reputation in providing {industry_specific} services.

I'm reaching out because we've developed an AI chatbot specifically designed to help service providers like you handle customer inquiries automatically, freeing you to focus on delivering your services rather than answering the same questions repeatedly.

Many service businesses struggle with:
• Missing potential clients who contact after hours
• Interruptions from phone calls during service delivery
• Repetitive questions about pricing, hours, and availability
• Managing appointment scheduling efficiently

Our AI solution integrates with your existing calendar and booking systems to provide seamless appointment scheduling and reminders, reducing administrative work by up to 30%.

Would you be open to a brief conversation to explore how this might benefit {company}?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ]
            },
            'follow_up': {
                'digital_marketing': [
                    {
                        'subject': "Following up: AI Chatbots for {company}",
                        'body': """Hello {first_name},

I wanted to follow up on my previous email about how our AI chatbot solution is helping marketing agencies like {company} generate and qualify leads 24/7.

I understand you're busy, so I thought I'd share a quick case study:

One of our marketing agency clients implemented our AI chatbot and saw a 35% increase in qualified leads within the first month. The chatbot now handles initial qualification for all website visitors, allowing their team to focus only on the most promising opportunities.

Would you be interested in a quick 15-minute call this week to discuss how we might be able to achieve similar results for {company}?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    },
                    {
                        'subject': "Quick question about lead generation at {company}",
                        'body': """Hi {first_name},

I reached out last week about our AI chatbot solution for marketing agencies.

I'm curious - what methods is {company} currently using to qualify leads that come through your website? Many agencies we work with were initially skeptical about automation but now find it indispensable for scaling their lead generation.

I'd be happy to share some specific examples of how other marketing agencies in the {industry_specific} space are using our solution to:

• Qualify leads based on budget, timeline, and project scope
• Route qualified leads to the appropriate team members
• Nurture leads that aren't ready to buy
• Gather valuable data on prospect needs

Would you have 15 minutes this week for a quick call?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'saas_companies': [
                    {
                        'subject': "Following up: Reducing Support Costs at {company}",
                        'body': """Hello {first_name},

I wanted to follow up on my previous email about how our AI chatbot solution is helping SaaS companies like {company} reduce support costs while improving customer satisfaction.

I understand you're busy, so I thought I'd share a quick case study:

One of our SaaS clients implemented our AI chatbot and saw a 42% reduction in support tickets within the first two months. Their customer satisfaction scores actually increased because users were getting immediate answers instead of waiting for email responses.

Would you be interested in a quick 15-minute call this week to discuss how we might be able to achieve similar results for {company}?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    },
                    {
                        'subject': "Quick question about customer support at {company}",
                        'body': """Hi {first_name},

I reached out last week about our AI chatbot solution for SaaS companies.

I'm curious - how is {company} currently handling customer support inquiries outside business hours? Many SaaS companies we work with were initially concerned about automation but now find it essential for providing 24/7 support.

I'd be happy to share some specific examples of how other SaaS companies in the {industry_specific} space are using our solution to:

• Resolve common technical issues instantly
• Guide users through onboarding steps
• Collect detailed information before escalating to human agents
• Identify and address common user pain points

Would you have 15 minutes this week for a quick call?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'enterprise_it': [
                    {
                        'subject': "Following up: Reducing IT Tickets at {company}",
                        'body': """Hello {first_name},

I wanted to follow up on my previous email about how our AI chatbot solution is helping enterprises like {company} reduce IT support ticket volume.

I understand you're busy, so I thought I'd share a quick case study:

One of our enterprise clients implemented our AI chatbot and saw a 45% reduction in level 1 support tickets within the first quarter. Their IT team was able to focus on more strategic projects instead of handling routine password resets and access requests.

Would you be interested in a quick 15-minute call this week to discuss how we might be able to achieve similar results for {company}?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    },
                    {
                        'subject': "Quick question about IT support at {company}",
                        'body': """Hi {first_name},

I reached out last week about our AI chatbot solution for enterprise IT departments.

I'm curious - what's the biggest challenge {company}'s IT support team is currently facing? Many enterprises we work with were initially concerned about automation but now find it essential for managing support volume.

I'd be happy to share some specific examples of how other enterprises are using our solution to:

• Automate password resets and access requests
• Provide step-by-step troubleshooting for common issues
• Collect detailed information before escalating to IT staff
• Identify and address recurring support requests

Would you have 15 minutes this week for a quick call?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'smes': [
                    {
                        'subject': "Following up: 24/7 Customer Service for {company}",
                        'body': """Hello {first_name},

I wanted to follow up on my previous email about how our affordable AI chatbot solution is helping small businesses like {company} provide 24/7 customer service.

I understand you're busy, so I thought I'd share a quick case study:

One of our small business clients implemented our AI chatbot and started capturing leads outside business hours immediately. They estimate they were previously missing 30% of potential customers who contacted them after hours.

Would you be interested in a quick 15-minute call this week to discuss how we might be able to achieve similar results for {company}?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    },
                    {
                        'subject': "Quick question about customer service at {company}",
                        'body': """Hi {first_name},

I reached out last week about our affordable AI chatbot solution for small businesses.

I'm curious - how is {company} currently handling customer inquiries outside business hours? Many small businesses we work with were initially concerned about the complexity of AI but now find our solution incredibly easy to use.

I'd be happy to share some specific examples of how other small businesses in the {industry_specific} space are using our solution to:

• Answer FAQs 24/7
• Capture lead information when no one is available
• Provide instant responses to common questions
• Schedule callbacks for more complex inquiries

Would you have 15 minutes this week for a quick call?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'service_businesses': [
                    {
                        'subject': "Following up: Automating Appointments for {company}",
                        'body': """Hello {first_name},

I wanted to follow up on my previous email about how our AI chatbot solution is helping service businesses like {company} automate appointment booking and reduce no-shows.

I understand you're busy, so I thought I'd share a quick case study:

One of our service business clients implemented our AI chatbot and saw a 30% reduction in phone interruptions during service delivery and a 25% decrease in no-shows thanks to automated reminders.

Would you be interested in a quick 15-minute call this week to discuss how we might be able to achieve similar results for {company}?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    },
                    {
                        'subject': "Quick question about appointment booking at {company}",
                        'body': """Hi {first_name},

I reached out last week about our AI chatbot solution for service businesses.

I'm curious - how is {company} currently handling appointment scheduling and reminders? Many service providers we work with were initially concerned about automation but now find it essential for reducing no-shows and administrative work.

I'd be happy to share some specific examples of how other service businesses in the {industry_specific} space are using our solution to:

• Allow clients to book appointments 24/7
• Send automated reminders to reduce no-shows
• Answer common questions about services and pricing
• Free up phone lines for more complex inquiries

Would you have 15 minutes this week for a quick call?

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ]
            },
            'final_attempt': {
                'digital_marketing': [
                    {
                        'subject': "Last note re: AI chatbots for marketing agencies",
                        'body': """Hi {first_name},

I've reached out a couple of times about how our AI chatbot solution is helping marketing agencies automate lead generation and qualification.

I don't want to clutter your inbox, so this will be my last email for now. If you're interested in learning how we're helping agencies like {company}:

• Generate and qualify leads 24/7
• Increase conversion rates by 25% on average
• Integrate with existing CRM and marketing tools
• Scale lead generation without adding staff

You can:

1. Reply to this email to schedule a quick call
2. Visit our website at [Your Website] to learn more
3. Try a demo at [Demo Link]

If the timing isn't right, no problem at all. I'm here if you need anything in the future.

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'saas_companies': [
                    {
                        'subject': "Last note re: AI support for SaaS companies",
                        'body': """Hi {first_name},

I've reached out a couple of times about how our AI chatbot solution is helping SaaS companies improve customer support and reduce churn.

I don't want to clutter your inbox, so this will be my last email for now. If you're interested in learning how we're helping SaaS companies like {company}:

• Provide instant, 24/7 customer support
• Reduce support tickets by up to 40%
• Decrease churn by improving response times
• Scale support without adding headcount

You can:

1. Reply to this email to schedule a quick call
2. Visit our website at [Your Website] to learn more
3. Try a demo at [Demo Link]

If the timing isn't right, no problem at all. I'm here if you need anything in the future.

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'enterprise_it': [
                    {
                        'subject': "Last note re: AI for IT support automation",
                        'body': """Hi {first_name},

I've reached out a couple of times about how our AI chatbot solution is helping enterprises reduce IT support ticket volume.

I don't want to clutter your inbox, so this will be my last email for now. If you're interested in learning how we're helping enterprises like {company}:

• Reduce level 1 support tickets by 40%
• Automate password resets and access requests
• Provide 24/7 IT support for common issues
• Free up IT staff for strategic projects

You can:

1. Reply to this email to schedule a quick call
2. Visit our website at [Your Website] to learn more
3. Try a demo at [Demo Link]

If the timing isn't right, no problem at all. I'm here if you need anything in the future.

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'smes': [
                    {
                        'subject': "Last note re: Affordable AI for small businesses",
                        'body': """Hi {first_name},

I've reached out a couple of times about how our affordable AI chatbot solution is helping small businesses provide 24/7 customer service.

I don't want to clutter your inbox, so this will be my last email for now. If you're interested in learning how we're helping small businesses like {company}:

• Provide 24/7 customer service without adding staff
• Capture leads outside business hours
• Answer FAQs instantly
• Compete with larger companies' service levels

You can:

1. Reply to this email to schedule a quick call
2. Visit our website at [Your Website] to learn more
3. Try a demo at [Demo Link]

If the timing isn't right, no problem at all. I'm here if you need anything in the future.

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ],
                'service_businesses': [
                    {
                        'subject': "Last note re: Appointment automation for service businesses",
                        'body': """Hi {first_name},

I've reached out a couple of times about how our AI chatbot solution is helping service businesses automate appointment booking and reduce no-shows.

I don't want to clutter your inbox, so this will be my last email for now. If you're interested in learning how we're helping service businesses like {company}:

• Allow clients to book appointments 24/7
• Reduce no-shows by 25% with automated reminders
• Answer common questions about services and pricing
• Reduce phone interruptions during service delivery

You can:

1. Reply to this email to schedule a quick call
2. Visit our website at [Your Website] to learn more
3. Try a demo at [Demo Link]

If the timing isn't right, no problem at all. I'm here if you need anything in the future.

Best regards,

[Your Name]
[Your Position]
[Your Company]
[Your Phone]
[Your Email]
"""
                    }
                ]
            }
        }
        
        # Industry-specific details to personalize templates
        self.industry_specifics = {
            'digital_marketing': [
                'social media marketing',
                'SEO services',
                'content marketing',
                'PPC advertising',
                'email marketing',
                'conversion rate optimization',
                'marketing automation'
            ],
            'saas_companies': [
                'cloud solutions',
                'business intelligence',
                'project management',
                'customer relationship management',
                'human resources',
                'financial management',
                'collaboration tools'
            ],
            'enterprise_it': [
                'network infrastructure',
                'cybersecurity',
                'cloud migration',
                'data management',
                'enterprise software',
                'IT service management',
                'digital transformation'
            ],
            'smes': [
                'local business',
                'retail operations',
                'customer service',
                'business growth',
                'online presence',
                'customer engagement',
                'operational efficiency'
            ],
            'service_businesses': [
                'professional services',
                'home services',
                'consulting',
                'maintenance',
                'repair services',
                'installation services',
                'client satisfaction'
            ]
        }
    
    def generate_templates(self, output_dir=None):
        """Generate and save all templates"""
        if not output_dir:
            output_dir = '/home/ubuntu/lead_generation/email_templates/output'
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save templates as JSON
        template_file = os.path.join(output_dir, f"email_templates_{self.timestamp}.json")
        
        try:
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=4)
            
            print(f"Saved templates to {template_file}")
        except Exception as e:
            print(f"Error saving templates: {e}")
        
        # Also save as individual HTML files for easy reference
        for stage, industries in self.templates.items():
            stage_dir = os.path.join(output_dir, stage)
            os.makedirs(stage_dir, exist_ok=True)
            
            for industry, templates in industries.items():
                industry_dir = os.path.join(stage_dir, industry)
                os.makedirs(industry_dir, exist_ok=True)
                
                for i, template in enumerate(templates, 1):
                    template_file = os.path.join(industry_dir, f"template_{i}.html")
                    
                    try:
                        with open(template_file, 'w', encoding='utf-8') as f:
                            f.write(f"<!DOCTYPE html>\n<html>\n<head>\n")
                            f.write(f"<title>{stage.replace('_', ' ').title()} - {industry.replace('_', ' ').title()} - Template {i}</title>\n")
                            f.write(f"<style>\nbody {{ font-family: Arial, sans-serif; margin: 20px; }}\n")
                            f.write(f".subject {{ font-weight: bold; margin-bottom: 10px; }}\n")
                            f.write(f".body {{ white-space: pre-wrap; }}\n")
                            f.write(f"</style>\n</head>\n<body>\n")
                            f.write(f"<h1>{stage.replace('_', ' ').title()} - {industry.replace('_', ' ').title()}</h1>\n")
                            f.write(f"<div class='subject'>Subject: {template['subject']}</div>\n")
                            f.write(f"<div class='body'>{template['body']}</div>\n")
                            f.write(f"</body>\n</html>")
                        
                        print(f"Saved {industry} {stage} template {i} to {template_file}")
                    except Exception as e:
                        print(f"Error saving {industry} {stage} template {i}: {e}")
        
        return output_dir
    
    def generate_personalized_template(self, lead, stage, industry):
        """Generate a personalized template for a specific lead"""
        if industry not in self.templates[stage]:
            industry = list(self.templates[stage].keys())[0]  # Use the first industry as fallback
        
        templates = self.templates[stage][industry]
        template = random.choice(templates)  # Randomly select a template
        
        # Format the template with lead information
        first_name = lead.get('first_name', 'there')
        if first_name == 'N/A' or not first_name:
            first_name = 'there'
        
        company = lead.get('company_name', 'your company')
        if company == 'N/A' or not company:
            company = 'your company'
        
        # Select a random industry-specific detail
        industry_specific = random.choice(self.industry_specifics[industry])
        
        personalized_subject = template['subject'].format(
            first_name=first_name,
            company=company,
            industry_specific=industry_specific
        )
        
        personalized_body = template['body'].format(
            first_name=first_name,
            company=company,
            industry_specific=industry_specific
        )
        
        return {
            'subject': personalized_subject,
            'body': personalized_body
        }
    
    def generate_personalized_templates_for_leads(self, leads, output_file=None):
        """Generate personalized templates for a list of leads"""
        if not output_file:
            output_file = f"/home/ubuntu/lead_generation/email_templates/output/personalized_emails_{self.timestamp}.csv"
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'company_name', 'first_name', 'last_name', 'email', 'industry', 
                             'initial_subject', 'initial_body', 'followup_subject', 'followup_body', 
                             'final_subject', 'final_body']
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
                    
                    # Generate personalized templates for each stage
                    initial = self.generate_personalized_template(lead, 'initial_outreach', template_industry)
                    followup = self.generate_personalized_template(lead, 'follow_up', template_industry)
                    final = self.generate_personalized_template(lead, 'final_attempt', template_industry)
                    
                    writer.writerow({
                        'id': lead.get('id', ''),
                        'company_name': lead.get('company_name', ''),
                        'first_name': lead.get('first_name', ''),
                        'last_name': lead.get('last_name', ''),
                        'email': lead.get('email', ''),
                        'industry': industry,
                        'initial_subject': initial['subject'],
                        'initial_body': initial['body'],
                        'followup_subject': followup['subject'],
                        'followup_body': followup['body'],
                        'final_subject': final['subject'],
                        'final_body': final['body']
                    })
            
            print(f"Saved personalized email templates for {len(leads)} leads to {output_file}")
            return output_file
        except Exception as e:
            print(f"Error saving personalized email templates: {e}")
            return None
    
    def generate_html_preview(self, lead, output_dir=None):
        """Generate HTML preview files for a specific lead"""
        if not output_dir:
            output_dir = f"/home/ubuntu/lead_generation/email_templates/output/previews/{lead.get('company_name', 'company').replace(' ', '_')}"
        
        os.makedirs(output_dir, exist_ok=True)
        
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
        
        # Generate personalized templates for each stage
        stages = {
            'initial_outreach': 'Initial Outreach',
            'follow_up': 'Follow Up',
            'final_attempt': 'Final Attempt'
        }
        
        preview_files = []
        
        for stage_key, stage_name in stages.items():
            template = self.generate_personalized_template(lead, stage_key, template_industry)
            
            preview_file = os.path.join(output_dir, f"{stage_key}.html")
            
            try:
                with open(preview_file, 'w', encoding='utf-8') as f:
                    f.write(f"<!DOCTYPE html>\n<html>\n<head>\n")
                    f.write(f"<title>{stage_name} Email for {lead.get('company_name', 'Company')}</title>\n")
                    f.write(f"<style>\nbody {{ font-family: Arial, sans-serif; margin: 20px; }}\n")
                    f.write(f".subject {{ font-weight: bold; margin-bottom: 10px; }}\n")
                    f.write(f".body {{ white-space: pre-wrap; }}\n")
                    f.write(f"</style>\n</head>\n<body>\n")
                    f.write(f"<h1>{stage_name} Email for {lead.get('company_name', 'Company')}</h1>\n")
                    f.write(f"<div class='subject'>Subject: {template['subject']}</div>\n")
                    f.write(f"<div class='body'>{template['body']}</div>\n")
                    f.write(f"</body>\n</html>")
                
                preview_files.append(preview_file)
                print(f"Saved {stage_name} preview for {lead.get('company_name', 'Company')} to {preview_file}")
            except Exception as e:
                print(f"Error saving {stage_name} preview: {e}")
        
        return preview_files

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Email Template Generator')
    
    parser.add_argument('--output-dir', type=str, 
                        default='/home/ubuntu/lead_generation/email_templates/output',
                        help='Output directory for templates')
    
    parser.add_argument('--input', type=str, default=None,
                        help='Input CSV file with leads data for personalized templates')
    
    parser.add_argument('--output-file', type=str, default=None,
                        help='Output CSV file for personalized templates')
    
    parser.add_argument('--preview', action='store_true',
                        help='Generate HTML preview files for leads')
    
    return parser.parse_args()

def main():
    """Main function to run the template generator"""
    print(f"Starting email template generator at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Parse arguments
    args = parse_arguments()
    
    # Initialize the template generator
    generator = EmailTemplateGenerator()
    
    # Generate and save templates
    template_dir = generator.generate_templates(args.output_dir)
    
    # Generate personalized templates if input file is provided
    if args.input and os.path.exists(args.input):
        try:
            with open(args.input, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                leads = list(csv_reader)
            
            personalized_file = generator.generate_personalized_templates_for_leads(leads, args.output_file)
            print(f"Personalized templates saved to: {personalized_file}")
            
            # Generate HTML previews if requested
            if args.preview and leads:
                # Generate previews for the first 5 leads as examples
                for lead in leads[:5]:
                    generator.generate_html_preview(lead)
        except Exception as e:
            print(f"Error generating personalized templates: {e}")
    
    print(f"Email template generator completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Templates saved to: {template_dir}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
