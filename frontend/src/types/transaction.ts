// Transaction-related TypeScript types and interfaces

export interface Transaction {
  id: number;
  account_id: number;
  transaction_date: string;
  transaction_type: 'deposit' | 'withdrawal' | 'transfer';
  amount: number;
  description: string;
  recipient_account?: string | null;
  balance_after: number;
  reference_number?: string | null;
  status: 'completed' | 'pending' | 'failed';
  created_at: string;
  formatted_amount?: string;
  formatted_balance?: string;
  formatted_date?: string;
  type_icon?: string;
}

export interface TransactionFilters {
  type?: 'deposit' | 'withdrawal' | 'transfer';
  from_date?: string;
  to_date?: string;
  search?: string;
  sort_by?: 'transaction_date' | 'amount';
  sort_order?: 'asc' | 'desc';
}

export interface PaginationInfo {
  current_page: number;
  total_pages: number;
  page_size: number;
  total_items: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface Account {
  id: number;
  account_number: string;
  account_name: string;
  account_type: 'checking' | 'savings' | 'investment';
  balance: number;
  formatted_balance?: string;
  masked_account_number?: string;
  created_at: string;
  updated_at?: string;
}

export interface TransactionSummary {
  total_transactions: number;
  recent_transactions_today: number;
  monthly_deposits: {
    count: number;
    amount: number;
    formatted_amount: string;
  };
  monthly_withdrawals: {
    count: number;
    amount: number;
    formatted_amount: string;
  };
  monthly_net: {
    amount: number;
    formatted_amount: string;
  };
}

export interface TransactionStatistics {
  period_days: number;
  from_date: string;
  to_date: string;
  total_transactions: number;
  deposits: {
    count: number;
    total_amount: number;
    average_amount: number;
    formatted_total: string;
    formatted_average: string;
  };
  withdrawals: {
    count: number;
    total_amount: number;
    average_amount: number;
    formatted_total: string;
    formatted_average: string;
  };
  transfers: {
    count: number;
    total_amount: number;
    formatted_total: string;
  };
  net_change: {
    amount: number;
    formatted_amount: string;
  };
}

export interface ApiResponse<T> {
  data: T;
  pagination?: PaginationInfo;
  account_info?: Account;
  summary?: TransactionSummary;
}

export interface ErrorResponse {
  detail: string;
  status_code?: number;
}

// Filter preset types for common filtering scenarios
export type TransactionFilterPreset = 
  | 'all'
  | 'deposits'
  | 'withdrawals' 
  | 'transfers'
  | 'today'
  | 'this_week'
  | 'this_month';

// Transaction list item display mode
export type TransactionDisplayMode = 'compact' | 'detailed';

// API endpoint types
export interface TransactionListParams {
  account_id?: number;
  type?: string;
  from_date?: string;
  to_date?: string;
  limit?: number;
  offset?: number;
  search?: string;
  sort_by?: string;
  sort_order?: string;
}