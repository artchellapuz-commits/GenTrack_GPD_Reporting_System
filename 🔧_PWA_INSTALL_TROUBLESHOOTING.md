# 🔧 PWA Install Icon Not Showing - Fix

## Why You Can't See the Install Icon

The install icon won't show on the **landing page**. You need to:

1. **Sign In first**
2. **Go to the Dashboard**
3. **Then** the install icon will appear

---

## ✅ Correct Steps to Install PWA

### Step 1: Sign In
1. Go to `http://localhost:8080`
2. Click **"Sign In"**
3. Enter your credentials
4. Log in

### Step 2: Go to Dashboard
- After login, you'll be on the dashboard
- URL will be: `http://localhost:8080/dashboard`

### Step 3: NOW Look for Install Icon
- The install icon (⊕) should now appear in the address bar
- Click it to install

---

## Alternative Method (Works Immediately)

If you still don't see the install icon, use the **browser menu method**:

### In Chrome:
1. Click the **three dots (⋮)** menu (top right)
2. Hover over **"Save and share"**
3. Click **"Install NPC System..."**
4. Click **"Install"**

### In Edge:
1. Click the **three dots (⋮)** menu (top right)
2. Click **"Apps"**
3. Click **"Install this site as an app"**
4. Click **"Install"**

---

## Why This Happens

PWA install criteria requires:
- ✅ Valid manifest.json
- ✅ Service worker registered
- ✅ User has interacted with the site (logged in)
- ✅ Not on the landing page

The browser only shows the install prompt after you've used the app a bit (like logging in and viewing the dashboard).

---

## Quick Fix Summary

**Don't look for install icon on landing page!**

Instead:
1. Sign in → Dashboard
2. Then look for install icon
3. Or use browser menu method

---

## Still Not Working?

### Check These:

1. **Are you using Chrome or Edge?**
   - Firefox doesn't support PWA installation
   - Use Chrome or Edge

2. **Is the service worker registered?**
   - Press F12 (DevTools)
   - Go to "Application" tab
   - Check "Service Workers"
   - Should say "activated and running"

3. **Clear cache and try again**
   - Press Ctrl+Shift+Delete
   - Clear browsing data
   - Reload page
   - Sign in again

4. **Use the menu method instead**
   - This always works
   - Doesn't require the install icon

---

## Easiest Solution

**Just use the browser menu!**

Chrome: ⋮ → Save and share → Install NPC System
Edge: ⋮ → Apps → Install this site as an app

This works even if the install icon doesn't show!

---

**TL;DR**: Sign in first, then look for install icon. Or just use the browser menu method!
