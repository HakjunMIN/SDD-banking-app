import { RouteObject } from 'react-router-dom'
import { TransactionHistory } from '../pages/TransactionHistory'
import TransactionsPage from '../pages/TransactionsPage'
import TransferPage from '../pages/TransferPage'

// Define application routes
export const routes: RouteObject[] = [
  {
    path: '/',
    element: <TransactionsPage />,
    index: true,
  },
  {
    path: '/transactions',
    element: <TransactionsPage />,
  },
  {
    path: '/transactions/:accountId',
    element: <TransactionsPage />,
  },
  {
    path: '/legacy-transactions',
    element: <TransactionHistory />,
  },
  {
    path: '/transfer',
    element: <TransferPage />,
  },
  // Future routes can be added here
  // {
  //   path: '/dashboard',
  //   element: <Dashboard />,
  // },
  // {
  //   path: '/statistics',
  //   element: <Statistics />,
  // },
]

// Route paths constants for type safety
export const ROUTE_PATHS = {
  HOME: '/',
  TRANSACTIONS: '/transactions',
  TRANSACTION_BY_ACCOUNT: '/transactions/:accountId',
  TRANSFER: '/transfer',
} as const

// Helper function to build parametric routes
export const buildRoute = {
  transactionsByAccount: (accountId: string | number) => `/transactions/${accountId}`,
}