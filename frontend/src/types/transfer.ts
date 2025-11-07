/**
 * Transfer Types and Interfaces
 * TypeScript definitions for transfer-related data structures
 */

// Transfer status enumeration
export enum TransferStatus {
  PENDING = 'PENDING',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
  CANCELLED = 'CANCELLED'
}

// Transfer type enumeration
export enum TransferType {
  INTERNAL = 'INTERNAL',  // Same bank transfer
  EXTERNAL = 'EXTERNAL'   // Different bank transfer
}

// Virtual Bank interface
export interface VirtualBank {
  id: number;
  bank_code: string;
  bank_name: string;
  bank_name_en?: string;
  is_active: boolean;
  transfer_fee: number;
  processing_time_min: number;
  processing_time_max: number;
  success_rate: number;
  api_endpoint?: string;
  description?: string;
}

// Transfer request interface
export interface TransferRequest {
  from_account_id: number;
  to_account_number: string;
  to_bank_id?: number;  // Optional for internal transfers
  amount: number;
  description?: string;
  transfer_type: TransferType;
}

// Transfer response interface
export interface Transfer {
  id: number;
  from_account_id: number;
  to_account_number: string;
  to_bank_id?: number;
  amount: number;
  description?: string;
  status: TransferStatus;
  transfer_type: TransferType;
  reference_number: string;
  created_at: string;
  completed_at?: string;
  error_message?: string;
  virtual_bank?: VirtualBank;  // Populated for external transfers
}

// Transfer validation interface
export interface TransferValidation {
  valid: boolean;
  errors?: string[];
  warnings?: string[];
  estimated_fee?: number;
  estimated_processing_time?: number;
}

// Transfer form data interface
export interface TransferFormData {
  from_account_id: number | null;
  to_account_number: string;
  to_bank_id: number | null;
  amount: number | null;
  description: string;
  transfer_type: TransferType;
}

// Account for transfer selection
export interface AccountForTransfer {
  id: number;
  account_number: string;
  account_name: string;
  account_type: string;
  balance: number;
  daily_transfer_limit?: number;
  per_transaction_limit?: number;
  transfer_enabled?: boolean;
  daily_transfer_used?: number;
}

// Transfer limits interface
export interface TransferLimits {
  daily_limit: number;
  per_transaction_limit: number;
  daily_used: number;
  remaining_daily: number;
  remaining_transaction: number;
}

// Transfer history query parameters
export interface TransferHistoryParams {
  account_id?: number;
  status?: TransferStatus;
  transfer_type?: TransferType;
  start_date?: string;
  end_date?: string;
  limit?: number;
  offset?: number;
}

// Transfer statistics interface
export interface TransferStats {
  total_transfers: number;
  successful_transfers: number;
  failed_transfers: number;
  total_amount: number;
  average_amount: number;
  success_rate: number;
}

// API response wrappers
export interface TransferResponse {
  data: Transfer;
  message: string;
  success: boolean;
}

export interface TransferListResponse {
  data: Transfer[];
  pagination: {
    current_page: number;
    total_pages: number;
    page_size: number;
    total_items: number;
    has_next: boolean;
    has_previous: boolean;
  };
  message: string;
  success: boolean;
}

export interface BankListResponse {
  data: VirtualBank[];
  message: string;
  success: boolean;
}

// Error response interface
export interface ApiErrorResponse {
  error: string;
  message: string;
  details?: any;
  success: false;
}

// Transfer flow state interface (for multi-step forms)
export interface TransferFlowState {
  step: 'form' | 'confirm' | 'processing' | 'complete' | 'error';
  form_data: TransferFormData;
  validation?: TransferValidation;
  transfer?: Transfer;
  error?: string;
}

// Transfer confirmation data
export interface TransferConfirmationData {
  form_data: TransferFormData;
  validation: TransferValidation;
  from_account: AccountForTransfer;
  to_bank?: VirtualBank;
  estimated_completion: string;
}

// Hook state interfaces
export interface UseTransferState {
  transfers: Transfer[];
  current_transfer: Transfer | null;
  loading: boolean;
  error: string | null;
  form_state: TransferFlowState;
}

export interface UseTransferActions {
  createTransfer: (data: TransferRequest) => Promise<Transfer>;
  getTransfers: (params?: TransferHistoryParams) => Promise<Transfer[]>;
  getTransfer: (id: number) => Promise<Transfer>;
  validateTransfer: (data: TransferRequest) => Promise<TransferValidation>;
  cancelTransfer: (id: number) => Promise<boolean>;
  resetForm: () => void;
  setFormStep: (step: TransferFlowState['step']) => void;
}

// Utility type guards
export const isTransferPending = (transfer: Transfer): boolean => {
  return transfer.status === TransferStatus.PENDING;
};

export const isTransferCompleted = (transfer: Transfer): boolean => {
  return transfer.status === TransferStatus.COMPLETED;
};

export const isTransferFailed = (transfer: Transfer): boolean => {
  return transfer.status === TransferStatus.FAILED;
};

export const isExternalTransfer = (transfer: Transfer): boolean => {
  return transfer.transfer_type === TransferType.EXTERNAL;
};

export const canCancelTransfer = (transfer: Transfer): boolean => {
  return transfer.status === TransferStatus.PENDING;
};