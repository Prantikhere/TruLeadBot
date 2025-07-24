import React, { useState } from 'react';
import { 
  Bell, 
  Search, 
  User, 
  Settings, 
  LogOut, 
  Moon, 
  Sun,
  RefreshCw,
  Download
} from 'lucide-react';

interface HeaderProps {
  title: string;
  subtitle?: string;
  onRefresh?: () => void;
  onExport?: () => void;
  showSearch?: boolean;
  onSearch?: (query: string) => void;
}

const Header: React.FC<HeaderProps> = ({
  title,
  subtitle,
  onRefresh,
  onExport,
  showSearch = false,
  onSearch,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(searchQuery);
    }
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    // In a real app, you'd implement dark mode logic here
  };

  const notifications = [
    {
      id: 1,
      title: 'New leads scraped',
      message: '25 new leads added from digital marketing agencies',
      time: '5 minutes ago',
      unread: true,
    },
    {
      id: 2,
      title: 'LinkedIn automation completed',
      message: '15 connection requests sent successfully',
      time: '1 hour ago',
      unread: true,
    },
    {
      id: 3,
      title: 'Email campaign update',
      message: 'Campaign "Q1 Outreach" has 12% open rate',
      time: '2 hours ago',
      unread: false,
    },
  ];

  const unreadCount = notifications.filter(n => n.unread).length;

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Left side - Title and subtitle */}
        <div className="flex-1">
          <h1 className="text-2xl font-semibold text-gray-900">{title}</h1>
          {subtitle && (
            <p className="text-sm text-gray-600 mt-1">{subtitle}</p>
          )}
        </div>

        {/* Center - Search */}
        {showSearch && (
          <div className="flex-1 max-w-md mx-8">
            <form onSubmit={handleSearchSubmit} className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search leads, companies, contacts..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input pl-10 pr-4 w-full"
              />
            </form>
          </div>
        )}

        {/* Right side - Actions and user menu */}
        <div className="flex items-center space-x-4">
          {/* Action buttons */}
          <div className="flex items-center space-x-2">
            {onRefresh && (
              <button
                onClick={onRefresh}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                title="Refresh data"
              >
                <RefreshCw className="w-4 h-4" />
              </button>
            )}
            
            {onExport && (
              <button
                onClick={onExport}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                title="Export data"
              >
                <Download className="w-4 h-4" />
              </button>
            )}

            {/* Dark mode toggle */}
            <button
              onClick={toggleDarkMode}
              className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              title={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDarkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
          </div>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors relative"
              title="Notifications"
            >
              <Bell className="w-4 h-4" />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {unreadCount}
                </span>
              )}
            </button>

            {/* Notifications dropdown */}
            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                <div className="p-4 border-b border-gray-200">
                  <h3 className="font-semibold text-gray-900">Notifications</h3>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  {notifications.map((notification) => (
                    <div
                      key={notification.id}
                      className={`p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer ${
                        notification.unread ? 'bg-blue-50' : ''
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="font-medium text-gray-900 text-sm">
                            {notification.title}
                          </h4>
                          <p className="text-gray-600 text-sm mt-1">
                            {notification.message}
                          </p>
                          <p className="text-gray-400 text-xs mt-2">
                            {notification.time}
                          </p>
                        </div>
                        {notification.unread && (
                          <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
                <div className="p-4 border-t border-gray-200">
                  <button className="text-primary-600 text-sm font-medium hover:text-primary-700">
                    View all notifications
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* User menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-2 p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                <User className="w-4 h-4 text-white" />
              </div>
              <span className="text-sm font-medium text-gray-700">Admin</span>
            </button>

            {/* User dropdown */}
            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                <div className="p-4 border-b border-gray-200">
                  <p className="font-medium text-gray-900">Admin User</p>
                  <p className="text-sm text-gray-600">admin@leadgen.ai</p>
                </div>
                <div className="py-2">
                  <button className="w-full flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    <Settings className="w-4 h-4" />
                    <span>Settings</span>
                  </button>
                  <button className="w-full flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    <LogOut className="w-4 h-4" />
                    <span>Sign out</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;