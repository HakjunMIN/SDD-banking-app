/**
 * Transfer API Client
 * HTTP client for transfer-related API operations
 */

import axios, { AxiosResponse } from 'axios';
import {
  Transfer,
  TransferRequest,
  TransferResponse,
  TransferListResponse,
  BankListResponse,
  VirtualBank,
  TransferValidation,
  TransferHistoryParams,
  TransferLimits,
  ApiErrorResponse
} from '../types/transfer';

// API base configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,  // 30 seconds for transfer operations
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for authentication (if needed)
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with error status
      const errorData: ApiErrorResponse = {
        error: error.response.data.error || 'API Error',
        message: error.response.data.message || 'An error occurred',
        details: error.response.data.details,
        success: false
      };
      return Promise.reject(errorData);
    } else if (error.request) {
      // Network error
      const networkError: ApiErrorResponse = {
        error: 'Network Error',
        message: 'Unable to connect to server',
        success: false
      };
      return Promise.reject(networkError);
    } else {
      // Other error
      const genericError: ApiErrorResponse = {
        error: 'Unknown Error',
        message: error.message || 'An unknown error occurred',
        success: false
      };
      return Promise.reject(genericError);
    }
  }
);

/**
 * Transfer API Service Class
 */
export class TransferAPIService {
  
  /**
   * Create a new transfer
   * 
   * @param transferData Transfer request data
   * @returns Promise<Transfer> Created transfer
   */
  static async createTransfer(transferData: TransferRequest): Promise<Transfer> {
    try {
      const response: AxiosResponse<TransferResponse> = await apiClient.post(
        '/api/v1/transfers',
        transferData
      );
      return response.data.data;
    } catch (error) {
      console.error('Create transfer error:', error);
      throw error;
    }
  }

  /**
   * Get transfer history
   * 
   * @param params Query parameters for filtering
   * @returns Promise<Transfer[]> Array of transfers
   */
  static async getTransfers(params?: TransferHistoryParams): Promise<Transfer[]> {
    try {
      const response: AxiosResponse<TransferListResponse> = await apiClient.get(
        '/api/v1/transfers',
        { params }
      );
      return response.data.data;
    } catch (error) {
      console.error('Get transfers error:', error);
      throw error;
    }
  }

  /**
   * Get specific transfer by ID
   * 
   * @param transferId Transfer ID
   * @returns Promise<Transfer> Transfer details
   */
  static async getTransfer(transferId: number): Promise<Transfer> {
    try {
      const response: AxiosResponse<TransferResponse> = await apiClient.get(
        `/api/v1/transfers/${transferId}`
      );
      return response.data.data;
    } catch (error) {
      console.error('Get transfer error:', error);
      throw error;
    }
  }

  /**
   * Get transfer status
   * 
   * @param transferId Transfer ID
   * @returns Promise<string> Current transfer status
   */
  static async getTransferStatus(transferId: number): Promise<string> {
    try {
      const response: AxiosResponse<{ status: string }> = await apiClient.get(
        `/api/v1/transfers/${transferId}/status`
      );
      return response.data.status;
    } catch (error) {
      console.error('Get transfer status error:', error);
      throw error;
    }
  }

  /**
   * Validate transfer before execution
   * 
   * @param transferData Transfer request data
   * @returns Promise<TransferValidation> Validation result
   */
  static async validateTransfer(transferData: TransferRequest): Promise<TransferValidation> {
    try {
      const response: AxiosResponse<TransferValidation> = await apiClient.post(
        '/api/v1/transfers/validate',
        transferData
      );
      return response.data;
    } catch (error) {
      console.error('Validate transfer error:', error);
      throw error;
    }
  }

  /**
   * Cancel pending transfer
   * 
   * @param transferId Transfer ID
   * @returns Promise<boolean> Cancellation success
   */
  static async cancelTransfer(transferId: number): Promise<boolean> {
    try {
      await apiClient.delete(`/api/v1/transfers/${transferId}`);
      return true;
    } catch (error) {
      console.error('Cancel transfer error:', error);
      throw error;
    }
  }

  /**
   * Get supported virtual banks
   * 
   * @returns Promise<VirtualBank[]> Array of supported banks
   */
  static async getSupportedBanks(): Promise<VirtualBank[]> {
    try {
      const response: AxiosResponse<BankListResponse> = await apiClient.get(
        '/api/v1/transfers/banks'
      );
      return response.data.data;
    } catch (error) {
      console.error('Get banks error:', error);
      throw error;
    }
  }

  /**
   * Get transfer limits for account
   * 
   * @param accountId Account ID
   * @returns Promise<TransferLimits> Transfer limits information
   */
  static async getTransferLimits(accountId: number): Promise<TransferLimits> {
    try {
      const response: AxiosResponse<TransferLimits> = await apiClient.get(
        `/api/v1/accounts/${accountId}/transfer-limits`
      );
      return response.data;
    } catch (error) {
      console.error('Get transfer limits error:', error);
      throw error;
    }
  }
}

/**
 * Convenience functions for common operations
 */

/**
 * Create internal transfer (same bank)
 */
export const createInternalTransfer = async (
  fromAccountId: number,
  toAccountNumber: string,
  amount: number,
  description?: string
): Promise<Transfer> => {
  return TransferAPIService.createTransfer({
    from_account_id: fromAccountId,
    to_account_number: toAccountNumber,
    amount,
    description,
    transfer_type: 'INTERNAL' as any
  });
};

/**
 * Create external transfer (different bank)
 */
export const createExternalTransfer = async (
  fromAccountId: number,
  toAccountNumber: string,
  toBankId: number,
  amount: number,
  description?: string
): Promise<Transfer> => {
  return TransferAPIService.createTransfer({
    from_account_id: fromAccountId,
    to_account_number: toAccountNumber,
    to_bank_id: toBankId,
    amount,
    description,
    transfer_type: 'EXTERNAL' as any
  });
};

/**
 * Poll transfer status until completion
 */
export const pollTransferStatus = async (
  transferId: number,
  maxAttempts: number = 30,
  intervalMs: number = 2000
): Promise<string> => {
  let attempts = 0;
  
  while (attempts < maxAttempts) {
    try {
      const status = await TransferAPIService.getTransferStatus(transferId);
      
      if (status === 'COMPLETED' || status === 'FAILED' || status === 'CANCELLED') {
        return status;
      }
      
      // Wait before next poll
      await new Promise(resolve => setTimeout(resolve, intervalMs));
      attempts++;
    } catch (error) {
      console.error('Poll transfer status error:', error);
      attempts++;
      
      if (attempts >= maxAttempts) {
        throw error;
      }
      
      // Wait before retry
      await new Promise(resolve => setTimeout(resolve, intervalMs));
    }
  }
  
  throw new Error('Transfer status polling timeout');
};

/**
 * Error handling utilities
 */
export const isApiError = (error: any): error is ApiErrorResponse => {
  return error && typeof error === 'object' && 'success' in error && error.success === false;
};

export const getErrorMessage = (error: any): string => {
  if (isApiError(error)) {
    return error.message || error.error || 'An error occurred';
  }
  
  if (error instanceof Error) {
    return error.message;
  }
  
  return 'An unknown error occurred';
};

// Export the main service
export default TransferAPIService;