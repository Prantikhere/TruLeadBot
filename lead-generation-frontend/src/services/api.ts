import axios, { AxiosResponse } from 'axios';
import { 
  ApiResponse, 
  Lead, 
  Contact, 
  Interaction, 
  EmailCampaign, 
  EmailTemplate,
  LinkedInCampaign,
  LinkedInTemplate,
  ScrapingJob,
  ScrapingConfig,
  LeadStats,
  CampaignStats,
  AutomationConfig,
  LeadFormData,
  ContactFormData
} from '../types';

// Configure axios defaults
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens if needed
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Generic API call wrapper
async function apiCall<T>(
  method: 'GET' | 'POST' | 'PUT' | 'DELETE',
  endpoint: string,
  data?: any,
  params?: any
): Promise<ApiResponse<T>> {
  try {
    const response = await api.request({
      method,
      url: endpoint,
      data,
      params,
    });
    
    return {
      success: true,
      data: response.data,
    };
  } catch (error: any) {
    console.error(`API Error (${method} ${endpoint}):`, error);
    
    return {
      success: false,
      error: error.response?.data?.message || error.message || 'An error occurred',
    };
  }
}

// Lead Management API
export const leadApi = {
  // Get all leads with filtering and pagination
  getLeads: async (params?: {
    page?: number;
    limit?: number;
    status?: string;
    industry?: string;
    search?: string;
    sort?: string;
    order?: 'asc' | 'desc';
  }) => {
    return apiCall<{ leads: Lead[]; pagination: any }>('GET', '/leads', undefined, params);
  },

  // Get a single lead by ID
  getLead: async (id: number) => {
    return apiCall<Lead>('GET', `/leads/${id}`);
  },

  // Create a new lead
  createLead: async (leadData: LeadFormData) => {
    return apiCall<Lead>('POST', '/leads', leadData);
  },

  // Update a lead
  updateLead: async (id: number, leadData: Partial<LeadFormData>) => {
    return apiCall<Lead>('PUT', `/leads/${id}`, leadData);
  },

  // Delete a lead
  deleteLead: async (id: number) => {
    return apiCall<void>('DELETE', `/leads/${id}`);
  },

  // Update lead status
  updateLeadStatus: async (id: number, status: string, nextAction?: string, nextActionDate?: string) => {
    return apiCall<Lead>('PUT', `/leads/${id}/status`, {
      status,
      next_action: nextAction,
      next_action_date: nextActionDate,
    });
  },

  // Add tags to a lead
  addLeadTags: async (id: number, tags: string[]) => {
    return apiCall<void>('POST', `/leads/${id}/tags`, { tags });
  },

  // Remove tags from a lead
  removeLeadTags: async (id: number, tags: string[]) => {
    return apiCall<void>('DELETE', `/leads/${id}/tags`, { tags });
  },

  // Export leads to CSV
  exportLeads: async (params?: { status?: string; industry?: string }) => {
    return apiCall<{ download_url: string }>('POST', '/leads/export', params);
  },

  // Import leads from CSV
  importLeads: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await api.post('/leads/import', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || error.message,
      };
    }
  },
};

// Contact Management API
export const contactApi = {
  // Get contacts for a lead
  getContacts: async (leadId: number) => {
    return apiCall<Contact[]>('GET', `/leads/${leadId}/contacts`);
  },

  // Create a new contact
  createContact: async (leadId: number, contactData: ContactFormData) => {
    return apiCall<Contact>('POST', `/leads/${leadId}/contacts`, contactData);
  },

  // Update a contact
  updateContact: async (contactId: number, contactData: Partial<ContactFormData>) => {
    return apiCall<Contact>('PUT', `/contacts/${contactId}`, contactData);
  },

  // Delete a contact
  deleteContact: async (contactId: number) => {
    return apiCall<void>('DELETE', `/contacts/${contactId}`);
  },
};

