/**
 * TransferForm Component
 * Form for creating internal transfers between accounts
 */

import React, { useState } from 'react';
import { Transfer, TransferRequest } from '../types/transfer';

interface TransferFormProps {
  /** Current user's accounts for selection */
  accounts: Array<{
    id: number;
    account_number: string;
    account_name: string;
    balance: number;
  }>;
  /** Callback when transfer is submitted */
  onSubmit: (transferData: TransferRequest) => Promise<Transfer>;
  /** Loading state */
  isLoading?: boolean;
  /** Error message to display */
  error?: string | null;
  /** Success callback after transfer */
  onSuccess?: (transfer: Transfer) => void;
}

interface FormData {
  from_account_id: number | null;
  to_account_number: string;
  amount: string;
  description: string;
}

interface FormErrors {
  from_account_id?: string;
  to_account_number?: string;
  amount?: string;
  general?: string;
}

export const TransferForm: React.FC<TransferFormProps> = ({
  accounts,
  onSubmit,
  isLoading = false,
  error,
  onSuccess
}) => {
  const [formData, setFormData] = useState<FormData>({
    from_account_id: null,
    to_account_number: '',
    amount: '',
    description: ''
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Validate from account
    if (!formData.from_account_id) {
      newErrors.from_account_id = 'Please select a source account';
    }

    // Validate to account number
    if (!formData.to_account_number.trim()) {
      newErrors.to_account_number = 'Please enter destination account number';
    } else if (!/^\d{10,20}$/.test(formData.to_account_number.trim())) {
      newErrors.to_account_number = 'Account number must be 10-20 digits';
    }

    // Check if not transferring to same account
    const selectedAccount = accounts.find(acc => acc.id === formData.from_account_id);
    if (selectedAccount && selectedAccount.account_number === formData.to_account_number.trim()) {
      newErrors.to_account_number = 'Cannot transfer to the same account';
    }

    // Validate amount
    if (!formData.amount.trim()) {
      newErrors.amount = 'Please enter transfer amount';
    } else {
      const amount = parseFloat(formData.amount);
      if (isNaN(amount) || amount <= 0) {
        newErrors.amount = 'Amount must be a positive number';
      } else if (amount > 1000000) {
        newErrors.amount = 'Amount cannot exceed 1,000,000 KRW';
      } else if (selectedAccount && amount > selectedAccount.balance) {
        newErrors.amount = 'Insufficient balance';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm() || isSubmitting || isLoading) {
      return;
    }

    setIsSubmitting(true);
    setErrors({});

    try {
      const transferRequest: TransferRequest = {
        from_account_id: formData.from_account_id!,
        to_account_number: formData.to_account_number.trim(),
        amount: parseFloat(formData.amount),
        description: formData.description.trim() || undefined,
        to_bank_id: undefined  // undefined for internal transfers
      };

      const transfer = await onSubmit(transferRequest);
      
      // Clear form on success
      setFormData({
        from_account_id: null,
        to_account_number: '',
        amount: '',
        description: ''
      });
      
      onSuccess?.(transfer);
      
    } catch (err: any) {
      console.error('Transfer submission error:', err);
      console.log('Error object details:', {
        message: err?.message,
        error: err?.error,
        details: err?.details,
        fullObject: err
      });
      
      // Handle specific error messages
      let errorMessage = 'Failed to process transfer. Please try again.';
      
      if (err?.message) {
        if (err.message.includes('Destination account not found')) {
          errorMessage = '입금 계좌번호를 찾을 수 없습니다. 계좌번호를 다시 확인해주세요.';
        } else if (err.message.includes('Insufficient balance')) {
          errorMessage = '잔액이 부족합니다. 이체 금액을 확인해주세요.';
        } else if (err.message.includes('Transfer amount must be positive')) {
          errorMessage = '이체 금액은 0보다 커야 합니다.';
        } else if (err.message.includes('Transfer amount exceeds maximum limit')) {
          errorMessage = '이체 금액이 최대 한도를 초과했습니다. (최대: 1,000,000원)';
        } else {
          errorMessage = err.message;
        }
      }
      
      setErrors({ general: errorMessage });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (field: keyof FormData, value: string | number | null) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    
    // Clear field-specific error when user starts typing
    if (field in errors && errors[field as keyof FormErrors]) {
      setErrors(prev => ({
        ...prev,
        [field]: undefined
      }));
    }
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const selectedAccount = accounts.find(acc => acc.id === formData.from_account_id);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">계좌 이체</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Source Account Selection */}
        <div>
          <label htmlFor="from_account" className="block text-sm font-medium text-gray-700 mb-2">
            출금계좌
          </label>
          <select
            id="from_account"
            value={formData.from_account_id || ''}
            onChange={(e) => handleInputChange('from_account_id', e.target.value ? parseInt(e.target.value) : null)}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${
              errors.from_account_id ? 'border-red-500' : 'border-gray-300'
            }`}
            disabled={isLoading || isSubmitting}
          >
            <option value="">계좌를 선택하세요</option>
            {accounts.map((account) => (
              <option key={account.id} value={account.id}>
                {account.account_name} ({account.account_number}) - {formatCurrency(account.balance)}
              </option>
            ))}
          </select>
          {errors.from_account_id && (
            <p className="mt-1 text-sm text-red-600">{errors.from_account_id}</p>
          )}
          {selectedAccount && (
            <p className="mt-1 text-sm text-gray-600">
              사용가능 잔액: {formatCurrency(selectedAccount.balance)}
            </p>
          )}
        </div>

        {/* Destination Account Number */}
        <div>
          <label htmlFor="to_account_number" className="block text-sm font-medium text-gray-700 mb-2">
            입금계좌번호
          </label>
          <input
            type="text"
            id="to_account_number"
            value={formData.to_account_number}
            onChange={(e) => handleInputChange('to_account_number', e.target.value)}
            placeholder="계좌번호를 입력하세요 (숫자만)"
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${
              errors.to_account_number ? 'border-red-500' : 'border-gray-300'
            }`}
            disabled={isLoading || isSubmitting}
            maxLength={20}
          />
          {errors.to_account_number && (
            <p className="mt-1 text-sm text-red-600">{errors.to_account_number}</p>
          )}
        </div>

        {/* Transfer Amount */}
        <div>
          <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
            이체금액 (KRW)
          </label>
          <input
            type="number"
            id="amount"
            value={formData.amount}
            onChange={(e) => handleInputChange('amount', e.target.value)}
            placeholder="이체할 금액을 입력하세요"
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${
              errors.amount ? 'border-red-500' : 'border-gray-300'
            }`}
            disabled={isLoading || isSubmitting}
            min="1"
            max="1000000"
            step="1"
          />
          {errors.amount && (
            <p className="mt-1 text-sm text-red-600">{errors.amount}</p>
          )}
        </div>

        {/* Transfer Description */}
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
            이체사유 (선택사항)
          </label>
          <input
            type="text"
            id="description"
            value={formData.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            placeholder="이체 사유를 입력하세요"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            disabled={isLoading || isSubmitting}
            maxLength={500}
          />
        </div>

        {/* Error Messages */}
        {(errors.general || error) && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-sm text-red-600">{errors.general || error}</p>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => {
              setFormData({
                from_account_id: null,
                to_account_number: '',
                amount: '',
                description: ''
              });
              setErrors({});
            }}
            className="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
            disabled={isLoading || isSubmitting}
          >
            초기화
          </button>
          <button
            type="submit"
            disabled={isLoading || isSubmitting}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? '이체 처리중...' : '이체하기'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TransferForm;