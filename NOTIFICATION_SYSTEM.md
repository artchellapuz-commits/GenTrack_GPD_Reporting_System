# Notification System

## Overview
The notification system displays a bell icon in the navbar for administrators with a dropdown panel showing recent password reset requests.

## Features

### 1. Notification Bell Icon
- Located in the top navbar (AppLayout component)
- Only visible to administrators
- Shows a red badge with the count of pending requests
- Badge pulses to draw attention when there are pending requests
- Clicking the bell opens a dropdown notification panel

### 2. Notification Dropdown Panel
- Shows up to 5 most recent pending password reset requests
- Displays username, request time, and quick preview
- Click on any notification to go to the full Password Reset Requests page
- Automatically scrolls to and highlights the clicked request row
- Highlight animation lasts for 5 seconds with a golden/yellow glow
- "View All Requests" link at the bottom for full list
- Empty state when no pending requests

### 3. Real-time Updates
- Automatically polls the backend every 30 seconds for updates
- Immediately refreshes when a request is processed (approved/rejected/completed)
- Uses custom events to communicate between components
- Loads recent requests when dropdown is opened

### 3. Backend API Endpoint
**Endpoint:** `GET /api/auth/pending_reset_count/`

**Response:**
```json
{
  "count": 5
}
```

**Access:** Admin users only (returns 0 for non-admin users)

## Implementation Details

### Frontend Components

#### AppLayout.vue
- Displays the notification bell icon
- Manages the notification count state
- Polls the API every 30 seconds
- Listens for `password-reset-processed` custom events

**Key Methods:**
- `loadPendingResetCount()` - Fetches the current count from API
- `loadRecentRequests()` - Fetches the 5 most recent pending requests
- `toggleNotificationMenu()` - Opens/closes the notification dropdown
- `viewRequest(request)` - Navigates to requests page with highlight query parameter
- `viewAllRequests()` - Navigates to requests page from "View All" link
- `formatTimeAgo(dateString)` - Formats timestamps as relative time (e.g., "5 minutes ago")
- `handlePasswordResetProcessed()` - Refreshes count when requests are processed

#### PasswordResetRequests.vue
- Dispatches `password-reset-processed` event after processing requests
- Triggers notification refresh in parent component
- Handles row highlighting when navigated from notification

**Key Methods:**
- `notifyParentToRefresh()` - Dispatches custom event to update notification count
- `scrollToHighlightedRow()` - Scrolls to and highlights the specified request row
- Automatically removes highlight after 5 seconds

**Highlight System:**
- Uses route query parameter `?highlight=<request_id>` to identify which row to highlight
- Adds unique ID to each table row: `request-row-{id}`
- Applies `highlighted-row` CSS class for animation
- Smooth scroll to center the row in viewport
- Golden/yellow glow animation that fades over 5 seconds
- Left border accent bar that fades out
- Automatically cleans up query parameter after animation

### Backend Implementation

#### auth_views.py
**New Action:** `pending_reset_count`
- Returns count of password reset requests with status='PENDING'
- Admin-only access
- Returns 0 for non-admin users

## Visual Design

### Notification Dropdown
- Width: 380px (responsive on mobile)
- Max height: 500px with scrollable content
- Border radius: 12px
- Shadow: Elevated with soft shadow
- Header: Shows title and pending count badge
- Body: Scrollable list of notifications
- Footer: "View All Requests" link

### Notification Items
- Icon: Blue gradient circle with lock icon
- Layout: Icon + content (username, message, time)
- Hover effect: Light gray background
- Time format: Relative (e.g., "5 minutes ago", "2 hours ago")
- Clickable: Navigates to the specific request with highlight

### Row Highlight Animation
- Duration: 5 seconds
- Background: Golden/yellow glow (#fef3c7)
- Box shadow: 3px golden border (#fbbf24)
- Left accent bar: Gradient golden bar (4px wide)
- Animation: Smooth fade from highlighted to normal state
- Scroll behavior: Smooth scroll to center the row in viewport

### Notification Badge
- Background: Red (#ef4444)
- Position: Top-right corner of bell icon
- Animation: Subtle pulse effect
- Font: Bold, 0.625rem
- Min width: 18px, Height: 18px
- Border radius: 9px (circular)

### Bell Icon
- Uses PrimeIcons bell icon (`pi-bell`)
- Size: 1.125rem
- Hover effect: Background changes to light gray
- Tooltip: Shows count and "pending password reset request(s)"

## Usage

### For Administrators
1. Log in with admin credentials
2. Look for the bell icon in the top navbar
3. If there's a red badge, it shows the number of pending requests
4. Click the bell to open the notification dropdown
5. View recent requests in the dropdown panel
6. Click on any notification to navigate to that specific request
7. The page will automatically scroll to the request and highlight it with a golden glow for 5 seconds
8. Process the request (approve/reject/reset password)
9. The count updates automatically after processing

### For Developers
To add more notification types in the future:
1. Create a new API endpoint for the notification count
2. Add a new icon/badge in the AppLayout navbar
3. Set up polling or event-based updates
4. Follow the same pattern as password reset notifications

## Testing

### Manual Testing
1. Create a password reset request from the login page
2. Log in as admin
3. Verify the bell icon shows a badge with count "1"
4. Click the bell icon to open the notification dropdown
5. Verify the dropdown shows the recent request with username and time
6. Click on the notification item
7. Verify the page navigates to Password Reset Requests
8. Verify the specific request row is highlighted with a golden glow
9. Verify the page scrolls to center the highlighted row
10. Wait 5 seconds and verify the highlight fades away
11. Approve or reject the request
12. Return to dashboard and verify the badge count decreased
13. Open the dropdown again and verify it shows "No pending requests"

### API Testing
```bash
# Get pending count (as admin)
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/auth/pending_reset_count/
```

## Future Enhancements
- Add sound/desktop notifications for new requests
- Support multiple notification types (not just password resets)
- Add notification history/log
- Implement WebSocket for real-time updates instead of polling
- Add notification preferences in user settings
