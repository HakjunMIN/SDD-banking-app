import React from 'react';

interface DateRangeFilterProps {
  fromDate?: string;
  toDate?: string;
  onFromDateChange: (date: string) => void;
  onToDateChange: (date: string) => void;
  onClear: () => void;
}

const DateRangeFilter: React.FC<DateRangeFilterProps> = ({
  fromDate,
  toDate,
  onFromDateChange,
  onToDateChange,
  onClear
}) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-gray-700">기간 선택</h3>
        {(fromDate || toDate) && (
          <button
            onClick={onClear}
            className="text-xs text-blue-600 hover:text-blue-800"
          >
            초기화
          </button>
        )}
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="from-date-range" className="block text-xs font-medium text-gray-600 mb-1">
            시작 날짜
          </label>
          <input
            type="date"
            id="from-date-range"
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            value={fromDate || ''}
            onChange={(e) => onFromDateChange(e.target.value)}
            max={toDate || undefined}
          />
        </div>
        
        <div>
          <label htmlFor="to-date-range" className="block text-xs font-medium text-gray-600 mb-1">
            종료 날짜
          </label>
          <input
            type="date"
            id="to-date-range"
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            value={toDate || ''}
            onChange={(e) => onToDateChange(e.target.value)}
            min={fromDate || undefined}
          />
        </div>
      </div>
      
      {fromDate && toDate && (
        <div className="text-xs text-gray-500">
          {new Date(fromDate).toLocaleDateString('ko-KR')} ~ {new Date(toDate).toLocaleDateString('ko-KR')}
        </div>
      )}
    </div>
  );
};

export default DateRangeFilter;