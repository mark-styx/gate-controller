# Frontend Quick Start Guide

Get your Gate Controller frontend running in 5 minutes!

## 🚀 Quick Setup (3 steps)

### 1. Install Dependencies (2 min)
```bash
cd /Users/mark/sentinel/gate-controller/frontend
npm install
```

### 2. Configure (1 min)
```bash
# Copy example config
cp .env.local.example .env.local

# Edit with your settings
nano .env.local
```

Add your API details:
```bash
NEXT_PUBLIC_API_URL=http://YOUR_PI_IP:8000
NEXT_PUBLIC_API_KEY=your-api-key-here
```

**Get your API key:**
```bash
cd /Users/mark/sentinel/gate-controller
./gate.sh key
```

### 3. Run (30 sec)
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser!

---

## 📱 Install as PWA

### On iPhone/iPad:
1. Open Safari
2. Go to your app URL
3. Tap Share button (square with arrow)
4. Tap "Add to Home Screen"
5. Name it and tap "Add"

### On Android:
1. Open Chrome
2. Go to your app URL
3. Tap menu (three dots)
4. Tap "Install app" or "Add to Home screen"

### On Desktop (Chrome/Edge):
1. Go to your app URL
2. Look for install icon in address bar
3. Click "Install"

---

## 🎯 Features

- **Real-time Status** - Updates every 2 seconds
- **One-tap Control** - Activate gate instantly
- **Emergency Brake** - Stop gate immediately
- **Health Monitoring** - System status at a glance
- **Mobile Optimized** - Works perfectly on phones
- **Offline Support** - Cached for offline use
- **Dark Mode** - Easy on the eyes

---

## 🛠️ Development Commands

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type checking
npx tsc --noEmit

# Lint code
npm run lint
```

---

## 📂 Project Structure

```
frontend/
├── app/                  # Pages (Next.js 14 App Router)
│   ├── page.tsx         # Home dashboard
│   ├── layout.tsx       # Root layout
│   ├── globals.css      # Global styles
│   └── settings/        # Settings page
├── components/          # React components
├── hooks/              # Custom hooks
│   └── useGate.ts      # Gate control hooks
├── lib/                # Utilities
│   └── api.ts          # API client
├── public/             # Static files
│   ├── icon.svg        # App icon
│   └── manifest.json   # PWA manifest
└── package.json        # Dependencies
```

---

## 🌐 Deployment

### Easiest: Vercel (Recommended)
```bash
# Push to GitHub
git add frontend/
git commit -m "Add frontend"
git push

# Deploy on Vercel
# 1. Import GitHub repo
# 2. Set Root Directory: frontend
# 3. Add env vars
# 4. Deploy
```

### Self-Hosted: Run on Pi
```bash
npm run build
pm2 start npm --name "gate-frontend" -- start
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for all options.

---

## 🔧 Customization

### Change Colors
Edit `tailwind.config.js`:
```js
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
        500: '#your-color',
      }
    }
  }
}
```

### Change App Name
Edit `public/manifest.json`:
```json
{
  "name": "Your Gate Controller",
  "short_name": "YourGate"
}
```

### Update Status Interval
Edit `app/page.tsx`:
```tsx
const { status } = useGateStatus(5000); // 5 seconds
```

---

## 🐛 Troubleshooting

### "Failed to fetch"
- Check API is running: `./gate.sh status`
- Verify API URL in `.env.local`
- Check API key is correct

### "CORS error"
Add to your Flask backend:
```python
from flask_cors import CORS
CORS(app)
```

### "PWA won't install"
- Must use HTTPS (or localhost)
- Clear browser cache
- Check manifest.json is valid

### "Slow on Pi"
- Use `npm run build && npm start` (not dev)
- Or deploy to Vercel instead

---

## 📊 Architecture

```
┌─────────────┐         ┌──────────────┐
│   Browser   │         │  Raspberry   │
│   (PWA)     │         │     Pi       │
├─────────────┤         ├──────────────┤
│             │  HTTP   │              │
│  Next.js    ├────────►│  Flask API   │
│  Frontend   │         │  (gate_api)  │
│             │         │              │
│  localhost  │         │   Redis      │
│  :3000      │         │              │
└─────────────┘         └──────────────┘
                              │
                              ▼
                        ┌──────────┐
                        │   GPIO   │
                        │  Relays  │
                        └──────────┘
```

---

## ✅ Next Steps

1. [ ] Test all features (status, activate, ebrake)
2. [ ] Install PWA on your phone
3. [ ] Set up for family members
4. [ ] Configure alerts (optional)
5. [ ] Deploy to production (Vercel recommended)

---

## 🆘 Need Help?

- 📖 [Full README](./README.md)
- 🚀 [Deployment Guide](./DEPLOYMENT.md)
- 🐛 [Issues](https://github.com/your-username/gate-controller/issues)

---

**You're all set! Run `npm run dev` and start controlling your gate! 🎉**
