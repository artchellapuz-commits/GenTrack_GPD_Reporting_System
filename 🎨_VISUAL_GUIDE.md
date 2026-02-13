# 🎨 Visual Guide - Priority 1 Features

## What You'll See When You Test

---

## 1. Login Page 🔐

```
┌─────────────────────────────────────────┐
│                                         │
│              [⚡ Logo]                  │
│        NPC Reporting System             │
│   Agus Hydroelectric Power Plants       │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │ 👤 Username                       │  │
│  │ [Enter your username_______]      │  │
│  │                                   │  │
│  │ 🔒 Password                       │  │
│  │ [Enter your password_______] 👁   │  │
│  │                                   │  │
│  │ [        Login        ]           │  │
│  │                                   │  │
│  │ Don't have an account?            │  │
│  │ Register here                     │  │
│  └───────────────────────────────────┘  │
│                                         │
│  © 2026 National Power Corporation      │
└─────────────────────────────────────────┘
```

**Features**:
- Beautiful gradient background (purple-blue)
- Show/hide password toggle
- Error messages display below password
- Loading state when submitting
- Auto-redirect to dashboard on success

---

## 2. Register Page 📝

```
┌─────────────────────────────────────────┐
│                                         │
│              [⚡ Logo]                  │
│          Create Account                 │
│      Join NPC Reporting System          │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │ First Name    │  Last Name        │  │
│  │ [John____]    │  [Doe_____]       │  │
│  │                                   │  │
│  │ Username                          │  │
│  │ [johndoe___________________]      │  │
│  │                                   │  │
│  │ Email                             │  │
│  │ [john@example.com__________]      │  │
│  │                                   │  │
│  │ Password                          │  │
│  │ [••••••••••••••••••••••••]        │  │
│  │ At least 8 characters             │  │
│  │                                   │  │
│  │ Confirm Password                  │  │
│  │ [••••••••••••••••••••••••]        │  │
│  │                                   │  │
│  │ [    Create Account    ]          │  │
│  │                                   │  │
│  │ Already have an account?          │  │
│  │ Login here                        │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Features**:
- Two-column layout for name fields
- Email validation
- Password confirmation
- Error messages for validation
- Auto-login after registration

---

## 3. Dashboard with Header 📊

```
┌─────────────────────────────────────────────────────────────┐
│ [NPC Logo] NPC Reporting System                             │
│            Agus-Pulangi Hydro-Electric Power Plants         │
│                                                             │
│  [Dashboard] [Upload] [Reports] [Generate]    👤 John [Logout]│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     Dashboard                               │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ 📊 Total │  │ ⚡ Active│  │ 📈 Avg   │  │ 📅 Last  │   │
│  │ 1,234 MW │  │ 6 Plants │  │ 85% CF   │  │ Updated  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Generation Trend                                    │   │
│  │ [7 Days] [30 Days] [90 Days] [All]                 │   │
│  │                                                     │   │
│  │     MW                                              │   │
│  │  300 ┤     ╱╲                                       │   │
│  │  250 ┤    ╱  ╲    ╱╲                                │   │
│  │  200 ┤   ╱    ╲  ╱  ╲                               │   │
│  │  150 ┤  ╱      ╲╱    ╲                              │   │
│  │  100 ┤ ╱              ╲                             │   │
│  │   50 ┤╱                ╲                            │   │
│  │    0 └────────────────────────────────              │   │
│  │      Jan  Feb  Mar  Apr  May  Jun                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Capacity Factor by Plant                            │   │
│  │                                                     │   │
│  │  100% ┤                                             │   │
│  │   80% ┤ ███  ███  ███  ███  ███  ███               │   │
│  │   60% ┤ ███  ███  ███  ███  ███  ███               │   │
│  │   40% ┤ ███  ███  ███  ███  ███  ███               │   │
│  │   20% ┤ ███  ███  ███  ███  ███  ███               │   │
│  │    0% └─────────────────────────────                │   │
│  │       AG1  AG2  AG4  AG5  AG6  AG7                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ © 2026 National Power Corporation. All rights reserved.     │
│ Help • Documentation • Contact                              │
└─────────────────────────────────────────────────────────────┘
```

**Features**:
- Sticky header with navigation
- User menu with name and logout
- Summary cards with icons
- Interactive line chart
- Bar chart for comparison
- Responsive footer

---

## 4. Mobile View (Phone) 📱

```
┌─────────────────────┐
│ [☰] NPC Reporting   │
│     System          │
├─────────────────────┤
│                     │
│  ┌───────────────┐  │
│  │ 📊 Total      │  │
│  │ 1,234 MW      │  │
│  └───────────────┘  │
│                     │
│  ┌───────────────┐  │
│  │ ⚡ Active     │  │
│  │ 6 Plants      │  │
│  └───────────────┘  │
│                     │
│  ┌───────────────┐  │
│  │ Generation    │  │
│  │ Trend         │  │
│  │               │  │
│  │   ╱╲          │  │
│  │  ╱  ╲         │  │
│  │ ╱    ╲        │  │
│  └───────────────┘  │
│                     │
│  ┌───────────────┐  │
│  │ Capacity      │  │
│  │ Factor        │  │
│  │               │  │
│  │ ███ ███ ███   │  │
│  │ AG1 AG2 AG4   │  │
│  └───────────────┘  │
│                     │
└─────────────────────┘
```

**Features**:
- Hamburger menu for navigation
- Stacked layout (single column)
- Touch-friendly buttons
- Optimized chart sizes
- Readable text on small screens

---

## 5. Tablet View (iPad) 📱

```
┌─────────────────────────────────────────┐
│ [NPC Logo] NPC Reporting System         │
│                                         │
│ [Dashboard] [Upload] [Reports] [Generate]│
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │ 📊 Total │  │ ⚡ Active│            │
│  │ 1,234 MW │  │ 6 Plants │            │
│  └──────────┘  └──────────┘            │
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │ 📈 Avg   │  │ 📅 Last  │            │
│  │ 85% CF   │  │ Updated  │            │
│  └──────────┘  └──────────┘            │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Generation Trend                │   │
│  │                                 │   │
│  │     ╱╲                          │   │
│  │    ╱  ╲    ╱╲                   │   │
│  │   ╱    ╲  ╱  ╲                  │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Capacity Factor                 │   │
│  │                                 │   │
│  │ ███  ███  ███  ███  ███  ███    │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Features**:
- Two-column grid for cards
- Full-width charts
- Compact navigation
- Optimized spacing

