# 📱 How to Use the PWA (Progressive Web App)

## What is a PWA?

A Progressive Web App (PWA) lets you install the NPC Reporting System on your device like a native app. It works on phones, tablets, and computers!

---

## 🎯 Benefits of Using PWA

1. **📲 Install on Home Screen** - Quick access like a native app
2. **⚡ Faster Loading** - Cached resources load instantly
3. **🔌 Works Offline** - Access some features without internet
4. **📱 Native Feel** - Full screen, no browser UI
5. **💾 Less Storage** - Smaller than native apps
6. **🔄 Auto Updates** - Always get the latest version

---

## 📱 How to Install on Mobile (Android/iOS)

### Android (Chrome, Edge, Samsung Internet)

#### Method 1: Install Prompt Banner
1. Open your mobile browser (Chrome recommended)
2. Go to: `http://your-server-ip:8080` or your domain
3. Log in to the system
4. Look for the **"Install App"** banner at the top
   ```
   ┌─────────────────────────────────────┐
   │ 📱 Install NPC System               │
   │ Install this app for quick access   │
   │ [Install] [✕]                       │
   └─────────────────────────────────────┘
   ```
5. Click **"Install"**
6. Confirm installation
7. App icon appears on your home screen!

#### Method 2: Browser Menu
1. Open the website in Chrome
2. Tap the **⋮** (three dots) menu
3. Select **"Add to Home screen"** or **"Install app"**
4. Name the app (default: "NPC System")
5. Tap **"Add"** or **"Install"**
6. Done! Icon is now on your home screen

### iOS (Safari)

**Note**: iOS has limited PWA support, but you can still add to home screen:

1. Open Safari browser
2. Go to the website
3. Tap the **Share** button (square with arrow)
4. Scroll down and tap **"Add to Home Screen"**
5. Name the app
6. Tap **"Add"**
7. Icon appears on home screen

**iOS Limitations**:
- No install prompt banner
- Limited offline features
- No push notifications
- Must use Safari (not Chrome)

---

## 💻 How to Install on Desktop (Windows/Mac/Linux)

### Chrome, Edge, Brave

#### Method 1: Install Button
1. Open the website in Chrome/Edge
2. Look for the **install icon** (⊕) in the address bar
   ```
   https://your-site.com  [⊕]
   ```
3. Click the install icon
4. Click **"Install"** in the popup
5. App opens in its own window
6. Shortcut added to desktop/start menu

#### Method 2: Browser Menu
1. Click the **⋮** (three dots) menu
2. Select **"Install NPC System..."**
3. Click **"Install"**
4. App opens in standalone window

### Firefox
Firefox doesn't support PWA installation, but you can:
1. Bookmark the site
2. Use it in the browser normally

---

## 🚀 Using the Installed PWA

### Opening the App

**Mobile**:
- Tap the app icon on your home screen
- Opens full screen (no browser UI)

**Desktop**:
- Click the desktop shortcut
- Or find it in Start Menu (Windows) / Applications (Mac)
- Opens in its own window

### Features Available

✅ **All regular features work**:
- Dashboard
- Upload Excel
- View Reports
- Generate Reports
- Water Nomination
- User Management
- Advanced Analytics
- Automated Reports

✅ **Additional PWA features**:
- Faster loading (cached resources)
- Works offline (limited)
- Full screen experience
- Native app feel

### Offline Capabilities

**What works offline**:
- Previously viewed pages (cached)
- Static resources (CSS, JS, images)
- Service worker keeps running

**What needs internet**:
- Loading new data
- Uploading files
- Generating reports
- API calls

---

## 🔧 Managing the Installed PWA

### Updating the App

**Automatic Updates**:
- PWA checks for updates automatically
- New version downloads in background
- Refresh page to get latest version

**Manual Update**:
1. Close the app completely
2. Reopen it
3. New version loads automatically

### Uninstalling the PWA

#### Android
1. Long press the app icon
2. Select **"App info"** or **"Uninstall"**
3. Tap **"Uninstall"**

Or:
1. Go to Settings → Apps
2. Find "NPC System"
3. Tap **"Uninstall"**

#### iOS
1. Long press the app icon
2. Tap **"Remove App"**
3. Confirm **"Delete"**

#### Desktop (Chrome/Edge)
1. Open the PWA
2. Click **⋮** (three dots) in the app window
3. Select **"Uninstall NPC System..."**
4. Confirm uninstall

