# User Management Page - Visual Guide

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  USER MANAGEMENT                        [+ Create New User]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  👥 12   │  │  ✓ 10    │  │  🛡️ 2    │  │  💼 3    │       │
│  │  Total   │  │  Active  │  │  Admins  │  │ Managers │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Search: [________________]  Role: [All Roles ▼]  Status: [All ▼]│
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Username    Email              Role      Status    Date Joined │
│  ─────────────────────────────────────────────────────────────  │
│  👤 admin    admin@npc.com      ADMIN     Active    Jan 15      │
│                                                     [✏️][🔒][🗑️] │
│  👤 manager1 manager@npc.com    MANAGER   Active    Jan 20      │
│                                                     [✏️][🔒][🗑️] │
│  👤 operator operator@npc.com   OPERATOR  Inactive  Feb 01      │
│                                                     [✏️][✓][🗑️]  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Statistics Cards

### Total Users Card
```
┌──────────────┐
│   👥         │
│   12         │
│ Total Users  │
└──────────────┘
```
Shows the total number of users in the system.

### Active Users Card
```
┌──────────────┐
│   ✓          │
│   10         │
│ Active Users │
└──────────────┘
```
Shows how many users can currently login.

### Admins Card
```
┌──────────────┐
│   🛡️         │
│   2          │
│   Admins     │
└──────────────┘
```
Shows the number of admin users.

### Managers Card
```
┌──────────────┐
│   💼         │
│   3          │
│  Managers    │
└──────────────┘
```
Shows the number of manager users.

## Search and Filter Section

```
┌─────────────────────────────────────────────────────────────┐
│ Search                                                       │
│ [Search by username or email...                          ] │
│                                                              │
│ Role                    Status                               │
│ [All Roles        ▼]   [All Status       ▼]                │
└─────────────────────────────────────────────────────────────┘
```

### Search Options:
- Type username or email to filter results in real-time
- Results update as you type

### Role Filter Options:
- All Roles
- Admin
- Manager
- Operator
- Viewer

### Status Filter Options:
- All Status
- Active
- Inactive

## User Table

```
┌──────────────────────────────────────────────────────────────────┐
│ Username  │ Email           │ Role     │ Status  │ Date   │ Actions│
├──────────────────────────────────────────────────────────────────┤
│ 👤 admin  │ admin@npc.com   │ ADMIN    │ Active  │ Jan 15 │ [✏️][🔒][🗑️]│
│ 👤 john   │ john@npc.com    │ MANAGER  │ Active  │ Jan 20 │ [✏️][🔒][🗑️]│
│ 👤 mary   │ mary@npc.com    │ OPERATOR │ Inactive│ Feb 01 │ [✏️][✓][🗑️] │
└──────────────────────────────────────────────────────────────────┘
```

### Role Badges:
- **ADMIN** - Red badge
- **MANAGER** - Orange badge
- **OPERATOR** - Green badge
- **VIEWER** - Blue badge

### Status Badges:
- **Active** - Green badge
- **Inactive** - Red badge

### Action Buttons:
- **✏️ Edit** - Yellow button - Opens edit modal
- **🔒 Deactivate** - Gray button - Disables user login
- **✓ Activate** - Green button - Enables user login
- **🗑️ Delete** - Red button - Permanently removes user

## Create/Edit User Modal

```
┌─────────────────────────────────────────────────┐
│  Create New User                            [×] │
├─────────────────────────────────────────────────┤
│                                                  │
│  Username *                                      │
│  [_____________________________________]         │
│                                                  │
│  Email                                           │
│  [_____________________________________]         │
│                                                  │
│  Password *                                      │
│  [_____________________________________]         │
│                                                  │
│  Confirm Password *                              │
│  [_____________________________________]         │
│                                                  │
│  Role *                                          │
│  [Viewer                              ▼]        │
│                                                  │
│  ☑ Active User                                  │
│                                                  │
├─────────────────────────────────────────────────┤
│                      [Cancel] [Create User]     │
└─────────────────────────────────────────────────┘
```