// Interaction Management API
export const interactionApi = {
  // Get interactions for a lead
  getInteractions: async (leadId: number) => {
    return apiCall<Interaction[]>('GET', `/leads/${leadId}/interactions`);
  },

  // Create a new interaction
  createInteraction: async (leadId: number, interactionData: {
    contact_id?: number;
    interaction_type: string;
    channel: string;
    notes?: string;
  }) => {
    return apiCall<Interaction>('POST', `/leads/${leadId}/interactions`, interactionData);
  },

  // Update an interaction
  updateInteraction: async (interactionId: number, interactionData: Partial<{
    interaction_type: string;
    channel: string;
    notes: string;
  }>) => {
    return apiCall<Interaction>('PUT', `/interactions/${interactionId}`, interactionData);
  },

  // Delete an interaction
  deleteInteraction: async (interactionId: number) => {
    return apiCall<void>('DELETE', `/interactions/${interactionId}`);
  },
};

// Web Scraping API
export const scrapingApi = {
  // Start a new scraping job
  startScraping: async (config: ScrapingConfig) => {
    return apiCall<ScrapingJob>('POST', '/scraping/start', config);
  },

  // Get scraping job status
  getScrapingStatus: async (jobId: string) => {
    return apiCall<ScrapingJob>('GET', `/scraping/status/${jobId}`);
  },

  // Get scraping history
  getScrapingHistory: async () => {
    return apiCall<ScrapingJob[]>('GET', '/scraping/history');
  },

  // Cancel a scraping job
  cancelScraping: async (jobId: string) => {
    return apiCall<void>('POST', `/scraping/cancel/${jobId}`);
  },
};

// Email Campaign API
export const emailApi = {
  // Get all email campaigns
  getCampaigns: async () => {
    return apiCall<EmailCampaign[]>('GET', '/email/campaigns');
  },

  // Get a single campaign
  getCampaign: async (id: number) => {
    return apiCall<EmailCampaign>('GET', `/email/campaigns/${id}`);
  },

  // Create a new campaign
  createCampaign: async (campaignData: {
    name: string;
    description?: string;
    status?: string;
  }) => {
    return apiCall<EmailCampaign>('POST', '/email/campaigns', campaignData);
  },

  // Update a campaign
  updateCampaign: async (id: number, campaignData: Partial<{
    name: string;
    description: string;
    status: string;
  }>) => {
    return apiCall<EmailCampaign>('PUT', `/email/campaigns/${id}`, campaignData);
  },

  // Delete a campaign
  deleteCampaign: async (id: number) => {
    return apiCall<void>('DELETE', `/email/campaigns/${id}`);
  },

  // Get templates for a campaign
  getTemplates: async (campaignId: number) => {
    return apiCall<EmailTemplate[]>('GET', `/email/campaigns/${campaignId}/templates`);
  },

  // Create a new template
  createTemplate: async (campaignId: number, templateData: {
    template_type: string;
    subject: string;
    body: string;
  }) => {
    return apiCall<EmailTemplate>('POST', `/email/campaigns/${campaignId}/templates`, templateData);
  },

  // Update a template
  updateTemplate: async (templateId: number, templateData: Partial<{
    template_type: string;
    subject: string;
    body: string;
  }>) => {
    return apiCall<EmailTemplate>('PUT', `/email/templates/${templateId}`, templateData);
  },

  // Delete a template
  deleteTemplate: async (templateId: number) => {
    return apiCall<void>('DELETE', `/email/templates/${templateId}`);
  },

  // Generate personalized templates
  generateTemplates: async (industry: string, templateType: string, leadData: any) => {
    return apiCall<{ subject: string; body: string }>('POST', '/email/generate-template', {
      industry,
      template_type: templateType,
      lead_data: leadData,
    });
  },

  // Send test email
  sendTestEmail: async (templateId: number, testEmail: string) => {
    return apiCall<void>('POST', `/email/templates/${templateId}/test`, {
      test_email: testEmail,
    });
  },
};

