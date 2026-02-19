# User Management System - Complete Guide

## Overview
A comprehensive user management interface has been implemented for administrators to easily create and manage user accounts without needing to access the Django admin panel.

## Features

### 1. User List View
- **Table Display**: Shows all users with key information
  - Username
  - Email
  - Role (Admin, Manager, Operator, Viewer)
  - Status (Active/Inactive)
  - Date Joined
  
- **Statistics Dashboard**: 
  - Total Users count
  - Active Users count
  - Admins count
  - Managers count

### 2. Search and Filtering
- **Search**: Search by username or email
- **Filter by Role**: Admin, Manager, Operator, Viewer
- **Filter by Status**: Active or Inactive users

### 3. Create New User
Admins can create new users with:
- Username (required, unique)
- Email address
- Password (required for new users)
- Role assignment (Viewer, Operator, Manager, Admin)
- Active status toggle

### 4. Edit User
- Update user information
- Change user role
- Modify email address
- Toggle active status
- Note: Username cannot be changed after creation

### 5. User Actions
- **Activate/Deactivate**: Toggle user access without deleting
- **Delete**: Permanently remove user account
- **Edit**: Modify user details and role

## Access

### For Administrators
1. Login with admin credentials
2. Navigate to sidebar → Administration → User Management
3. Or access directly at: `http://localhost:8080/user-management`

## User Roles

### VIEWER
- Can view reports and dashboards
- Read-only access
- Cannot upload or modify data

### OPERATOR
- All Viewer permissions
- Can upload Excel files
- Can create water nominations
- Cannot approve nominations

### MANAGER
- All Operator permissions
- Can approve water nominations
- Can manage team data

### ADMIN
- Full system access
- Can manage users
- Can access admin panel
- Can view audit logs
- All Manager permissions

## How to Create a New User

1. **Click "Create New User"** button
2. **Fill in the form**:
   - Enter username (required)
   - Enter email address (optional but recommended)
   - Enter password (required, minimum 8 characters)
   - Confirm password
   - Select role from dropdown
   - Check "Active User" if account should be immediately active
3. **Click "Create User"**
4. User account is created and can login immediately

## How to Edit a User

1. **Find the user** in the table (use search/filters if needed)
2. **Click the edit icon** (pencil) in the Actions column
3. **Modify information**:
   - Update email
   - Change role
   - Toggle active status
   - Note: Password cannot be changed through this interface
4. **Click "Update User"**

## How to Deactivate/Activate a User

1. **Find the user** in the table
2. **Click the activate/deactivate icon** in the Actions column
3. **Confirm the action**
4. User status is updated immediately
   - Deactivated users cannot login
   - Activated users can login normally

## How to Delete a User

1. **Find the user** in the table
2. **Click the delete icon** (trash) in the Actions column
3. **Confirm deletion** (this action cannot be undone)
4. User account is permanently removed

## API Endpoints Used

The frontend communicates with these backend endpoints:

- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `PUT /api/users/{id}/` - Update user
- `PATCH /api/users/{id}/` - Partial update (e.g., toggle status)
- `DELETE /api/users/{id}/` - Delete user

## Security

- Only users with ADMIN role can access User Management
- All API endpoints require authentication
- Passwords are hashed and never displayed
- User actions are logged in audit logs

## Best Practices

1. **Use Strong Passwords**: Require users to use strong passwords
2. **Assign Appropriate Roles**: Give users only the permissions they need
3. **Regular Review**: Periodically review user accounts and deactivate unused ones
4. **Email Addresses**: Always add email addresses for password recovery
5. **Deactivate Instead of Delete**: Deactivate users instead of deleting to preserve audit trails

## Troubleshooting

### Cannot Create User
- Check if username already exists
- Ensure password meets requirements
- Verify all required fields are filled

### Cannot Edit User
- Ensure you have admin permissions
- Check if user still exists
- Verify network connection

### User Cannot Login After Creation
- Check if user is marked as "Active"
- Verify password was set correctly
- Check if user has appropriate role assigned

## Future Enhancements

Potential improvements for future versions:
- Password reset functionality
- Bulk user import from CSV
- User activity reports
- Email notifications for new accounts
- Two-factor authentication setup
- User groups and permissions
- Export user list to Excel

## Support

For issues or questions:
1. Check audit logs for error details
2. Verify user has admin permissions
3. Check browser console for errors
4. Contact system administrator
