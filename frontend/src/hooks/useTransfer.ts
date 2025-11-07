/**
 * useTransfer Hook
 * Custom hook for managing transfer state and operations
 */

import { useState, useCallback } from 'react';
import { Transfer, TransferRequest, TransferStatus } from '../types/transfer';
import { TransferAPIService, createInternalTransfer, getErrorMessage, isApiError } from '../services/transferAPI';

interface TransferState {
  transfers: Transfer[];
  currentTransfer: Transfer | null;
  isLoading: boolean;
  isSubmitting: boolean;
  error: string | null;
  lastCreatedTransfer: Transfer | null;
}

interface UseTransferReturn {
  // State
  transfers: Transfer[];
  currentTransfer: Transfer | null;
  isLoading: boolean;
  isSubmitting: boolean;
  error: string | null;
  lastCreatedTransfer: Transfer | null;
  
  // Actions
  createTransfer: (transferData: TransferRequest) => Promise<Transfer>;
  getTransfers: (accountId: number, status?: TransferStatus) => Promise<Transfer[]>;
  getTransferById: (transferId: number) => Promise<Transfer | null>;
  refreshTransfers: (accountId: number) => Promise<void>;
  clearError: () => void;
  clearLastTransfer: () => void;
  
  // Utilities
  getTransfersByStatus: (status: TransferStatus) => Transfer[];
  getTotalTransferAmount: () => number;
}

export const useTransfer = (): UseTransferReturn => {
  const [state, setState] = useState<TransferState>({
    transfers: [],
    currentTransfer: null,
    isLoading: false,
    isSubmitting: false,
    error: null,
    lastCreatedTransfer: null
  });

  const setLoading = useCallback((isLoading: boolean) => {
    setState(prev => ({ ...prev, isLoading }));
  }, []);

  const setSubmitting = useCallback((isSubmitting: boolean) => {
    setState(prev => ({ ...prev, isSubmitting }));
  }, []);

  const setError = useCallback((error: string | null) => {
    setState(prev => ({ ...prev, error }));
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, [setError]);

  const clearLastTransfer = useCallback(() => {
    setState(prev => ({ ...prev, lastCreatedTransfer: null }));
  }, []);

  /**
   * Create a new transfer
   */
  const createTransfer = useCallback(async (transferData: TransferRequest): Promise<Transfer> => {
    setSubmitting(true);
    setError(null);

    try {
      let transfer: Transfer;
      
      if (transferData.transfer_type === 'INTERNAL' || !transferData.to_bank_id) {
        // Internal transfer
        transfer = await createInternalTransfer(
          transferData.from_account_id,
          transferData.to_account_number,
          transferData.amount,
          transferData.description
        );
      } else {
        // External transfer (not implemented in Phase 3)
        throw new Error('External transfers not implemented yet');
      }

      setState(prev => ({
        ...prev,
        transfers: [transfer, ...prev.transfers],
        lastCreatedTransfer: transfer,
        currentTransfer: transfer
      }));

      return transfer;

    } catch (error) {
      const errorMessage = getErrorMessage(error);
      setError(errorMessage);
      throw error;
    } finally {
      setSubmitting(false);
    }
  }, [setSubmitting, setError]);

  /**
   * Get transfers for an account
   */
  const getTransfers = useCallback(async (
    accountId: number, 
    status?: TransferStatus
  ): Promise<Transfer[]> => {
    setLoading(true);
    setError(null);

    try {
      const transfers = await TransferAPIService.getTransfers({
        account_id: accountId,
        status,
        limit: 50,
        offset: 0
      });

      setState(prev => ({
        ...prev,
        transfers
      }));

      return transfers;

    } catch (error) {
      const errorMessage = getErrorMessage(error);
      setError(errorMessage);
      return [];
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError]);

  /**
   * Get a specific transfer by ID
   */
  const getTransferById = useCallback(async (transferId: number): Promise<Transfer | null> => {
    setLoading(true);
    setError(null);

    try {
      const transfer = await TransferAPIService.getTransfer(transferId);
      
      setState(prev => ({
        ...prev,
        currentTransfer: transfer
      }));

      return transfer;

    } catch (error) {
      if (isApiError(error) && error.message.includes('not found')) {
        setError('Transfer not found');
      } else {
        const errorMessage = getErrorMessage(error);
        setError(errorMessage);
      }
      return null;
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError]);

  /**
   * Refresh transfers for an account
   */
  const refreshTransfers = useCallback(async (accountId: number): Promise<void> => {
    await getTransfers(accountId);
  }, [getTransfers]);

  /**
   * Filter transfers by status
   */
  const getTransfersByStatus = useCallback((status: TransferStatus): Transfer[] => {
    return state.transfers.filter(transfer => transfer.status === status);
  }, [state.transfers]);

  /**
   * Calculate total transfer amount
   */
  const getTotalTransferAmount = useCallback((): number => {
    return state.transfers
      .filter(transfer => transfer.status === TransferStatus.COMPLETED)
      .reduce((total, transfer) => total + transfer.amount, 0);
  }, [state.transfers]);

  return {
    // State
    transfers: state.transfers,
    currentTransfer: state.currentTransfer,
    isLoading: state.isLoading,
    isSubmitting: state.isSubmitting,
    error: state.error,
    lastCreatedTransfer: state.lastCreatedTransfer,
    
    // Actions
    createTransfer,
    getTransfers,
    getTransferById,
    refreshTransfers,
    clearError,
    clearLastTransfer,
    
    // Utilities
    getTransfersByStatus,
    getTotalTransferAmount
  };
};

export default useTransfer;