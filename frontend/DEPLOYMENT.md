# Frontend Deployment Guide

## Quick Deploy Options

### Option 1: Vercel (Recommended - Easiest)

1. **Push to GitHub**
   ```bash
   cd /Users/mark/sentinel/gate-controller
   git add frontend/
   git commit -m "Add Next.js PWA frontend"
   git push
   ```

2. **Deploy on Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repo
   - Set **Root Directory** to `frontend`
   - Add environment variables:
     - `NEXT_PUBLIC_API_URL` = `http://your-pi-ip:8000`
     - `NEXT_PUBLIC_API_KEY` = `your-api-key`
   - Deploy!

3. **Access Your App**
   - Get your Vercel URL (e.g., `https://gate-controller.vercel.app`)
   - Install on mobile devices

**Pros:**
- Automatic HTTPS
- Global CDN
- Easy deployments
- Free tier available
- Automatic builds on push

**Cons:**
- Requires internet
- External service

---

### Option 2: Self-Hosted on Raspberry Pi

Run the frontend on the same Pi as the backend:

1. **Build the app**
   ```bash
   cd /Users/mark/sentinel/gate-controller/frontend
   npm install
   npm run build
   ```

2. **Run with PM2**
   ```bash
   sudo npm install -g pm2
   pm2 start npm --name "gate-frontend" -- start
   pm2 save
   pm2 startup
   ```

3. **Access locally**
   - Open `http://your-pi-ip:3000`

4. **Optional: Add to systemd**
   ```bash
   pm2 startup
   pm2 save
   ```

**Pros:**
- Everything on one device
- No external services
- Works on local network

**Cons:**
- Slower on Pi
- Manual updates

---

### Option 3: Docker

1. **Create Dockerfile**
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

2. **Build and run**
   ```bash
   docker build -t gate-frontend .
   docker run -p 3000:3000 \
     -e NEXT_PUBLIC_API_URL=http://your-pi-ip:8000 \
     -e NEXT_PUBLIC_API_KEY=your-key \
     gate-frontend
   ```

3. **Or use docker-compose**
   ```yaml
   version: '3'
   services:
     frontend:
       build: ./frontend
       ports:
         - "3000:3000"
       environment:
         - NEXT_PUBLIC_API_URL=http://redis:6379
         - NEXT_PUBLIC_API_KEY=${API_KEY}
   ```

**Pros:**
- Easy deployment
- Portable
- Isolated environment

**Cons:**
- Requires Docker
- Larger image size

---

### Option 4: Static Export

Export as static HTML and serve anywhere:

1. **Modify next.config.js**
   ```js
   const withPWA = require('next-pwa')({
     dest: 'public',
   });
   
   module.exports = withPWA({
     output: 'export',
     trailingSlash: true,
     images: {
       unoptimized: true,
     },
   });
   ```

2. **Build static files**
   ```bash
   npm run build
   ```

3. **Serve the `out` directory**
   - Upload to any static host
   - S3 + CloudFront
   - GitHub Pages
   - Nginx/Apache

**Pros:**
- Maximum simplicity
- Cheap hosting
- Fast CDN

**Cons:**
- No server features
- Build-time env only

---

## Environment Variables

### Production Checklist

- [ ] `NEXT_PUBLIC_API_URL` - Your Pi's public URL or local IP
- [ ] `NEXT_PUBLIC_API_KEY` - From `gate_control/config.py`
- [ ] HTTPS enabled (required for PWA)
- [ ] CORS configured on backend

### Security Notes

1. **HTTPS Required for PWA**
   - Use Let's Encrypt
   - Or Vercel/Netlify automatic HTTPS
   - Or Cloudflare tunnel

2. **API Key Protection**
   - Never commit `.env.local`
   - Use environment variables in production
   - Rotate keys if exposed

3. **CORS Configuration**
   Add to your backend (Flask):
   ```python
   from flask_cors import CORS
   CORS(app, origins=['https://your-frontend.vercel.app'])
   ```

---

## Recommended Setup

### For Most Users: Vercel
1. Push code to GitHub
2. Connect to Vercel
3. Set environment variables
4. Deploy
5. Install PWA on mobile

### For Local Network: Self-Hosted on Pi
1. Build and run on Pi
2. Access via local IP
3. Install PWA on devices

### For Advanced Users: Docker
1. Build Docker image
2. Deploy to your server
3. Configure environment

---

## After Deployment

1. **Test the PWA**
   - Open on mobile
   - Install to home screen
   - Test all features

2. **Set up monitoring**
   - Vercel Analytics (free)
   - Google Analytics (optional)

3. **Customize (optional)**
   - Update colors in `tailwind.config.js`
   - Add your logo in `public/icon.svg`
   - Update app name in `manifest.json`

---

## Need Help?

- 📖 [Next.js Docs](https://nextjs.org/docs)
- 📖 [PWA Docs](https://github.com/shadowwalker/next-pwa)
- 📖 [Vercel Docs](https://vercel.com/docs)

---

**Choose your deployment method and follow the steps above!**
