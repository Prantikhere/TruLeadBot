import React, { useEffect, useState } from 'react';
import { 
  TrendingUp, 
  Users, 
  Mail, 
  Linkedin, 
  Globe,
  Activity,
  AlertCircle,
  CheckCircle,
  Clock,
  Target
} from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { analyticsApi, automationApi } from '../services/api';
import { LeadStats, CampaignStats } from '../types';
import LoadingSpinner from './ui/LoadingSpinner';

interface StatCardProps {
  title: string;
  value: string | number;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
  icon: React.ReactNode;
  color: string;
}

const StatCard: React.FC<StatCardProps> = ({ 
  title, 
  value, 
  change, 
  changeType = 'neutral', 
  icon, 
  color 
}) => {
  const changeColors = {
    positive: 'text-green-600',
    negative: 'text-red-600',
    neutral: 'text-gray-600',
  };

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900 mt-2">{value}</p>
          {change && (
            <p className={`text-sm mt-1 ${changeColors[changeType]}`}>
              {change}
            </p>
          )}
        </div>
        <div className={`p-3 rounded-lg ${color}`}>
          {icon}
        </div>
      </div>
    </div>
  );
};

interface ActivityItemProps {
  type: 'success' | 'warning' | 'error' | 'info';
  title: string;
  description: string;
  time: string;
}

const ActivityItem: React.FC<ActivityItemProps> = ({ type, title, description, time }) => {
  const icons = {
    success: <CheckCircle className="w-4 h-4 text-green-500" />,
    warning: <AlertCircle className="w-4 h-4 text-yellow-500" />,
    error: <AlertCircle className="w-4 h-4 text-red-500" />,
    info: <Activity className="w-4 h-4 text-blue-500" />,
  };

  return (
    <div className="flex items-start space-x-3 p-3 hover:bg-gray-50 rounded-lg">
      <div className="flex-shrink-0 mt-0.5">
        {icons[type]}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900">{title}</p>
        <p className="text-sm text-gray-600">{description}</p>
        <p className="text-xs text-gray-400 mt-1">{time}</p>
      </div>
    </div>
  );
};

