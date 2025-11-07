import React, { useState, useEffect } from 'react';
import TransactionItem from './TransactionItem';
import { Transaction, TransactionFilters, PaginationInfo } from '../types/transaction';

interface TransactionListProps {
  accountId?: number;
  filters?: TransactionFilters;
  onTransactionClick?: (transaction: Transaction) => void;
  className?: string;
}

interface TransactionListResponse {
  data: Transaction[];
  pagination: PaginationInfo;
  account_info?: any;
  summary?: any;
}

const TransactionList: React.FC<TransactionListProps> = ({
  accountId = 1,
  filters = {},
  onTransactionClick,
  className = ""
}) => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo>({
    current_page: 1,
    total_pages: 1,
    page_size: 20,
    total_items: 0,
    has_next: false,
    has_previous: false
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTransactions = async (page: number = 1) => {
    try {
      setLoading(true);
      setError(null);

      // Build query parameters
      const params = new URLSearchParams({
        account_id: accountId.toString(),
        limit: pagination.page_size.toString(),
        offset: ((page - 1) * pagination.page_size).toString()
      });

      // Add filters
      if (filters.type) {
        params.append('type', filters.type);
      }
      if (filters.from_date) {
        params.append('from_date', filters.from_date);
      }
      if (filters.to_date) {
        params.append('to_date', filters.to_date);
      }
      if (filters.search) {
        params.append('search', filters.search);
      }
      if (filters.sort_by) {
        params.append('sort_by', filters.sort_by);
      }
      if (filters.sort_order) {
        params.append('sort_order', filters.sort_order);
      }

      const response = await fetch(`http://localhost:8000/api/transactions?${params}`);
      
      if (!response.ok) {
        throw new Error('거래 내역을 불러오는데 실패했습니다.');
      }

      const data: TransactionListResponse = await response.json();
      
      setTransactions(data.data);
      setPagination(data.pagination);
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions(1);
  }, [accountId, filters]);

  const handlePageChange = (page: number) => {
    fetchTransactions(page);
  };

  if (loading) {
    return (
      <div className={`flex justify-center items-center py-8 ${className}`}>
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span className="ml-2 text-gray-600">거래 내역을 불러오는 중...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-red-50 border border-red-200 rounded-lg p-4 ${className}`}>
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              오류 발생
            </h3>
            <div className="mt-1 text-sm text-red-700">
              {error}
            </div>
          </div>
        </div>
        <div className="mt-4">
          <button
            onClick={() => fetchTransactions(pagination.current_page)}
            className="bg-red-100 hover:bg-red-200 text-red-800 text-sm px-3 py-1 rounded transition-colors"
          >
            다시 시도
          </button>
        </div>
      </div>
    );
  }

  if (transactions.length === 0) {
    return (
      <div className={`text-center py-8 ${className}`}>
        <div className="text-gray-400 text-6xl mb-4">📋</div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">거래 내역이 없습니다</h3>
        <p className="text-gray-600">
          {filters.search ? '검색 조건에 맞는 거래가 없습니다.' : '아직 거래 내역이 없습니다.'}
        </p>
      </div>
    );
  }

  return (
    <div className={`bg-white ${className}`}>
      {/* Transaction List */}
      <div className="divide-y divide-gray-200">
        {transactions.map((transaction) => (
          <TransactionItem
            key={transaction.id}
            transaction={transaction}
            onClick={onTransactionClick}
          />
        ))}
      </div>

      {/* Pagination */}
      {pagination.total_pages > 1 && (
        <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 mt-4">
          <div className="flex-1 flex justify-between sm:hidden">
            <button
              onClick={() => handlePageChange(pagination.current_page - 1)}
              disabled={!pagination.has_previous}
              className={`relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md ${
                pagination.has_previous
                  ? 'text-gray-700 bg-white hover:bg-gray-50'
                  : 'text-gray-400 bg-gray-50 cursor-not-allowed'
              }`}
            >
              이전
            </button>
            <button
              onClick={() => handlePageChange(pagination.current_page + 1)}
              disabled={!pagination.has_next}
              className={`ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md ${
                pagination.has_next
                  ? 'text-gray-700 bg-white hover:bg-gray-50'
                  : 'text-gray-400 bg-gray-50 cursor-not-allowed'
              }`}
            >
              다음
            </button>
          </div>
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                총 <span className="font-medium">{pagination.total_items}</span>개 중{' '}
                <span className="font-medium">
                  {(pagination.current_page - 1) * pagination.page_size + 1}
                </span>
                -{' '}
                <span className="font-medium">
                  {Math.min(pagination.current_page * pagination.page_size, pagination.total_items)}
                </span>
                개 표시
              </p>
            </div>
            <div>
              <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button
                  onClick={() => handlePageChange(pagination.current_page - 1)}
                  disabled={!pagination.has_previous}
                  className={`relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium ${
                    pagination.has_previous
                      ? 'text-gray-500 hover:bg-gray-50'
                      : 'text-gray-300 cursor-not-allowed'
                  }`}
                >
                  <span className="sr-only">이전</span>
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </button>

                {/* Page numbers */}
                {Array.from({ length: Math.min(5, pagination.total_pages) }, (_, i) => {
                  const startPage = Math.max(1, pagination.current_page - 2);
                  const pageNumber = startPage + i;
                  
                  if (pageNumber > pagination.total_pages) return null;
                  
                  return (
                    <button
                      key={pageNumber}
                      onClick={() => handlePageChange(pageNumber)}
                      className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                        pageNumber === pagination.current_page
                          ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                          : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                      }`}
                    >
                      {pageNumber}
                    </button>
                  );
                })}

                <button
                  onClick={() => handlePageChange(pagination.current_page + 1)}
                  disabled={!pagination.has_next}
                  className={`relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium ${
                    pagination.has_next
                      ? 'text-gray-500 hover:bg-gray-50'
                      : 'text-gray-300 cursor-not-allowed'
                  }`}
                >
                  <span className="sr-only">다음</span>
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TransactionList;