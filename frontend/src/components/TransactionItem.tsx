import React from 'react';
import { Transaction } from '../types/transaction';

interface TransactionItemProps {
  transaction: Transaction;
  onClick?: (transaction: Transaction) => void;
  showAccount?: boolean;
}

const TransactionItem: React.FC<TransactionItemProps> = ({
  transaction,
  onClick,
  showAccount = false
}) => {
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
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            완료
          </span>
        );
      case 'pending':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
            대기중
          </span>
        );
      case 'failed':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
            실패
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
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
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const transactionDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());

    if (transactionDate.getTime() === today.getTime()) {
      return `오늘 ${date.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })}`;
    } else {
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      
      if (transactionDate.getTime() === yesterday.getTime()) {
        return `어제 ${date.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })}`;
      } else {
        return date.toLocaleDateString('ko-KR', {
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      }
    }
  };

  return (
    <div 
      className={`bg-white border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors ${
        onClick ? 'cursor-pointer' : ''
      }`}
      onClick={() => onClick?.(transaction)}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3 flex-1">
          {/* Transaction Icon */}
          <div className="flex-shrink-0">
            <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center text-lg">
              {getTransactionIcon(transaction.transaction_type)}
            </div>
          </div>

          {/* Transaction Details */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {transaction.description || `${formatTransactionType(transaction.transaction_type)}`}
                </p>
                <div className="flex items-center space-x-2 mt-1">
                  <p className="text-xs text-gray-500">
                    {formatDate(transaction.transaction_date)}
                  </p>
                  {transaction.reference_number && (
                    <>
                      <span className="text-xs text-gray-400">•</span>
                      <p className="text-xs text-gray-500">
                        참조: {transaction.reference_number}
                      </p>
                    </>
                  )}
                </div>
                
                {/* Recipient Account (for transfers) */}
                {transaction.transaction_type === 'transfer' && transaction.recipient_account && (
                  <p className="text-xs text-gray-500 mt-1">
                    받는 계좌: {transaction.recipient_account}
                  </p>
                )}

                {/* Account info (if showAccount is true) */}
                {showAccount && (
                  <p className="text-xs text-gray-500 mt-1">
                    계좌: {transaction.account_id}
                  </p>
                )}
              </div>

              {/* Amount and Status */}
              <div className="flex flex-col items-end space-y-1">
                <span className={`text-sm font-medium ${getAmountColor(transaction.transaction_type)}`}>
                  {transaction.formatted_amount || formatAmount(transaction.amount, transaction.transaction_type)}
                </span>
                {transaction.status !== 'completed' && getStatusBadge(transaction.status)}
              </div>
            </div>

            {/* Balance After Transaction */}
            <div className="mt-2 flex justify-between items-center text-xs text-gray-500">
              <span>
                타입: {formatTransactionType(transaction.transaction_type)}
              </span>
              <span>
                잔액: {transaction.formatted_balance || new Intl.NumberFormat('ko-KR').format(transaction.balance_after)}원
              </span>
            </div>
          </div>
        </div>

        {/* Chevron for clickable items */}
        {onClick && (
          <div className="flex-shrink-0 ml-2">
            <svg 
              className="w-5 h-5 text-gray-400" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M9 5l7 7-7 7" 
              />
            </svg>
          </div>
        )}
      </div>
    </div>
  );
};

export default TransactionItem;