Or:
1. Go to `chrome://apps` (Chrome) or `edge://apps` (Edge)
2. Right-click the app
3. Select **"Remove from Chrome/Edge"**

---

## 🎨 PWA Features Explained

### Install Prompt Banner

The banner appears when:
- ✅ You visit the site on mobile
- ✅ Site is served over HTTPS (or localhost)
- ✅ Service worker is registered
- ✅ Manifest file is valid
- ✅ You haven't dismissed it recently

You can:
- **Install**: Adds app to home screen
- **✕ Dismiss**: Hides banner (shows again later)

### Service Worker

**What it does**:
- Caches files for offline use
- Speeds up page loading
- Enables background sync
- Handles network requests

**Cache Strategy**:
- Network-first: Try internet, fallback to cache
- Ensures you always get fresh data when online

### App Manifest

**Defines**:
- App name: "NPC System"
- Theme color: Blue (#003d82)
- Display mode: Standalone (full screen)
- Start URL: Your homepage
- Icons: App icons (need to be created)

---

## 🔍 Troubleshooting

### Install Prompt Not Showing

**Check**:
1. Are you using Chrome/Edge on Android?
2. Is the site served over HTTPS? (or localhost)
3. Have you dismissed it recently? (wait 3 months)
4. Is service worker registered? (check DevTools)

**Solution**:
- Use browser menu method instead
- Check browser console for errors

### App Not Working Offline

**Remember**:
- Only cached pages work offline
- API calls need internet
- First visit must be online

**Solution**:
- Visit pages while online to cache them
- Check service worker status in DevTools

### App Not Updating

**Solution**:
1. Close app completely
2. Clear browser cache
3. Reopen app
4. Hard refresh (Ctrl+Shift+R)

### Icons Not Showing

**Current Status**:
- Icons are placeholders
- Need to create actual icons

**To Fix**:
1. Create 192x192 and 512x512 PNG icons
2. Save to `frontend/public/icons/`
3. Update `manifest.json`

---

## 📊 Checking PWA Status

### Chrome DevTools

1. Open the website
2. Press **F12** (DevTools)
3. Go to **Application** tab
4. Check:
   - **Manifest**: Should show app details
   - **Service Workers**: Should be "activated and running"
   - **Cache Storage**: Should show cached files

### Lighthouse Audit

1. Open DevTools (F12)
2. Go to **Lighthouse** tab
3. Select **Progressive Web App**
4. Click **Generate report**
5. See PWA score and recommendations

---

## 🎯 Best Practices

### For Users

1. **Install on mobile** for best experience
2. **Visit pages while online** to cache them
3. **Keep app updated** by reopening regularly
4. **Use full screen** for native app feel

### For Field Users

Perfect for:
- 📱 Quick access on mobile
- 🏗️ Working at plant sites
- 📊 Checking reports on the go
- ⚡ Fast loading on slow networks

---

## 📝 Quick Reference

### Installation Methods

| Platform | Method 1 | Method 2 |
|----------|----------|----------|
| Android | Install banner | Browser menu |
| iOS | - | Share → Add to Home Screen |
| Desktop | Install icon in address bar | Browser menu |

### Browser Support

| Browser | Mobile | Desktop | Install |
|---------|--------|---------|---------|
| Chrome | ✅ | ✅ | ✅ |
| Edge | ✅ | ✅ | ✅ |
| Safari | ⚠️ Limited | ⚠️ Limited | ❌ |
| Firefox | ✅ Browse only | ✅ Browse only | ❌ |
| Samsung Internet | ✅ | - | ✅ |

### Key Features

- ✅ Install on home screen
- ✅ Full screen mode
- ✅ Offline caching
- ✅ Fast loading
- ✅ Auto updates
- ⚠️ Push notifications (not yet implemented)
- ⚠️ Background sync (not yet implemented)

---

## 🚀 Next Steps

### For Users
1. Install the PWA on your device
2. Use it like a native app
3. Enjoy faster loading and offline access

### For Developers
1. Create actual app icons (192x192, 512x512)
2. Test on different devices
3. Add push notifications
4. Implement background sync
5. Improve offline capabilities

---

## 📞 Need Help?

**PWA not working?**
1. Check browser compatibility
2. Verify HTTPS/localhost
3. Clear cache and try again
4. Use browser menu method

**Still having issues?**
- Check browser console for errors
- Verify service worker is registered
- Test on different browser/device

---

**Enjoy your mobile-first NPC Reporting System! 📱⚡**
