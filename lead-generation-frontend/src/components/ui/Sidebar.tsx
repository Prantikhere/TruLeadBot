import React from 'react';
import { 
  Database, 
  Globe, 
  Linkedin, 
  Mail, 
  BarChart3, 
  Settings, 
  Users, 
  Activity,
  FileText,
  Zap,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { NavigationItem } from '../../types';

interface SidebarProps {
  activeItem: string;
  onItemSelect: (itemId: string) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

const navigationItems: NavigationItem[] = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: 'BarChart3',
    path: '/dashboard',
  },
  {
    id: 'leads',
    label: 'Lead Database',
    icon: 'Database',
    path: '/leads',
  },
  {
    id: 'web-scraping',
    label: 'Web Scraping',
    icon: 'Globe',
    path: '/web-scraping',
  },
  {
    id: 'linkedin',
    label: 'LinkedIn Automation',
    icon: 'Linkedin',
    path: '/linkedin',
  },
  {
    id: 'email',
    label: 'Email Campaigns',
    icon: 'Mail',
    path: '/email',
  },
  {
    id: 'contacts',
    label: 'Contacts',
    icon: 'Users',
    path: '/contacts',
  },
  {
    id: 'interactions',
    label: 'Interactions',
    icon: 'Activity',
    path: '/interactions',
  },
  {
    id: 'reports',
    label: 'Reports',
    icon: 'FileText',
    path: '/reports',
  },
  {
    id: 'automation',
    label: 'Automation',
    icon: 'Zap',
    path: '/automation',
  },
  {
    id: 'settings',
    label: 'Settings',
    icon: 'Settings',
    path: '/settings',
  },
];

const iconComponents = {
  BarChart3,
  Database,
  Globe,
  Linkedin,
  Mail,
  Users,
  Activity,
  FileText,
  Zap,
  Settings,
};

const Sidebar: React.FC<SidebarProps> = ({
  activeItem,
  onItemSelect,
  collapsed,
  onToggleCollapse,
}) => {
  return (
    <div className={`bg-sidebar-bg text-white transition-all duration-300 ${
      collapsed ? 'w-16' : 'w-64'
    } flex flex-col h-full`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <div className="flex items-center justify-between">
          {!collapsed && (
            <div>
              <h1 className="text-lg font-semibold">Lead Generation</h1>
              <p className="text-sm text-gray-400">AI Automation Suite</p>
            </div>
          )}
          <button
            onClick={onToggleCollapse}
            className="p-2 rounded-lg hover:bg-sidebar-hover transition-colors"
            title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {collapsed ? (
              <ChevronRight className="w-4 h-4" />
            ) : (
              <ChevronLeft className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto scrollbar-thin">
        {navigationItems.map((item) => {
          const IconComponent = iconComponents[item.icon as keyof typeof iconComponents];
          const isActive = activeItem === item.id;

          return (
            <button
              key={item.id}
              onClick={() => onItemSelect(item.id)}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors text-left ${
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-300 hover:bg-sidebar-hover hover:text-white'
              }`}
              title={collapsed ? item.label : undefined}
            >
              <IconComponent className="w-5 h-5 flex-shrink-0" />
              {!collapsed && (
                <>
                  <span className="font-medium">{item.label}</span>
                  {item.badge && (
                    <span className="ml-auto bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
                      {item.badge}
                    </span>
                  )}
                </>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer */}
      {!collapsed && (
        <div className="p-4 border-t border-gray-700">
          <div className="text-xs text-gray-400">
            <p>Version 1.0.0</p>
            <p>© 2024 AI Lead Gen</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;