---

## 🎨 Color Scheme

### Primary Colors
- **Purple-Blue**: `#667eea` - Main brand color
- **Deep Purple**: `#764ba2` - Accent color
- **White**: `#ffffff` - Background

### Status Colors
- **Success**: `#10b981` (Green) - Successful operations
- **Warning**: `#f59e0b` (Orange) - Warnings
- **Error**: `#ef4444` (Red) - Errors
- **Info**: `#3b82f6` (Blue) - Information

### Neutral Colors
- **Gray 50**: `#f9fafb` - Light background
- **Gray 400**: `#9ca3af` - Secondary text
- **Gray 900**: `#111827` - Dark text

---

## 🔄 User Flow

### First Time User
```
1. Open http://localhost:8081
   ↓
2. Redirected to /login
   ↓
3. Click "Register here"
   ↓
4. Fill registration form
   ↓
5. Auto-login after registration
   ↓
6. Redirected to /dashboard
   ↓
7. See charts and data
```

### Returning User
```
1. Open http://localhost:8081
   ↓
2. Redirected to /login
   ↓
3. Enter username/password
   ↓
4. Click "Login"
   ↓
5. Redirected to /dashboard
   ↓
6. Navigate using header menu
```

### Logout Flow
```
1. Click "Logout" button
   ↓
2. Token is blacklisted
   ↓
3. Local storage cleared
   ↓
4. Redirected to /login
```

---

## 📱 Responsive Breakpoints

### Desktop (1024px+)
- Full navigation bar
- Multi-column layouts
- Large charts
- Sidebar support

### Tablet (768px - 1023px)
- Compact navigation
- Two-column grids
- Medium charts
- Optimized spacing

### Mobile (480px - 767px)
- Hamburger menu
- Single column
- Stacked layouts
- Touch-friendly

### Small Mobile (< 480px)
- Minimal navigation
- Full-width elements
- Larger touch targets
- Simplified layouts

---

## 🎯 Interactive Elements

### Buttons
- **Primary**: Purple gradient, white text
- **Secondary**: White background, purple border
- **Danger**: Red background, white text
- **Hover**: Slight lift effect (translateY)
- **Active**: Pressed effect

### Forms
- **Focus**: Blue border, subtle shadow
- **Error**: Red border, error message below
- **Success**: Green border, checkmark
- **Disabled**: Gray background, no interaction

### Charts
- **Hover**: Tooltip with details
- **Click**: Select data point
- **Zoom**: Pinch on mobile
- **Pan**: Drag on desktop

---

## 💡 Tips for Testing

1. **Test All Breakpoints**
   - Use Chrome DevTools (F12)
   - Toggle device toolbar (Ctrl+Shift+M)
   - Try different devices

2. **Test Authentication**
   - Register new user
   - Login/logout
   - Try wrong password
   - Check token refresh

3. **Test Charts**
   - Hover over data points
   - Change time ranges
   - Check responsiveness
   - Verify data accuracy

4. **Test Navigation**
   - Click all menu items
   - Check active states
   - Test back button
   - Verify redirects

---

**Ready to test!** 🚀

Open http://localhost:8081 and explore the new features!
