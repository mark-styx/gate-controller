# Gate Controller Frontend

A modern, installable Progressive Web App (PWA) for controlling your garage gate from anywhere.

![Next.js](https://img.shields.io/badge/Next.js-14-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC)
![PWA](https://img.shields.io/badge/PWA-Ready-green)

## ✨ Features

- 🚗 **Gate Control** - Activate your gate with one tap
- ⚠️ **Emergency Brake** - Engage/release e-brake instantly
- 📊 **Real-time Status** - Live updates every 2 seconds
- 📱 **Installable** - Add to home screen on iOS/Android
- 🎨 **Modern UI** - Beautiful dark mode design
- ⚡ **Fast** - Optimized for performance
- 🔒 **Secure** - API key authentication
- 📴 **Offline Ready** - Works without internet (cached)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
# or
yarn install
# or
pnpm install
```

### 2. Configure Environment

Copy the environment example:

```bash
cp ENV_EXAMPLE.md .env.local
```

Edit `.env.local` and set your API configuration:

```bash
# Your Gate Controller API URL
NEXT_PUBLIC_API_URL=http://your-pi-ip:8000

# Your API key (from gate_control/config.py)
NEXT_PUBLIC_API_KEY=your-api-key-here
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### 4. Build for Production

```bash
npm run build
npm start
```

## 📱 Installation

### On Mobile Devices

1. Open the app in your mobile browser
2. For **iOS Safari**: Tap Share → "Add to Home Screen"
3. For **Android Chrome**: Tap Menu → "Install app"
4. For **Desktop Chrome**: Click install icon in address bar

The app will now appear on your home screen like a native app!

## 🎯 Usage

### Dashboard
- **Door Status**: Shows current state (open/closed/unknown)
- **Motion**: Displays if door is moving
- **E-Brake**: Shows emergency brake status

### Controls
- **Activate Gate**: Opens/closes the gate
- **Engage E-Brake**: Stops all gate movement immediately

### Status Updates
- Auto-refreshes every 2 seconds
- Manual refresh by pulling down
- Real-time feedback on actions

## 🛠️ Development

### Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Custom SVG
- **PWA**: next-pwa

### Project Structure

```
frontend/
├── app/              # Next.js app directory
│   ├── layout.tsx    # Root layout
│   ├── page.tsx      # Main dashboard
│   └── globals.css   # Global styles
├── components/       # React components
├── hooks/            # Custom React hooks
│   └── useGate.ts    # Gate control hooks
├── lib/              # Utilities
│   └── api.ts        # API client
├── public/           # Static assets
│   ├── icons/        # App icons
│   ├── manifest.json # PWA manifest
│   └── screenshots/  # Store screenshots
└── next.config.js    # Next.js config
```

### Available Scripts

```bash
npm run dev       # Start development server
npm run build     # Build for production
npm run start     # Start production server
npm run lint      # Run ESLint
```

## 🚀 Deployment

### Option 1: Vercel (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/gate-controller/tree/main/frontend)

1. Push your code to GitHub
2. Import to Vercel
3. Add environment variables
4. Deploy!

### Option 2: Self-Hosted

Build and serve with any static hosting:

```bash
npm run build
# Serve the .next folder
```

### Option 3: Docker

Create a `Dockerfile`:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Gate Controller API URL | Yes |
| `NEXT_PUBLIC_API_KEY` | API key for authentication | Yes |

### API Requirements

The frontend expects the Gate Controller API to have these endpoints:

- `GET /health` - Health check (no auth)
- `GET /gate/status` - Get gate status (auth required)
- `POST /gate/activate` - Activate gate (auth required)
- `POST /gate/ebrake` - Toggle e-brake (auth required)

## 🎨 Customization

### Theming

Edit `tailwind.config.js` to customize colors:

```js
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      }
    }
  }
}
```

### Refresh Interval

Change status update frequency in `app/page.tsx`:

```tsx
const { status } = useGateStatus(2000); // milliseconds
```

## 📊 Monitoring

### Console Logs

All API calls are logged in development mode.

### Error Tracking

Integrate with Sentry, LogRocket, etc. for production error tracking.

## 🔒 Security

- API key stored in environment variables
- HTTPS required for PWA features
- No sensitive data in localStorage
- CORS properly configured on backend

## 🧪 Testing

```bash
# Run linting
npm run lint

# Type checking
npx tsc --noEmit
```

## 📝 License

MIT

## 🤝 Support

- 📖 [Documentation](../readme.md)
- 🐛 [Issues](https://github.com/your-username/gate-controller/issues)
- 💬 [Discussions](https://github.com/your-username/gate-controller/discussions)

---

**Built with ❤️ for the Gate Controller project**
