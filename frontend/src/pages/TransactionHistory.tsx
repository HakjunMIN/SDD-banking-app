export function TransactionHistory() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">거래 내역</h1>
        <div className="flex space-x-4">
          <button className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md text-sm font-medium">
            필터
          </button>
          <button className="bg-secondary-600 hover:bg-secondary-700 text-white px-4 py-2 rounded-md text-sm font-medium">
            내보내기
          </button>
        </div>
      </div>
      
      <div className="bg-white shadow-card rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">최근 거래</h2>
        </div>
        
        <div className="divide-y divide-gray-200">
          {/* Sample transaction items */}
          <div className="px-6 py-4 hover:bg-gray-50">
            <div className="flex justify-between items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">점심 식사</p>
                <p className="text-xs text-gray-500">2025-11-07 12:30</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium text-red-600">-25,000원</p>
                <p className="text-xs text-gray-500">체크카드</p>
              </div>
            </div>
          </div>
          
          <div className="px-6 py-4 hover:bg-gray-50">
            <div className="flex justify-between items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">월급 입금</p>
                <p className="text-xs text-gray-500">2025-11-01 09:00</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium text-green-600">+3,000,000원</p>
                <p className="text-xs text-gray-500">계좌이체</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}