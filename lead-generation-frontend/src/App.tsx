import React, { useState } from 'react';
import Sidebar from './components/ui/Sidebar';
import Header from './components/ui/Header';
import Dashboard from './components/Dashboard';
import LeadDatabase from './components/LeadDatabase';

// Placeholder components for other sections
const WebScraping = () => <div className="p-6">Web Scraping Component</div>;
const LinkedInAutomation = () => <div className="p-6">LinkedIn Automation Component</div>;
const EmailCampaigns = () => <div className="p-6">Email Campaigns Component</div>;
const Contacts = () => <div className="p-6">Contacts Component</div>;
const Interactions = () => <div className="p-6">Interactions Component</div>;
const Reports = () => <div className="p-6">Reports Component</div>;
const Automation = () => <div className="p-6">Automation Component</div>;
const Settings = () => <div className="p-6">Settings Component</div>;

const App: React.FC = () => {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const renderContent = () => {
    switch (activeSection) {
      case 'dashboard':
        return <Dashboard />;
      case 'leads':
        return <LeadDatabase />;
      case 'web-scraping':
        return <WebScraping />;
      case 'linkedin':
        return <LinkedInAutomation />;
      case 'email':
        return <EmailCampaigns />;
      case 'contacts':
        return <Contacts />;
      case 'interactions':
        return <Interactions />;
      case 'reports':
        return <Reports />;
      case 'automation':
        return <Automation />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  const getSectionTitle = () => {
    const titles = {
      dashboard: 'Dashboard',
      leads: 'Lead Database',
      'web-scraping': 'Web Scraping',
      linkedin: 'LinkedIn Automation',
      email: 'Email Campaigns',
      contacts: 'Contacts',
      interactions: 'Interactions',
      reports: 'Reports',
      automation: 'Automation',
      settings: 'Settings',
    };
    return titles[activeSection as keyof typeof titles] || 'Dashboard';
  };

  const getSectionSubtitle = () => {
    const subtitles = {
      dashboard: 'Overview of your lead generation performance',
      leads: 'Manage and track your lead generation pipeline',
      'web-scraping': 'Automate lead collection from business directories',
      linkedin: 'Manage LinkedIn outreach and connection campaigns',
      email: 'Create and manage email outreach campaigns',
      contacts: 'Manage contact information and relationships',
      interactions: 'Track all interactions with leads and prospects',
      reports: 'Analyze performance and generate insights',
      automation: 'Configure and monitor automated workflows',
      settings: 'Configure system settings and preferences',
    };
    return subtitles[activeSection as keyof typeof subtitles];
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar
        activeItem={activeSection}
        onItemSelect={setActiveSection}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header
          title={getSectionTitle()}
          subtitle={getSectionSubtitle()}
          showSearch={activeSection === 'leads' || activeSection === 'contacts'}
          onRefresh={() => window.location.reload()}
        />

        {/* Content */}
        <main className="flex-1 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default App;