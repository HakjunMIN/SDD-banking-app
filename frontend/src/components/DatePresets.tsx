import React from 'react';
import { dateUtils } from '../utils/dateUtils';

interface DatePresetsProps {
  onPresetSelect: (fromDate: string, toDate: string) => void;
  selectedFromDate?: string;
  selectedToDate?: string;
}

const DatePresets: React.FC<DatePresetsProps> = ({
  onPresetSelect,
  selectedFromDate,
  selectedToDate
}) => {
  const presets = [
    {
      label: '오늘',
      getValue: () => dateUtils.getToday()
    },
    {
      label: '어제',
      getValue: () => dateUtils.getYesterday()
    },
    {
      label: '최근 7일',
      getValue: () => dateUtils.getLastDays(7)
    },
    {
      label: '최근 30일',
      getValue: () => dateUtils.getLastDays(30)
    },
    {
      label: '이번 달',
      getValue: () => dateUtils.getCurrentMonth()
    },
    {
      label: '지난 달',
      getValue: () => dateUtils.getLastMonth()
    },
    {
      label: '최근 3개월',
      getValue: () => dateUtils.getLastMonths(3)
    }
  ];

  const isPresetActive = (fromDate: string, toDate: string) => {
    return selectedFromDate === fromDate && selectedToDate === toDate;
  };

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-medium text-gray-700">빠른 선택</h3>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        {presets.map((preset) => {
          const { fromDate, toDate } = preset.getValue();
          const isActive = isPresetActive(fromDate, toDate);
          
          return (
            <button
              key={preset.label}
              onClick={() => onPresetSelect(fromDate, toDate)}
              className={`px-3 py-2 text-xs font-medium rounded-md border transition-colors duration-200 ${
                isActive
                  ? 'bg-blue-100 text-blue-800 border-blue-300'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 hover:border-gray-400'
              }`}
            >
              {preset.label}
            </button>
          );
        })}
      </div>
      
      <div className="text-xs text-gray-500">
        클릭하여 해당 기간으로 빠르게 설정할 수 있습니다.
      </div>
    </div>
  );
};

export default DatePresets;