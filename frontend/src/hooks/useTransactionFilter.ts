import { useState, useCallback } from 'react';

export interface UseTransactionFilterResult {
  selectedType: string | null;
  setSelectedType: (type: string | null) => void;
  clearFilters: () => void;
  hasActiveFilters: boolean;
  getFilterParams: () => Record<string, string>;
}

export const useTransactionFilter = (initialType: string | null = null): UseTransactionFilterResult => {
  const [selectedType, setSelectedType] = useState<string | null>(initialType);

  const clearFilters = useCallback(() => {
    setSelectedType(null);
  }, []);

  const hasActiveFilters = selectedType !== null;

  const getFilterParams = useCallback(() => {
    const params: Record<string, string> = {};
    
    if (selectedType) {
      params.type = selectedType;
    }
    
    return params;
  }, [selectedType]);

  return {
    selectedType,
    setSelectedType,
    clearFilters,
    hasActiveFilters,
    getFilterParams
  };
};

export default useTransactionFilter;