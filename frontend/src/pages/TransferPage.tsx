/**
 * TransferPage
 * Main page for bank transfers
 */

import React, { useState, useEffect } from 'react';
import { Transfer } from '../types/transfer';
import { TransferForm } from '../components/TransferForm';
import { useTransfer } from '../hooks/useTransfer';

// Mock account data - in real app this would come from auth/account service
const mockAccounts = [
  {
    id: 1,
    account_number: '1234567890123456',
    account_name: '홍길동 주계좌',
    balance: 1500000
  },
  {
    id: 2,
    account_number: '2345678901234567',
    account_name: '홍길동 적금계좌',
    balance: 500000
  }
];

export const TransferPage: React.FC = () => {
  const {
    createTransfer,
    isSubmitting,
    error,
    lastCreatedTransfer,
    clearError,
    clearLastTransfer
  } = useTransfer();

  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    // Clear messages after 5 seconds
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  useEffect(() => {
    // Clear messages after 5 seconds
    if (error) {
      const timer = setTimeout(() => clearError(), 5000);
      return () => clearTimeout(timer);
    }
  }, [error, clearError]);

  const handleTransferSuccess = (transfer: Transfer) => {
    console.log('Transfer success object:', transfer);
    const referenceNumber = transfer?.reference_number || '알 수 없음';
    setSuccessMessage(
      `이체가 성공적으로 완료되었습니다. 이체 번호: ${referenceNumber}`
    );
    clearLastTransfer();
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      minimumFractionDigits: 0
    }).format(amount);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">계좌 이체</h1>
          <p className="mt-2 text-gray-600">
            다른 계좌로 안전하고 빠르게 이체하세요
          </p>
        </div>

        {/* Success Message */}
        {successMessage && (
          <div className="mb-6 bg-green-50 border border-green-200 rounded-md p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-green-800">
                  {successMessage}
                </p>
              </div>
              <div className="ml-auto pl-3">
                <button
                  onClick={() => setSuccessMessage(null)}
                  className="text-green-400 hover:text-green-600"
                >
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Transfer Form */}
          <div className="lg:col-span-2">
            <TransferForm
              accounts={mockAccounts}
              onSubmit={createTransfer}
              isLoading={isSubmitting}
              error={error}
              onSuccess={handleTransferSuccess}
            />
          </div>

          {/* Sidebar Info */}
          <div className="space-y-6">
            {/* Account Summary */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">내 계좌</h3>
              <div className="space-y-3">
                {mockAccounts.map((account) => (
                  <div key={account.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-md">
                    <div>
                      <p className="font-medium text-sm">{account.account_name}</p>
                      <p className="text-xs text-gray-500">{account.account_number}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium text-sm">{formatCurrency(account.balance)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Transfer Limits Info */}
            <div className="bg-blue-50 rounded-lg p-6">
              <h3 className="text-lg font-medium text-blue-900 mb-4">이체 한도</h3>
              <div className="space-y-2 text-sm text-blue-800">
                <div className="flex justify-between">
                  <span>1회 이체 한도:</span>
                  <span className="font-medium">{formatCurrency(1000000)}</span>
                </div>
                <div className="flex justify-between">
                  <span>이체 수수료:</span>
                  <span className="font-medium">무료 (같은 은행)</span>
                </div>
              </div>
            </div>

            {/* Recent Transfer */}
            {lastCreatedTransfer && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">최근 이체</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">받는계좌:</span>
                    <span className="font-medium">{lastCreatedTransfer.to_account_number}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">이체금액:</span>
                    <span className="font-medium">{formatCurrency(lastCreatedTransfer.amount)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">상태:</span>
                    <span className={`font-medium ${
                      lastCreatedTransfer.status === 'COMPLETED' 
                        ? 'text-green-600' 
                        : lastCreatedTransfer.status === 'FAILED' 
                        ? 'text-red-600' 
                        : 'text-yellow-600'
                    }`}>
                      {lastCreatedTransfer.status === 'COMPLETED' ? '완료' :
                       lastCreatedTransfer.status === 'FAILED' ? '실패' :
                       lastCreatedTransfer.status === 'PENDING' ? '처리중' : lastCreatedTransfer.status}
                    </span>
                  </div>
                  {lastCreatedTransfer.reference_number && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">거래번호:</span>
                      <span className="font-mono text-xs">{lastCreatedTransfer.reference_number}</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Available Accounts */}
            <div className="bg-blue-50 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-medium text-blue-900 mb-4">테스트용 계좌 목록</h3>
              <div className="space-y-2 text-sm">
                <div className="bg-white rounded-md p-3 border border-blue-200">
                  <div className="font-medium text-blue-900">1001-2345-6789</div>
                  <div className="text-blue-700">김철수 주계좌</div>
                </div>
                <div className="bg-white rounded-md p-3 border border-blue-200">
                  <div className="font-medium text-blue-900">1002-3456-7890</div>
                  <div className="text-blue-700">이영희 적금계좌</div>
                </div>
                <div className="bg-white rounded-md p-3 border border-blue-200">
                  <div className="font-medium text-blue-900">1003-4567-8901</div>
                  <div className="text-blue-700">박민수 투자계좌</div>
                </div>
                <div className="bg-white rounded-md p-3 border border-blue-200">
                  <div className="font-medium text-blue-900">1004-5678-9012</div>
                  <div className="text-blue-700">최지은 주계좌</div>
                </div>
              </div>
            </div>

            {/* Help Info */}
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">도움말</h3>
              <div className="space-y-3 text-sm text-gray-600">
                <div className="flex items-start space-x-2">
                  <div className="flex-shrink-0 w-1.5 h-1.5 bg-gray-400 rounded-full mt-2"></div>
                  <p>같은 은행 계좌간 이체는 즉시 처리됩니다</p>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="flex-shrink-0 w-1.5 h-1.5 bg-gray-400 rounded-full mt-2"></div>
                  <p>위 테스트 계좌 중 하나를 선택해서 이체해보세요</p>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="flex-shrink-0 w-1.5 h-1.5 bg-gray-400 rounded-full mt-2"></div>
                  <p>이체한 금액은 거래내역에서 확인할 수 있습니다</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TransferPage;