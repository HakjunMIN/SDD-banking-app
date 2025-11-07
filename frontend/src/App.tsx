import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { routes } from './routes/index'
import { Layout } from './components/Layout.tsx'

// Create router with layout wrapper
const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: routes,
  },
])

function App() {
  return <RouterProvider router={router} />
}

export default App