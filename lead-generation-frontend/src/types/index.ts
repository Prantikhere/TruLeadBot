// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

// Lead Types
export interface Lead {
  id: number;
  company_name: string;
  website?: string;
  industry?: string;
  company_size?: string;
  current_chatbot?: string;
  description?: string;
  address?: string;
  city?: string;
  state?: string;
  zipcode?: string;
  country?: string;
  source?: string;
  scraped_date?: string;
  created_at?: string;
  updated_at?: string;
  status?: string;
  score?: number;
  next_action?: string;
  next_action_date?: string;
  contacts?: Contact[];
  interactions?: Interaction[];
  tags?: string[];
}

export interface Contact {
  id: number;
  company_id: number;
  first_name?: string;
  last_name?: string;
  position?: string;
  email?: string;
  phone?: string;
  linkedin_url?: string;
  notes?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Interaction {
  id: number;
  company_id: number;
  contact_id?: number;
  interaction_type: string;
  channel: string;
  interaction_date: string;
  notes?: string;
  created_at?: string;
}

// Campaign Types
export interface EmailCampaign {
  id: number;
  name: string;
  description?: string;
  status: 'Draft' | 'Active' | 'Paused' | 'Completed';
  start_date?: string;
  end_date?: string;
  created_at?: string;
  updated_at?: string;
  templates?: EmailTemplate[];
}

export interface EmailTemplate {
  id: number;
  campaign_id: number;
  template_type: 'initial_outreach' | 'follow_up' | 'final_attempt';
  subject: string;
  body: string;
  created_at?: string;
  updated_at?: string;
}

export interface LinkedInCampaign {
  id: number;
  name: string;
  description?: string;
  status: 'Draft' | 'Active' | 'Paused' | 'Completed';
  start_date?: string;
  end_date?: string;
  created_at?: string;
  updated_at?: string;
  templates?: LinkedInTemplate[];
}

export interface LinkedInTemplate {
  id: number;
  campaign_id: number;
  template_type: 'connection_request' | 'follow_up';
  message: string;
  created_at?: string;
  updated_at?: string;
}

// Scraping Types
export interface ScrapingJob {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  industries: string[];
  leads_per_industry: number;
  total_leads: number;
  progress: number;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
}

export interface ScrapingConfig {
  target_industries: string[];
  leads_per_industry: number;
  enrich_data: boolean;
}

// Analytics Types
export interface LeadStats {
  total_leads: number;
  leads_by_status: { status: string; count: number }[];
  leads_by_industry: { industry: string; count: number }[];
  leads_by_source: { source: string; count: number }[];
  recent_activity: Interaction[];
}

export interface CampaignStats {
  email_campaigns: {
    total: number;
    active: number;
    emails_sent: number;
    open_rate: number;
    click_rate: number;
    reply_rate: number;
  };
  linkedin_campaigns: {
    total: number;
    active: number;
    connections_sent: number;
    acceptance_rate: number;
    messages_sent: number;
    reply_rate: number;
  };
}

// Configuration Types
export interface AutomationConfig {
  database: {
    path: string;
  };
  web_scraping: {
    enabled: boolean;
    target_industries: string[];
    leads_per_industry: number;
    enrich_data: boolean;
  };
  linkedin_automation: {
    enabled: boolean;
    connection_limit_per_day: number;
    message_limit_per_day: number;
    profile_finder_enabled: boolean;
    profile_finder_limit: number;
  };
  email_outreach: {
    enabled: boolean;
    emails_per_day: number;
    follow_up_days: number;
    max_follow_ups: number;
  };
  scheduling: {
    web_scraping_frequency: string;
    linkedin_frequency: string;
    email_frequency: string;
    database_backup_frequency: string;
  };
}

// UI Types
export interface NavigationItem {
  id: string;
  label: string;
  icon: string;
  path: string;
  badge?: number;
}

export interface TableColumn<T = any> {
  key: keyof T;
  label: string;
  sortable?: boolean;
  render?: (value: any, row: T) => React.ReactNode;
}

export interface FilterOption {
  label: string;
  value: string;
  count?: number;
}

export interface PaginationInfo {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}

// Form Types
export interface LeadFormData {
  company_name: string;
  website?: string;
  industry?: string;
  company_size?: string;
  current_chatbot?: string;
  description?: string;
  address?: string;
  city?: string;
  state?: string;
  zipcode?: string;
  country?: string;
  contacts?: Partial<Contact>[];
}

export interface ContactFormData {
  first_name?: string;
  last_name?: string;
  position?: string;
  email?: string;
  phone?: string;
  linkedin_url?: string;
  notes?: string;
}

// Notification Types
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  timestamp: Date;
  read: boolean;
  action?: {
    label: string;
    onClick: () => void;
  };
}

// Export constants
export const INDUSTRIES = [
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
] as const;

export const COMPANY_SIZES = [
  'Small (1-10)',
  'Medium (11-50)',
  'Large (51-200)',
  'Enterprise (201+)'
] as const;

export const LEAD_STATUSES = [
  'New',
  'Contacted',
  'Engaged',
  'Qualified',
  'Proposal Sent',
  'Negotiation',
  'Won',
  'Lost',
  'On Hold'
] as const;

export const INTERACTION_TYPES = [
  'Email Sent',
  'Email Received',
  'Phone Call',
  'LinkedIn Message',
  'LinkedIn Connection',
  'Meeting',
  'Demo',
  'Proposal',
  'Follow Up'
] as const;

export const CHANNELS = [
  'Email',
  'Phone',
  'LinkedIn',
  'Website',
  'In Person',
  'Video Call'
] as const;