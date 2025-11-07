import React from 'react';

export interface TransactionFilterProps {
  selectedType: string | null;
  onTypeChange: (type: string | null) => void;
  className?: string;
}

const TRANSACTION_TYPES = [
  { value: null, label: '전체' },
  { value: 'deposit', label: '입금' },
  { value: 'withdrawal', label: '출금' },
  { value: 'transfer', label: '계좌이체' }
];

export const TransactionFilter: React.FC<TransactionFilterProps> = ({
  selectedType,
  onTypeChange,
  className = ''
}) => {
  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {TRANSACTION_TYPES.map((type) => (
        <button
          key={type.value || 'all'}
          onClick={() => onTypeChange(type.value)}
          className={`
            px-4 py-2 rounded-lg text-sm font-medium transition-colors
            ${selectedType === type.value
              ? 'bg-blue-600 text-white shadow-md'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }
          `}
        >
          {type.label}
        </button>
      ))}
    </div>
  );
};

export default TransactionFilter;