// LinkedIn Campaign API
export const linkedinApi = {
  // Get all LinkedIn campaigns
  getCampaigns: async () => {
    return apiCall<LinkedInCampaign[]>('GET', '/linkedin/campaigns');
  },

  // Get a single campaign
  getCampaign: async (id: number) => {
    return apiCall<LinkedInCampaign>('GET', `/linkedin/campaigns/${id}`);
  },

  // Create a new campaign
  createCampaign: async (campaignData: {
    name: string;
    description?: string;
    status?: string;
  }) => {
    return apiCall<LinkedInCampaign>('POST', '/linkedin/campaigns', campaignData);
  },

  // Update a campaign
  updateCampaign: async (id: number, campaignData: Partial<{
    name: string;
    description: string;
    status: string;
  }>) => {
    return apiCall<LinkedInCampaign>('PUT', `/linkedin/campaigns/${id}`, campaignData);
  },

  // Delete a campaign
  deleteCampaign: async (id: number) => {
    return apiCall<void>('DELETE', `/linkedin/campaigns/${id}`);
  },

  // Get templates for a campaign
  getTemplates: async (campaignId: number) => {
    return apiCall<LinkedInTemplate[]>('GET', `/linkedin/campaigns/${campaignId}/templates`);
  },

  // Create a new template
  createTemplate: async (campaignId: number, templateData: {
    template_type: string;
    message: string;
  }) => {
    return apiCall<LinkedInTemplate>('POST', `/linkedin/campaigns/${campaignId}/templates`, templateData);
  },

  // Update a template
  updateTemplate: async (templateId: number, templateData: Partial<{
    template_type: string;
    message: string;
  }>) => {
    return apiCall<LinkedInTemplate>('PUT', `/linkedin/templates/${templateId}`, templateData);
  },

  // Delete a template
  deleteTemplate: async (templateId: number) => {
    return apiCall<void>('DELETE', `/linkedin/templates/${templateId}`);
  },

  // Start profile finder
  startProfileFinder: async (config: { limit: number; industry?: string }) => {
    return apiCall<{ job_id: string }>('POST', '/linkedin/profile-finder/start', config);
  },

  // Start LinkedIn automation
  startAutomation: async (config: {
    industries: string[];
    actions: string[];
    limits: { [key: string]: number };
  }) => {
    return apiCall<{ job_id: string }>('POST', '/linkedin/automation/start', config);
  },
};

// Analytics API
export const analyticsApi = {
  // Get lead statistics
  getLeadStats: async (dateRange?: { start: string; end: string }) => {
    return apiCall<LeadStats>('GET', '/analytics/leads', undefined, dateRange);
  },

  // Get campaign statistics
  getCampaignStats: async (dateRange?: { start: string; end: string }) => {
    return apiCall<CampaignStats>('GET', '/analytics/campaigns', undefined, dateRange);
  },

  // Get conversion funnel data
  getConversionFunnel: async (dateRange?: { start: string; end: string }) => {
    return apiCall<any>('GET', '/analytics/funnel', undefined, dateRange);
  },

  // Get performance trends
  getPerformanceTrends: async (metric: string, period: string) => {
    return apiCall<any>('GET', '/analytics/trends', undefined, { metric, period });
  },
};

// Configuration API
export const configApi = {
  // Get current configuration
  getConfig: async () => {
    return apiCall<AutomationConfig>('GET', '/config');
  },

  // Update configuration
  updateConfig: async (config: Partial<AutomationConfig>) => {
    return apiCall<AutomationConfig>('PUT', '/config', config);
  },

  // Reset configuration to defaults
  resetConfig: async () => {
    return apiCall<AutomationConfig>('POST', '/config/reset');
  },
};

// Automation API
export const automationApi = {
  // Run full automation
  runFullAutomation: async () => {
    return apiCall<{ job_id: string }>('POST', '/automation/run');
  },

  // Run specific component
  runComponent: async (component: string, config?: any) => {
    return apiCall<{ job_id: string }>('POST', `/automation/run/${component}`, config);
  },

  // Get automation status
  getAutomationStatus: async (jobId: string) => {
    return apiCall<any>('GET', `/automation/status/${jobId}`);
  },

  // Get automation history
  getAutomationHistory: async () => {
    return apiCall<any[]>('GET', '/automation/history');
  },

  // Cancel automation job
  cancelAutomation: async (jobId: string) => {
    return apiCall<void>('POST', `/automation/cancel/${jobId}`);
  },
};

// System API
export const systemApi = {
  // Get system health
  getHealth: async () => {
    return apiCall<{ status: string; components: any }>('GET', '/system/health');
  },

  // Get system logs
  getLogs: async (level?: string, limit?: number) => {
    return apiCall<any[]>('GET', '/system/logs', undefined, { level, limit });
  },

  // Backup database
  backupDatabase: async () => {
    return apiCall<{ backup_file: string }>('POST', '/system/backup');
  },

  // Get system stats
  getSystemStats: async () => {
    return apiCall<any>('GET', '/system/stats');
  },
};

export default api;