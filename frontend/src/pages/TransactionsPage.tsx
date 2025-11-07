import React, { useState, useEffect } from 'react';
import TransactionList from '../components/TransactionList';
import TransactionDetail from '../components/TransactionDetail';
import TransactionFilter from '../components/TransactionFilter';
import DateRangeFilter from '../components/DateRangeFilter';
import DatePresets from '../components/DatePresets';
import { useTransactionFilter } from '../hooks/useTransactionFilter';
import { Transaction, Account, TransactionFilters } from '../types/transaction';

const TransactionsPage: React.FC = () => {
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [account, setAccount] = useState<Account | null>(null);
  const [filters, setFilters] = useState<TransactionFilters>({});
  
  // Use the transaction filter hook for type filtering
  const {
    selectedType,
    setSelectedType,
    clearFilters: clearTypeFilter,
    hasActiveFilters: hasTypeFilter
  } = useTransactionFilter();

  // Load account information on component mount
  useEffect(() => {
    const loadAccountInfo = async () => {
      try {
        // For now, we'll use account ID 1 as default
        // In a real app, this would come from auth context or URL params
        const response = await fetch('http://localhost:8000/api/accounts/1');
        if (response.ok) {
          const accountData = await response.json();
          setAccount(accountData.data);
        }
      } catch (error) {
        console.error('Failed to load account info:', error);
      }
    };

    loadAccountInfo();
  }, []);

  // Update filters when type filter changes
  useEffect(() => {
    setFilters(prevFilters => ({
      ...prevFilters,
      type: selectedType as TransactionFilters['type']
    }));
  }, [selectedType]);

  const handleTransactionClick = (transaction: Transaction) => {
    setSelectedTransaction(transaction);
    setIsDetailModalOpen(true);
  };

  const handleCloseDetail = () => {
    setIsDetailModalOpen(false);
    setSelectedTransaction(null);
  };

  const handleFiltersChange = (newFilters: TransactionFilters) => {
    setFilters(newFilters);
  };

  const handleClearAllFilters = () => {
    clearTypeFilter();
    setFilters({});
  };

  const handleDateRangeClear = () => {
    setFilters(prevFilters => ({
      ...prevFilters,
      from_date: undefined,
      to_date: undefined
    }));
  };

  const handlePresetSelect = (fromDate: string, toDate: string) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      from_date: fromDate,
      to_date: toDate
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">거래 내역</h1>
              {account && (
                <p className="mt-1 text-sm text-gray-500">
                  계좌: {account.masked_account_number || account.account_number} ({account.account_name})
                </p>
              )}
            </div>
            
            {account && (
              <div className="text-right">
                <div className="text-sm text-gray-500">현재 잔액</div>
                <div className="text-xl font-bold text-gray-900">
                  {account.formatted_balance || new Intl.NumberFormat('ko-KR').format(account.balance)}원
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 gap-6">
          {/* Account Summary Card */}
          {account && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">계좌 요약</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-sm text-blue-600">계좌 종류</div>
                  <div className="text-lg font-semibold text-blue-900">
                    {account.account_type === 'checking' ? '당좌예금' :
                     account.account_type === 'savings' ? '저축예금' : 
                     account.account_type === 'investment' ? '투자계좌' : account.account_type}
                  </div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-sm text-green-600">현재 잔액</div>
                  <div className="text-lg font-semibold text-green-900">
                    {account.formatted_balance || new Intl.NumberFormat('ko-KR').format(account.balance)}원
                  </div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-sm text-purple-600">계좌 번호</div>
                  <div className="text-lg font-semibold text-purple-900">
                    {account.masked_account_number || account.account_number}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Filter Controls */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-medium text-gray-900">거래 필터</h2>
              {(hasTypeFilter || filters.from_date || filters.to_date || filters.search) && (
                <button
                  onClick={handleClearAllFilters}
                  className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                >
                  전체 해제
                </button>
              )}
            </div>
            
            <div className="space-y-6">
              {/* Transaction Type Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  거래 유형
                </label>
                <TransactionFilter
                  selectedType={selectedType}
                  onTypeChange={setSelectedType}
                />
              </div>

              {/* Date Range Filtering */}
              <div className="space-y-4">
                <label className="block text-sm font-medium text-gray-700">
                  기간 조회
                </label>
                
                {/* Date Presets */}
                <DatePresets
                  onPresetSelect={handlePresetSelect}
                  selectedFromDate={filters.from_date}
                  selectedToDate={filters.to_date}
                />
                
                {/* Custom Date Range */}
                <DateRangeFilter
                  fromDate={filters.from_date}
                  toDate={filters.to_date}
                  onFromDateChange={(date) => handleFiltersChange({ ...filters, from_date: date || undefined })}
                  onToDateChange={(date) => handleFiltersChange({ ...filters, to_date: date || undefined })}
                  onClear={handleDateRangeClear}
                />
              </div>

              {/* Search Filter */}
              <div>
                <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
                  검색
                </label>
                <input
                  type="text"
                  id="search"
                  placeholder="거래 내용 검색..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={filters.search || ''}
                  onChange={(e) => handleFiltersChange({ ...filters, search: e.target.value || undefined })}
                />
              </div>

              {/* Quick Filter Buttons */}
              <div className="mt-4 flex flex-wrap gap-2">
                <button
                  onClick={() => handleFiltersChange({})}
                  className={`px-3 py-1 text-sm rounded-full border ${
                    Object.keys(filters).length === 0
                      ? 'bg-blue-100 text-blue-800 border-blue-300'
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  전체
                </button>
                <button
                  onClick={() => handleFiltersChange({ type: 'deposit' })}
                  className={`px-3 py-1 text-sm rounded-full border ${
                    filters.type === 'deposit'
                      ? 'bg-green-100 text-green-800 border-green-300'
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  입금
                </button>
                <button
                  onClick={() => handleFiltersChange({ type: 'withdrawal' })}
                  className={`px-3 py-1 text-sm rounded-full border ${
                    filters.type === 'withdrawal'
                      ? 'bg-red-100 text-red-800 border-red-300'
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  출금
                </button>
                <button
                  onClick={() => handleFiltersChange({ type: 'transfer' })}
                  className={`px-3 py-1 text-sm rounded-full border ${
                    filters.type === 'transfer'
                      ? 'bg-blue-100 text-blue-800 border-blue-300'
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  이체
                </button>
                <button
                  onClick={() => {
                    const today = new Date();
                    const weekAgo = new Date();
                    weekAgo.setDate(today.getDate() - 7);
                    handleFiltersChange({
                      from_date: weekAgo.toISOString().split('T')[0],
                      to_date: today.toISOString().split('T')[0]
                    });
                  }}
                  className={`px-3 py-1 text-sm rounded-full border ${
                    filters.from_date && filters.to_date
                      ? 'bg-purple-100 text-purple-800 border-purple-300'
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  최근 7일
                </button>
              </div>
            </div>
          </div>

          {/* Transaction List */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">거래 목록</h2>
              <TransactionList
                accountId={account?.id || 1}
                filters={filters}
                onTransactionClick={handleTransactionClick}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Transaction Detail Modal */}
      <TransactionDetail
        transaction={selectedTransaction}
        isOpen={isDetailModalOpen}
        onClose={handleCloseDetail}
      />
    </div>
  );
};

export default TransactionsPage;