const Dashboard: React.FC = () => {
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  
  const { 
    data: leadStats, 
    loading: leadStatsLoading, 
    execute: fetchLeadStats 
  } = useApi<LeadStats>(analyticsApi.getLeadStats);
  
  const { 
    data: campaignStats, 
    loading: campaignStatsLoading, 
    execute: fetchCampaignStats 
  } = useApi<CampaignStats>(analyticsApi.getCampaignStats);

  const { 
    data: automationHistory, 
    loading: automationLoading, 
    execute: fetchAutomationHistory 
  } = useApi(automationApi.getAutomationHistory);

  useEffect(() => {
    fetchLeadStats();
    fetchCampaignStats();
    fetchAutomationHistory();
  }, []);

  const handleRefresh = () => {
    fetchLeadStats();
    fetchCampaignStats();
    fetchAutomationHistory();
  };

  const recentActivities = [
    {
      type: 'success' as const,
      title: 'Web scraping completed',
      description: '25 new leads added from digital marketing agencies',
      time: '5 minutes ago',
    },
    {
      type: 'info' as const,
      title: 'LinkedIn automation started',
      description: 'Sending connection requests to 15 prospects',
      time: '15 minutes ago',
    },
    {
      type: 'success' as const,
      title: 'Email campaign sent',
      description: 'Initial outreach emails sent to 50 leads',
      time: '1 hour ago',
    },
    {
      type: 'warning' as const,
      title: 'Rate limit reached',
      description: 'LinkedIn daily connection limit reached',
      time: '2 hours ago',
    },
  ];

  if (leadStatsLoading || campaignStatsLoading) {
    return (
      <div className="p-6">
        <LoadingSpinner size="lg" text="Loading dashboard..." />
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Leads"
          value={leadStats?.total_leads || 0}
          change="+12% from last week"
          changeType="positive"
          icon={<Users className="w-6 h-6 text-white" />}
          color="bg-blue-500"
        />
        
        <StatCard
          title="Email Campaigns"
          value={campaignStats?.email_campaigns.active || 0}
          change={`${campaignStats?.email_campaigns.emails_sent || 0} emails sent`}
          changeType="neutral"
          icon={<Mail className="w-6 h-6 text-white" />}
          color="bg-green-500"
        />
        
        <StatCard
          title="LinkedIn Connections"
          value={campaignStats?.linkedin_campaigns.connections_sent || 0}
          change={`${Math.round((campaignStats?.linkedin_campaigns.acceptance_rate || 0) * 100)}% acceptance rate`}
          changeType="positive"
          icon={<Linkedin className="w-6 h-6 text-white" />}
          color="bg-blue-600"
        />
        
        <StatCard
          title="Conversion Rate"
          value={`${Math.round((campaignStats?.email_campaigns.reply_rate || 0) * 100)}%`}
          change="+2.5% from last month"
          changeType="positive"
          icon={<TrendingUp className="w-6 h-6 text-white" />}
          color="bg-purple-500"
        />
      </div>

      {/* Charts and Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Lead Sources */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Lead Sources</h3>
          <div className="space-y-4">
            {leadStats?.leads_by_source?.map((source, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Globe className="w-4 h-4 text-gray-400" />
                  <span className="text-sm font-medium text-gray-900">
                    {source.source}
                  </span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-24 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-primary-600 h-2 rounded-full" 
                      style={{ 
                        width: `${(source.count / (leadStats?.total_leads || 1)) * 100}%` 
                      }}
                    ></div>
                  </div>
                  <span className="text-sm text-gray-600 w-8 text-right">
                    {source.count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Lead Status Distribution */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Lead Status</h3>
          <div className="space-y-4">
            {leadStats?.leads_by_status?.map((status, index) => {
              const statusColors = {
                'New': 'bg-blue-500',
                'Contacted': 'bg-yellow-500',
                'Engaged': 'bg-green-500',
                'Qualified': 'bg-purple-500',
                'Won': 'bg-emerald-500',
                'Lost': 'bg-red-500',
              };
              
              const colorClass = statusColors[status.status as keyof typeof statusColors] || 'bg-gray-500';
              
              return (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${colorClass}`}></div>
                    <span className="text-sm font-medium text-gray-900">
                      {status.status}
                    </span>
                  </div>
                  <span className="text-sm text-gray-600">
                    {status.count}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Recent Activity and Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <div className="lg:col-span-2 card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
            <button 
              onClick={handleRefresh}
              className="text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              Refresh
            </button>
          </div>
          <div className="space-y-2">
            {recentActivities.map((activity, index) => (
              <ActivityItem key={index} {...activity} />
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button className="w-full btn-primary flex items-center justify-center space-x-2">
              <Globe className="w-4 h-4" />
              <span>Start Web Scraping</span>
            </button>
            
            <button className="w-full btn-outline flex items-center justify-center space-x-2">
              <Linkedin className="w-4 h-4" />
              <span>LinkedIn Automation</span>
            </button>
            
            <button className="w-full btn-outline flex items-center justify-center space-x-2">
              <Mail className="w-4 h-4" />
              <span>Send Email Campaign</span>
            </button>
            
            <button className="w-full btn-outline flex items-center justify-center space-x-2">
              <Target className="w-4 h-4" />
              <span>Run Full Automation</span>
            </button>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">
              {Math.round((campaignStats?.email_campaigns.open_rate || 0) * 100)}%
            </div>
            <div className="text-sm text-gray-600">Email Open Rate</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {Math.round((campaignStats?.email_campaigns.click_rate || 0) * 100)}%
            </div>
            <div className="text-sm text-gray-600">Email Click Rate</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {Math.round((campaignStats?.linkedin_campaigns.acceptance_rate || 0) * 100)}%
            </div>
            <div className="text-sm text-gray-600">LinkedIn Acceptance Rate</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;