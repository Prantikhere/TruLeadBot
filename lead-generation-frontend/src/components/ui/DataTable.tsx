import React, { useState, useMemo } from 'react';
import { 
  ChevronUp, 
  ChevronDown, 
  ChevronLeft, 
  ChevronRight,
  MoreHorizontal,
  Filter,
  Search
} from 'lucide-react';
import { TableColumn, PaginationInfo } from '../../types';
import LoadingSpinner from './LoadingSpinner';

interface DataTableProps<T> {
  data: T[];
  columns: TableColumn<T>[];
  loading?: boolean;
  pagination?: PaginationInfo;
  onPageChange?: (page: number) => void;
  onSort?: (column: keyof T, direction: 'asc' | 'desc') => void;
  onRowClick?: (row: T) => void;
  onRowSelect?: (selectedRows: T[]) => void;
  selectable?: boolean;
  searchable?: boolean;
  filterable?: boolean;
  emptyMessage?: string;
  className?: string;
}

function DataTable<T extends { id: number | string }>({
  data,
  columns,
  loading = false,
  pagination,
  onPageChange,
  onSort,
  onRowClick,
  onRowSelect,
  selectable = false,
  searchable = false,
  filterable = false,
  emptyMessage = 'No data available',
  className = '',
}: DataTableProps<T>) {
  const [sortColumn, setSortColumn] = useState<keyof T | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  const [selectedRows, setSelectedRows] = useState<Set<number | string>>(new Set());
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  // Filter and search data
  const filteredData = useMemo(() => {
    if (!searchQuery) return data;
    
    return data.filter((row) =>
      columns.some((column) => {
        const value = row[column.key];
        return String(value).toLowerCase().includes(searchQuery.toLowerCase());
      })
    );
  }, [data, searchQuery, columns]);

  // Handle sorting
  const handleSort = (column: TableColumn<T>) => {
    if (!column.sortable) return;

    const newDirection = 
      sortColumn === column.key && sortDirection === 'asc' ? 'desc' : 'asc';
    
    setSortColumn(column.key);
    setSortDirection(newDirection);
    
    if (onSort) {
      onSort(column.key, newDirection);
    }
  };

  // Handle row selection
  const handleRowSelect = (rowId: number | string, selected: boolean) => {
    const newSelectedRows = new Set(selectedRows);
    
    if (selected) {
      newSelectedRows.add(rowId);
    } else {
      newSelectedRows.delete(rowId);
    }
    
    setSelectedRows(newSelectedRows);
    
    if (onRowSelect) {
      const selectedData = data.filter(row => newSelectedRows.has(row.id));
      onRowSelect(selectedData);
    }
  };

  // Handle select all
  const handleSelectAll = (selected: boolean) => {
    if (selected) {
      const allIds = new Set(data.map(row => row.id));
      setSelectedRows(allIds);
      if (onRowSelect) {
        onRowSelect(data);
      }
    } else {
      setSelectedRows(new Set());
      if (onRowSelect) {
        onRowSelect([]);
      }
    }
  };

  const isAllSelected = data.length > 0 && selectedRows.size === data.length;
  const isIndeterminate = selectedRows.size > 0 && selectedRows.size < data.length;

  return (
    <div className={`bg-white rounded-lg border border-gray-200 ${className}`}>
      {/* Table header with search and filters */}
      {(searchable || filterable) && (
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between space-x-4">
            {searchable && (
              <div className="flex-1 max-w-md">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <input
                    type="text"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="input pl-10 pr-4 w-full"
                  />
                </div>
              </div>
            )}
            
            {filterable && (
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="btn-outline flex items-center space-x-2"
              >
                <Filter className="w-4 h-4" />
                <span>Filters</span>
              </button>
            )}
          </div>
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              {selectable && (
                <th className="w-12 px-4 py-3">
                  <input
                    type="checkbox"
                    checked={isAllSelected}
                    ref={(input) => {
                      if (input) input.indeterminate = isIndeterminate;
                    }}
                    onChange={(e) => handleSelectAll(e.target.checked)}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                </th>
              )}
              
              {columns.map((column) => (
                <th
                  key={String(column.key)}
                  className={`px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider ${
                    column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''
                  }`}
                  onClick={() => handleSort(column)}
                >
                  <div className="flex items-center space-x-1">
                    <span>{column.label}</span>
                    {column.sortable && (
                      <div className="flex flex-col">
                        <ChevronUp 
                          className={`w-3 h-3 ${
                            sortColumn === column.key && sortDirection === 'asc'
                              ? 'text-primary-600'
                              : 'text-gray-400'
                          }`}
                        />
                        <ChevronDown 
                          className={`w-3 h-3 -mt-1 ${
                            sortColumn === column.key && sortDirection === 'desc'
                              ? 'text-primary-600'
                              : 'text-gray-400'
                          }`}
                        />
                      </div>
                    )}
                  </div>
                </th>
              ))}
              
              <th className="w-12 px-4 py-3"></th>
            </tr>
          </thead>
          
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr>
                <td colSpan={columns.length + (selectable ? 2 : 1)} className="px-4 py-8">
                  <LoadingSpinner text="Loading data..." />
                </td>
              </tr>
            ) : filteredData.length === 0 ? (
              <tr>
                <td colSpan={columns.length + (selectable ? 2 : 1)} className="px-4 py-8 text-center text-gray-500">
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              filteredData.map((row) => (
                <tr
                  key={row.id}
                  className={`hover:bg-gray-50 ${onRowClick ? 'cursor-pointer' : ''}`}
                  onClick={() => onRowClick && onRowClick(row)}
                >
                  {selectable && (
                    <td className="px-4 py-3">
                      <input
                        type="checkbox"
                        checked={selectedRows.has(row.id)}
                        onChange={(e) => handleRowSelect(row.id, e.target.checked)}
                        onClick={(e) => e.stopPropagation()}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                    </td>
                  )}
                  
                  {columns.map((column) => (
                    <td key={String(column.key)} className="px-4 py-3 text-sm text-gray-900">
                      {column.render 
                        ? column.render(row[column.key], row)
                        : String(row[column.key] || '-')
                      }
                    </td>
                  ))}
                  
                  <td className="px-4 py-3">
                    <button className="p-1 text-gray-400 hover:text-gray-600 rounded">
                      <MoreHorizontal className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pagination && (
        <div className="px-4 py-3 border-t border-gray-200 flex items-center justify-between">
          <div className="text-sm text-gray-700">
            Showing {((pagination.page - 1) * pagination.limit) + 1} to{' '}
            {Math.min(pagination.page * pagination.limit, pagination.total)} of{' '}
            {pagination.total} results
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => onPageChange && onPageChange(pagination.page - 1)}
              disabled={pagination.page <= 1}
              className="p-2 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            
            <span className="text-sm text-gray-700">
              Page {pagination.page} of {pagination.totalPages}
            </span>
            
            <button
              onClick={() => onPageChange && onPageChange(pagination.page + 1)}
              disabled={pagination.page >= pagination.totalPages}
              className="p-2 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default DataTable;