# Lead Generation Frontend

A modern React TypeScript frontend for the AI Lead Generation Automation System. This application provides a comprehensive interface for managing leads, campaigns, and automation workflows.

## Features

- **Dashboard**: Real-time analytics and performance metrics
- **Lead Database**: Comprehensive lead management with filtering and search
- **Web Scraping**: Configure and monitor automated lead collection
- **LinkedIn Automation**: Manage LinkedIn outreach campaigns
- **Email Campaigns**: Create and track email marketing campaigns
- **Contact Management**: Organize and manage contact information
- **Interaction Tracking**: Log and monitor all lead interactions
- **Reports & Analytics**: Generate insights and performance reports
- **Automation Workflows**: Configure end-to-end automation processes

## Technology Stack

- **React 18** with TypeScript for type-safe development
- **Vite** for fast development and building
- **Tailwind CSS** for modern, responsive styling
- **Axios** for API communication
- **Lucide React** for consistent iconography
- **Custom Hooks** for state management and API integration

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python backend API running (see backend documentation)

### Installation

1. Clone the repository and navigate to the frontend directory:
```bash
cd lead-generation-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment configuration:
```bash
cp .env.example .env
```

4. Update the `.env` file with your API configuration:
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

5. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Project Structure

```
src/
├── components/           # React components
│   ├── ui/              # Reusable UI components
│   ├── Dashboard.tsx    # Main dashboard
│   └── LeadDatabase.tsx # Lead management
├── hooks/               # Custom React hooks
│   └── useApi.ts       # API integration hooks
├── services/           # API service layer
│   └── api.ts         # API client and endpoints
├── types/             # TypeScript type definitions
│   └── index.ts      # Shared types and interfaces
├── App.tsx           # Main application component
└── main.tsx         # Application entry point
```

## Key Components

### Dashboard
- Real-time metrics and KPIs
- Activity feed and notifications
- Quick action buttons
- Performance charts and analytics

### Lead Database
- Paginated lead listing with search and filters
- Bulk operations (edit, delete, tag)
- Import/export functionality
- Detailed lead profiles

### Data Table
- Reusable table component with sorting and pagination
- Row selection and bulk actions
- Responsive design for mobile devices
- Loading states and error handling

## API Integration

The frontend communicates with the Python backend through a RESTful API. Key features:

- **Automatic retry logic** for failed requests
- **Loading states** and error handling
- **Optimistic updates** for better UX
- **Real-time polling** for live data
- **Batch operations** for bulk actions

### Custom Hooks

- `useApi`: Basic API call management
- `usePaginatedApi`: Paginated data handling
- `usePolling`: Real-time data updates
- `useOptimisticApi`: Optimistic UI updates
- `useBatchApi`: Bulk operation handling

## Styling and Design

The application uses Tailwind CSS with a custom design system:

- **Consistent color palette** with primary, secondary, and semantic colors
- **Responsive breakpoints** for mobile-first design
- **Custom components** with hover states and transitions
- **Dark mode support** (configurable)
- **Accessibility features** with proper ARIA labels

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler

### Code Quality

- **TypeScript** for type safety
- **ESLint** for code linting
- **Prettier** for code formatting
- **Consistent naming conventions**
- **Component documentation**

## Deployment

### Production Build

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

### Environment Variables

Configure the following environment variables for production:

```env
VITE_API_BASE_URL=https://your-api-domain.com/api
VITE_APP_NAME=Lead Generation Suite
VITE_APP_VERSION=1.0.0
```

### Deployment Options

- **Netlify**: Connect your repository for automatic deployments
- **Vercel**: Zero-configuration deployment
- **AWS S3 + CloudFront**: For enterprise deployments
- **Docker**: Containerized deployment

## Backend Integration

This frontend is designed to work with the Python backend API. Ensure the backend is running and accessible at the configured API URL.

### Required Backend Endpoints

- `GET /api/leads` - Lead listing with pagination
- `POST /api/leads` - Create new lead
- `PUT /api/leads/:id` - Update lead
- `DELETE /api/leads/:id` - Delete lead
- `GET /api/analytics/leads` - Lead statistics
- `POST /api/scraping/start` - Start web scraping
- `GET /api/email/campaigns` - Email campaigns
- `POST /api/linkedin/automation/start` - LinkedIn automation

## Contributing

1. Follow the existing code style and conventions
2. Add TypeScript types for all new features
3. Include proper error handling and loading states
4. Test components thoroughly before submitting
5. Update documentation for new features

## Support

For issues and questions:

1. Check the backend API is running and accessible
2. Verify environment variables are configured correctly
3. Check browser console for error messages
4. Review network requests in developer tools

## License

This project is part of the AI Lead Generation Automation System.