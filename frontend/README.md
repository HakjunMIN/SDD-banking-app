# Banking App Frontend

React frontend application for the Banking App transaction history feature.

## Tech Stack

- **React 18** - Frontend framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

3. Open browser to [http://localhost:3000](http://localhost:3000)

### Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test

# Run tests in watch mode
npm run test:watch

# Generate test coverage
npm run test:coverage

# Lint code
npm run lint
```

## Project Structure

```
frontend/
├── public/                # Static assets
├── src/
│   ├── components/        # Reusable UI components
│   │   └── Layout.tsx     # Main layout component
│   ├── pages/             # Page components
│   │   └── TransactionHistory.tsx
│   ├── services/          # API service functions
│   ├── types/             # TypeScript type definitions
│   ├── hooks/             # Custom React hooks
│   ├── App.tsx            # Main app component
│   ├── main.tsx           # App entry point
│   └── index.css          # Global styles
├── tailwind.config.js     # Tailwind CSS configuration
├── vite.config.ts         # Vite configuration
├── tsconfig.json          # TypeScript configuration
└── package.json           # Dependencies and scripts
```

## Features

- **Transaction History View** - Display list of banking transactions
- **Responsive Design** - Works on desktop and mobile devices
- **API Integration** - Connects to FastAPI backend
- **Type Safety** - Full TypeScript support
- **Modern UI** - Clean design with Tailwind CSS

## API Integration

The frontend connects to the backend API running on `http://localhost:8000`. API proxy is configured in `vite.config.ts` to route `/api` requests to the backend.

## Styling

This project uses Tailwind CSS with custom color palette:
- Primary: Blue tones for main actions
- Secondary: Gray tones for supporting elements  
- Success: Green for positive transactions
- Warning: Orange for alerts
- Error: Red for negative transactions or errors