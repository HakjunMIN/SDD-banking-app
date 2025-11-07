import { RouteObject } from 'react-router-dom'
import { TransactionHistory } from '../pages/TransactionHistory'
import TransactionsPage from '../pages/TransactionsPage'

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
} as const

// Helper function to build parametric routes
export const buildRoute = {
  transactionsByAccount: (accountId: string | number) => `/transactions/${accountId}`,
}