### Form Fields:

**Username** (required)
- Must be unique
- Cannot be changed after creation
- Used for login

**Email** (optional)
- Recommended for password recovery
- Can be updated later

**Password** (required for new users)
- Minimum 8 characters recommended
- Not shown when editing existing users

**Confirm Password** (required for new users)
- Must match password field
- Validation happens on submit

**Role** (required)
- Dropdown with options:
  - Viewer (default)
  - Operator
  - Manager
  - Admin

**Active User** (checkbox)
- Checked = User can login
- Unchecked = User cannot login

## Color Scheme

### Statistics Cards:
- Total Users: Purple gradient
- Active Users: Blue gradient
- Admins: Pink gradient
- Managers: Teal gradient

### Role Badges:
- Admin: Red background (#fee2e2), Dark red text (#991b1b)
- Manager: Yellow background (#fef3c7), Dark yellow text (#92400e)
- Operator: Green background (#d1fae5), Dark green text (#065f46)
- Viewer: Blue background (#dbeafe), Dark blue text (#1e40af)

### Status Badges:
- Active: Green background (#d1fae5), Dark green text (#065f46)
- Inactive: Red background (#fee2e2), Dark red text (#991b1b)

### Action Buttons:
- Edit: Yellow background (#fef3c7), Dark yellow text (#92400e)
- Delete: Red background (#fee2e2), Dark red text (#991b1b)
- Activate: Green background (#d1fae5), Dark green text (#065f46)
- Deactivate: Gray background (#e2e8f0), Dark gray text (#475569)

## Responsive Design

### Desktop (> 1200px):
- Statistics cards in 4 columns
- Full table with all columns visible
- Filters in 3 columns

### Tablet (768px - 1200px):
- Statistics cards in 2 columns
- Table scrolls horizontally if needed
- Filters stack vertically

### Mobile (< 768px):
- Statistics cards in 1 column
- Table becomes scrollable
- Filters stack vertically
- Modal takes full width

## User Interactions

### Hover Effects:
- Statistics cards lift up slightly
- Table rows highlight on hover
- Buttons change color on hover
- Cursor changes to pointer on clickable elements

### Click Actions:
- Create New User button → Opens modal
- Edit button → Opens modal with user data
- Activate/Deactivate → Shows confirmation dialog
- Delete → Shows confirmation dialog
- Search input → Filters results in real-time
- Filter dropdowns → Updates table immediately

### Loading States:
- Spinner shown while fetching users
- Buttons disabled during API calls
- Loading message displayed

### Empty States:
- "No users found" message when filters return no results
- Large user icon with message
- Suggestion to adjust filters

## Accessibility Features

- All buttons have descriptive titles
- Form fields have proper labels
- Keyboard navigation supported
- Focus indicators visible
- Color contrast meets WCAG standards
- Screen reader friendly

## Best Practices for Use

1. **Always fill in email addresses** - Helps with account recovery
2. **Use descriptive usernames** - Makes user identification easier
3. **Assign appropriate roles** - Follow principle of least privilege
4. **Deactivate instead of delete** - Preserves audit trail
5. **Regular review** - Check for inactive accounts periodically
6. **Strong passwords** - Enforce password requirements
7. **Test new accounts** - Verify users can login after creation

## Common Workflows

### Creating a New Operator:
1. Click "Create New User"
2. Enter username (e.g., "operator_agus1")
3. Enter email
4. Set password
5. Select "Operator" role
6. Check "Active User"
7. Click "Create User"

### Promoting User to Manager:
1. Find user in table
2. Click edit button
3. Change role to "Manager"
4. Click "Update User"

### Temporarily Disabling Access:
1. Find user in table
2. Click deactivate button
3. Confirm action
4. User cannot login until reactivated

### Removing Old Account:
1. Find user in table
2. Click delete button
3. Confirm deletion
4. User permanently removed

