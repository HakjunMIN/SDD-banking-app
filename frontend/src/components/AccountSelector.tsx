/**
 * AccountSelector Component
 * Dropdown component for selecting bank accounts
 */

import React from 'react';

export interface Account {
  id: number;
  account_number: string;
  account_name: string;
  account_type: string;
  balance: number;
}

interface AccountSelectorProps {
  /** List of accounts to display */
  accounts: Account[];
  /** Currently selected account ID */
  selectedAccountId?: number | null;
  /** Callback when account is selected */
  onSelect: (accountId: number | null) => void;
  /** Placeholder text */
  placeholder?: string;
  /** Whether the selector is disabled */
  disabled?: boolean;
  /** Whether to show account balance */
  showBalance?: boolean;
  /** CSS class name */
  className?: string;
  /** Error state */
  error?: boolean;
  /** Accounts to exclude from selection */
  excludeAccounts?: number[];
}

export const AccountSelector: React.FC<AccountSelectorProps> = ({
  accounts,
  selectedAccountId,
  onSelect,
  placeholder = '계좌를 선택하세요',
  disabled = false,
  showBalance = true,
  className = '',
  error = false,
  excludeAccounts = []
}) => {
  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const getAccountTypeLabel = (type: string): string => {
    const typeMap: Record<string, string> = {
      'checking': '입출금',
      'savings': '적금',
      'deposit': '예금'
    };
    return typeMap[type] || type;
  };

  const filteredAccounts = accounts.filter(account => 
    !excludeAccounts.includes(account.id)
  );

  const selectedAccount = filteredAccounts.find(account => account.id === selectedAccountId);

  return (
    <div className={className}>
      <select
        value={selectedAccountId || ''}
        onChange={(e) => onSelect(e.target.value ? parseInt(e.target.value) : null)}
        disabled={disabled}
        className={`
          w-full px-3 py-2 border rounded-md shadow-sm 
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
          ${error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'}
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
          transition-colors duration-200
        `}
      >
        <option value="">{placeholder}</option>
        {filteredAccounts.map((account) => (
          <option key={account.id} value={account.id}>
            {account.account_name} ({account.account_number})
            {showBalance && ` - ${formatCurrency(account.balance)}`}
          </option>
        ))}
      </select>
      
      {/* Selected Account Details */}
      {selectedAccount && (
        <div className="mt-2 text-sm text-gray-600">
          <div className="flex justify-between items-center">
            <span>{getAccountTypeLabel(selectedAccount.account_type)} 계좌</span>
            {showBalance && (
              <span className="font-medium">
                잔액: {formatCurrency(selectedAccount.balance)}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AccountSelector;