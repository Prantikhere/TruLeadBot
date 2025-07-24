import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Filter, 
  Download, 
  Upload, 
  Edit, 
  Trash2, 
  Eye,
  Tag,
  ExternalLink
} from 'lucide-react';
import { useApi, usePaginatedApi } from '../hooks/useApi';
import { leadApi } from '../services/api';
import { Lead, TableColumn, INDUSTRIES, COMPANY_SIZES, LEAD_STATUSES } from '../types';
import DataTable from './ui/DataTable';
import LoadingSpinner from './ui/LoadingSpinner';

const LeadDatabase: React.FC = () => {
  const [selectedLeads, setSelectedLeads] = useState<Lead[]>([]);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    status: '',
    industry: '',
    company_size: '',
    search: '',
  });

  // Use paginated API hook for leads
  const {
    data: leads,
    loading,
    error,
    pagination,
    updateParams,
    refresh,
  } = usePaginatedApi(leadApi.getLeads, {
    page: 1,
    limit: 25,
    ...filters,
  });

  // Update leads when filters change
  useEffect(() => {
    updateParams(filters);
  }, [filters, updateParams]);

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleSearch = (query: string) => {
    setFilters(prev => ({ ...prev, search: query }));
  };

  const handleExport = async () => {
    try {
      const response = await leadApi.exportLeads(filters);
      if (response.success && response.data?.download_url) {
        window.open(response.data.download_url, '_blank');
      }
    } catch (error) {
      console.error('Export failed:', error);
    }
  };

  const handleImport = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      leadApi.importLeads(file).then((response) => {
        if (response.success) {
          refresh();
        }
      });
    }
  };

  const getStatusBadge = (status: string) => {
    const statusColors = {
      'New': 'badge-info',
      'Contacted': 'badge-warning',
      'Engaged': 'badge-success',
      'Qualified': 'badge-success',
      'Won': 'badge-success',
      'Lost': 'badge-error',
    };
    
    const colorClass = statusColors[status as keyof typeof statusColors] || 'badge-info';
    
    return (
      <span className={`badge ${colorClass}`}>
        {status}
      </span>
    );
  };

  const columns: TableColumn<Lead>[] = [
    {
      key: 'company_name',
      label: 'Company',
      sortable: true,
      render: (value, row) => (
        <div>
          <div className="font-medium text-gray-900">{value}</div>
          {row.website && (
            <a 
              href={row.website} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-sm text-primary-600 hover:text-primary-700 flex items-center space-x-1"
              onClick={(e) => e.stopPropagation()}
            >
              <span>{new URL(row.website).hostname}</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          )}
        </div>
      ),
    },
    {
      key: 'industry',
      label: 'Industry',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-600">{value || '-'}</span>
      ),
    },
    {
      key: 'company_size',
      label: 'Size',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-600">{value || '-'}</span>
      ),
    },
    {
      key: 'status',
      label: 'Status',
      sortable: true,
      render: (value) => getStatusBadge(value || 'New'),
    },
    {
      key: 'current_chatbot',
      label: 'Current Chatbot',
      render: (value) => (
        <span className="text-sm text-gray-600">
          {value === 'None detected' ? (
            <span className="text-green-600">None detected</span>
          ) : (
            value || '-'
          )}
        </span>
      ),
    },
    {
      key: 'city',
      label: 'Location',
      render: (value, row) => (
        <span className="text-sm text-gray-600">
          {[row.city, row.state, row.country].filter(Boolean).join(', ') || '-'}
        </span>
      ),
    },
    {
      key: 'created_at',
      label: 'Added',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-600">
          {value ? new Date(value).toLocaleDateString() : '-'}
        </span>
      ),
    },
  ];

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Error loading leads: {error}</p>
          <button 
            onClick={refresh}
            className="mt-2 btn-primary"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header Actions */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Lead Database</h2>
          <p className="text-sm text-gray-600 mt-1">
            Manage and track your lead generation pipeline
          </p>
        </div>
        
        <div className="flex items-center space-x-3">
          <label className="btn-outline cursor-pointer">
            <Upload className="w-4 h-4 mr-2" />
            Import
            <input
              type="file"
              accept=".csv"
              onChange={handleImport}
              className="hidden"
            />
          </label>
          
          <button 
            onClick={handleExport}
            className="btn-outline"
          >
            <Download className="w-4 h-4 mr-2" />
            Export
          </button>
          
          <button 
            onClick={() => setShowFilters(!showFilters)}
            className="btn-outline"
          >
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </button>
          
          <button className="btn-primary">
            <Plus className="w-4 h-4 mr-2" />
            Add Lead
          </button>
        </div>
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="card p-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={filters.status}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="select w-full"
              >
                <option value="">All Statuses</option>
                {LEAD_STATUSES.map(status => (
                  <option key={status} value={status}>{status}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Industry
              </label>
              <select
                value={filters.industry}
                onChange={(e) => handleFilterChange('industry', e.target.value)}
                className="select w-full"
              >
                <option value="">All Industries</option>
                {INDUSTRIES.map(industry => (
                  <option key={industry} value={industry}>{industry}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Company Size
              </label>
              <select
                value={filters.company_size}
                onChange={(e) => handleFilterChange('company_size', e.target.value)}
                className="select w-full"
              >
                <option value="">All Sizes</option>
                {COMPANY_SIZES.map(size => (
                  <option key={size} value={size}>{size}</option>
                ))}
              </select>
            </div>
            
            <div className="flex items-end">
              <button
                onClick={() => setFilters({ status: '', industry: '', company_size: '', search: '' })}
                className="btn-outline w-full"
              >
                Clear Filters
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Selected Actions */}
      {selectedLeads.length > 0 && (
        <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-primary-800">
              {selectedLeads.length} lead{selectedLeads.length > 1 ? 's' : ''} selected
            </span>
            <div className="flex items-center space-x-2">
              <button className="btn-outline text-sm">
                <Tag className="w-4 h-4 mr-1" />
                Add Tags
              </button>
              <button className="btn-outline text-sm">
                <Edit className="w-4 h-4 mr-1" />
                Bulk Edit
              </button>
              <button className="btn-outline text-sm text-red-600 hover:text-red-700">
                <Trash2 className="w-4 h-4 mr-1" />
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Data Table */}
      <DataTable
        data={leads}
        columns={columns}
        loading={loading}
        pagination={pagination}
        onRowSelect={setSelectedLeads}
        selectable
        searchable
        onSearch={handleSearch}
        emptyMessage="No leads found. Start by importing leads or running web scraping."
      />
    </div>
  );
};

export default LeadDatabase;