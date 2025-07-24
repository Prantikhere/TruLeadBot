import { useState, useEffect, useCallback } from 'react';
import { ApiResponse } from '../types';

interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

interface UseApiOptions {
  immediate?: boolean;
  onSuccess?: (data: any) => void;
  onError?: (error: string) => void;
}

export function useApi<T>(
  apiFunction: (...args: any[]) => Promise<ApiResponse<T>>,
  options: UseApiOptions = {}
) {
  const { immediate = false, onSuccess, onError } = options;
  
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(async (...args: any[]) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const response = await apiFunction(...args);
      
      if (response.success) {
        setState({
          data: response.data || null,
          loading: false,
          error: null,
        });
        
        if (onSuccess) {
          onSuccess(response.data);
        }
        
        return response.data;
      } else {
        const errorMessage = response.error || 'An error occurred';
        setState({
          data: null,
          loading: false,
          error: errorMessage,
        });
        
        if (onError) {
          onError(errorMessage);
        }
        
        throw new Error(errorMessage);
      }
    } catch (error: any) {
      const errorMessage = error.message || 'An unexpected error occurred';
      setState({
        data: null,
        loading: false,
        error: errorMessage,
      });
      
      if (onError) {
        onError(errorMessage);
      }
      
      throw error;
    }
  }, [apiFunction, onSuccess, onError]);

  const reset = useCallback(() => {
    setState({
      data: null,
      loading: false,
      error: null,
    });
  }, []);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [immediate, execute]);

  return {
    ...state,
    execute,
    reset,
  };
}

// Hook for paginated data
export function usePaginatedApi<T>(
  apiFunction: (params: any) => Promise<ApiResponse<{ data: T[]; pagination: any }>>,
  initialParams: any = {}
) {
  const [params, setParams] = useState(initialParams);
  const [allData, setAllData] = useState<T[]>([]);
  const [pagination, setPagination] = useState<any>(null);

  const { data, loading, error, execute } = useApi(apiFunction);

  useEffect(() => {
    execute(params);
  }, [params, execute]);

  useEffect(() => {
    if (data) {
      if (params.page === 1) {
        setAllData(data.data);
      } else {
        setAllData(prev => [...prev, ...data.data]);
      }
      setPagination(data.pagination);
    }
  }, [data, params.page]);

  const loadMore = useCallback(() => {
    if (pagination && pagination.page < pagination.totalPages) {
      setParams(prev => ({ ...prev, page: prev.page + 1 }));
    }
  }, [pagination]);

  const refresh = useCallback(() => {
    setParams(prev => ({ ...prev, page: 1 }));
    setAllData([]);
  }, []);

  const updateParams = useCallback((newParams: any) => {
    setParams(prev => ({ ...prev, ...newParams, page: 1 }));
    setAllData([]);
  }, []);

  return {
    data: allData,
    pagination,
    loading,
    error,
    loadMore,
    refresh,
    updateParams,
    hasMore: pagination ? pagination.page < pagination.totalPages : false,
  };
}

// Hook for real-time data updates
export function usePolling<T>(
  apiFunction: (...args: any[]) => Promise<ApiResponse<T>>,
  interval: number = 5000,
  enabled: boolean = true
) {
  const { data, loading, error, execute } = useApi(apiFunction);
  const [isPolling, setIsPolling] = useState(enabled);

  useEffect(() => {
    if (!isPolling) return;

    const poll = async () => {
      try {
        await execute();
      } catch (error) {
        console.error('Polling error:', error);
      }
    };

    // Initial fetch
    poll();

    // Set up interval
    const intervalId = setInterval(poll, interval);

    return () => clearInterval(intervalId);
  }, [isPolling, interval, execute]);

  const startPolling = useCallback(() => setIsPolling(true), []);
  const stopPolling = useCallback(() => setIsPolling(false), []);

  return {
    data,
    loading,
    error,
    isPolling,
    startPolling,
    stopPolling,
  };
}

// Hook for optimistic updates
export function useOptimisticApi<T>(
  apiFunction: (...args: any[]) => Promise<ApiResponse<T>>,
  optimisticUpdate?: (currentData: T | null, ...args: any[]) => T | null
) {
  const [optimisticData, setOptimisticData] = useState<T | null>(null);
  const { data, loading, error, execute: originalExecute } = useApi(apiFunction);

  const execute = useCallback(async (...args: any[]) => {
    // Apply optimistic update
    if (optimisticUpdate) {
      const newOptimisticData = optimisticUpdate(data, ...args);
      setOptimisticData(newOptimisticData);
    }

    try {
      const result = await originalExecute(...args);
      setOptimisticData(null); // Clear optimistic data on success
      return result;
    } catch (error) {
      setOptimisticData(null); // Clear optimistic data on error
      throw error;
    }
  }, [data, optimisticUpdate, originalExecute]);

  return {
    data: optimisticData || data,
    loading,
    error,
    execute,
    isOptimistic: optimisticData !== null,
  };
}

// Hook for batch operations
export function useBatchApi<T>(
  apiFunction: (item: any) => Promise<ApiResponse<T>>
) {
  const [results, setResults] = useState<{ [key: string]: ApiResponse<T> }>({});
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const executeBatch = useCallback(async (items: any[], keyExtractor: (item: any) => string) => {
    setLoading(true);
    setProgress(0);
    setResults({});

    const total = items.length;
    const newResults: { [key: string]: ApiResponse<T> } = {};

    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      const key = keyExtractor(item);

      try {
        const result = await apiFunction(item);
        newResults[key] = result;
      } catch (error: any) {
        newResults[key] = {
          success: false,
          error: error.message,
        };
      }

      setProgress(((i + 1) / total) * 100);
      setResults({ ...newResults });
    }

    setLoading(false);
    return newResults;
  }, [apiFunction]);

  const getSuccessCount = useCallback(() => {
    return Object.values(results).filter(result => result.success).length;
  }, [results]);

  const getErrorCount = useCallback(() => {
    return Object.values(results).filter(result => !result.success).length;
  }, [results]);

  return {
    results,
    loading,
    progress,
    executeBatch,
    getSuccessCount,
    getErrorCount,
  };
}