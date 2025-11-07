import React from 'react';
import { Transaction } from '../types/transaction';

interface TransactionDetailProps {
  transaction: Transaction | null;
  isOpen: boolean;
  onClose: () => void;
}

const TransactionDetail: React.FC<TransactionDetailProps> = ({
  transaction,
  isOpen,
  onClose
}) => {
  if (!isOpen || !transaction) {
    return null;
  }

  const getTransactionIcon = (type: string) => {
    switch (type) {
      case 'deposit':
        return '💰';
      case 'withdrawal':
        return '💸';
      case 'transfer':
        return '🔄';
      default:
        return '📄';
    }
  };

  const getAmountColor = (type: string) => {
    switch (type) {
      case 'deposit':
        return 'text-green-600';
      case 'withdrawal':
        return 'text-red-600';
      case 'transfer':
        return 'text-blue-600';
      default:
        return 'text-gray-600';
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
            ✓ 완료
          </span>
        );
      case 'pending':
        return (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
            ⏳ 대기중
          </span>
        );
      case 'failed':
        return (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">
            ✗ 실패
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800">
            {status}
          </span>
        );
    }
  };

  const formatTransactionType = (type: string) => {
    switch (type) {
      case 'deposit':
        return '입금';
      case 'withdrawal':
        return '출금';
      case 'transfer':
        return '이체';
      default:
        return type;
    }
  };

  const formatAmount = (amount: number, type: string) => {
    const sign = type === 'withdrawal' ? '-' : '+';
    const formattedAmount = new Intl.NumberFormat('ko-KR').format(Math.abs(amount));
    return `${sign}${formattedAmount}원`;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-screen overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">거래 상세 정보</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            aria-label="닫기"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Transaction Overview */}
          <div className="flex items-center space-x-4 mb-6">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center text-2xl">
              {getTransactionIcon(transaction.transaction_type)}
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-medium text-gray-900">
                {transaction.description || formatTransactionType(transaction.transaction_type)}
              </h3>
              <div className="flex items-center space-x-3 mt-2">
                <span className={`text-2xl font-bold ${getAmountColor(transaction.transaction_type)}`}>
                  {transaction.formatted_amount || formatAmount(transaction.amount, transaction.transaction_type)}
                </span>
                {getStatusBadge(transaction.status)}
              </div>
            </div>
          </div>

          {/* Transaction Details Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Basic Information */}
            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-500 uppercase tracking-wide">기본 정보</h4>
              
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">거래 ID:</span>
                  <span className="text-sm font-medium text-gray-900">#{transaction.id}</span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">거래 유형:</span>
                  <span className="text-sm font-medium text-gray-900">
                    {formatTransactionType(transaction.transaction_type)}
                  </span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">계좌 ID:</span>
                  <span className="text-sm font-medium text-gray-900">{transaction.account_id}</span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">거래 일시:</span>
                  <span className="text-sm font-medium text-gray-900">
                    {transaction.formatted_date || formatDate(transaction.transaction_date)}
                  </span>
                </div>
                
                {transaction.reference_number && (
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">참조 번호:</span>
                    <span className="text-sm font-medium text-gray-900">{transaction.reference_number}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Financial Information */}
            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-500 uppercase tracking-wide">금액 정보</h4>
              
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">거래 금액:</span>
                  <span className={`text-sm font-medium ${getAmountColor(transaction.transaction_type)}`}>
                    {transaction.formatted_amount || formatAmount(transaction.amount, transaction.transaction_type)}
                  </span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500">거래 후 잔액:</span>
                  <span className="text-sm font-medium text-gray-900">
                    {transaction.formatted_balance || new Intl.NumberFormat('ko-KR').format(transaction.balance_after)}원
                  </span>
                </div>
                
                {transaction.transaction_type === 'transfer' && transaction.recipient_account && (
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">받는 계좌:</span>
                    <span className="text-sm font-medium text-gray-900">{transaction.recipient_account}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Description Section */}
          {transaction.description && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h4 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">거래 설명</h4>
              <p className="text-sm text-gray-900 bg-gray-50 p-3 rounded-lg">
                {transaction.description}
              </p>
            </div>
          )}

          {/* Metadata */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <h4 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">시스템 정보</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-gray-500">
              <div>
                <span className="font-medium">생성 일시:</span>
                <br />
                {formatDate(transaction.created_at)}
              </div>
              <div>
                <span className="font-medium">상태:</span>
                <br />
                <span className="inline-block mt-1">
                  {getStatusBadge(transaction.status)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end space-x-3 p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            닫기
          </button>
        </div>
      </div>
    </div>
  );
};

export default TransactionDetail;