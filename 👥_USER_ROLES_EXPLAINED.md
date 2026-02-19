# 👥 User Roles Explained - NPC Reporting System

## Overview
The system has 4 user roles with different access levels and permissions. Each role is designed for specific job functions in the organization.

---

## 🔵 VIEWER (Read-Only Access)

**Who:** Management, executives, external stakeholders, auditors

**Purpose:** View reports and data without making changes

### What They Can Do:
✅ View Dashboard (see all plant statistics and charts)
✅ View Reports (browse historical data)
✅ Generate Reports (export data to Excel/PDF)
✅ Search and filter data
✅ View charts and analytics

### What They CANNOT Do:
❌ Upload new data
❌ Submit water nominations
❌ Edit or delete data
❌ Approve submissions
❌ Manage users
❌ Access admin panel

### UI Access:
- Dashboard
- View Reports
- Generate Report

**Badge Color:** Blue

**Use Case Example:**
> "The Regional Director needs to monitor plant performance but shouldn't be able to modify operational data."

---

## 🟢 OPERATOR (Data Entry)

**Who:** Plant operators, data encoders, field staff

**Purpose:** Upload daily generation data and submit water nominations

### What They Can Do:
✅ Everything VIEWER can do, PLUS:
✅ Upload Excel files with generation data
✅ Submit water nominations for their assigned plant
✅ Edit their own submissions (before approval)
✅ View upload history

### What They CANNOT Do:
❌ Approve data submissions
❌ Delete approved data
❌ Manage users
❌ Access admin panel
❌ Upload data for other plants (if assigned to specific plant)

### UI Access:
- Dashboard
- Upload Excel ⭐ NEW
- View Reports
- Generate Report
- Water Nomination ⭐ NEW

**Badge Color:** Green

**Use Case Example:**
> "The Agus 1 plant operator uploads daily generation data every morning and submits water nominations for the next day."

---

## 🟠 MANAGER (Approval & Oversight)

**Who:** Plant managers, supervisors, department heads

**Purpose:** Review and approve data submissions, oversee operations

### What They Can Do:
✅ Everything OPERATOR can do, PLUS:
✅ Approve water nominations
✅ Approve data uploads
✅ View audit logs for their plant
✅ Edit approved data (with audit trail)
✅ Delete incorrect submissions
✅ Assign operators to plants

### What They CANNOT Do:
❌ Manage system-wide users (only their plant staff)
❌ Access Django admin panel
❌ Change system settings
❌ View other plants' sensitive data (if restricted)

### UI Access:
- Dashboard
- Upload Excel
- View Reports
- Generate Report
- Water Nomination
- Approval Queue (future feature)

**Badge Color:** Orange

**Use Case Example:**
> "The Pulangi 4 Plant Manager reviews and approves the operator's water nomination before it's sent to the grid operator."

---

## 🔴 ADMIN (Full System Access)

**Who:** System administrators, IT staff, super users

**Purpose:** Full system control, user management, system configuration

### What They Can Do:
✅ Everything MANAGER can do, PLUS:
✅ Access Django Admin Panel
✅ Create/edit/delete any user
✅ Assign roles to users
✅ View all audit logs (system-wide)
✅ Manage plants and units
✅ Configure system settings
✅ Delete any data
✅ Run database maintenance
✅ View email notification logs

### What They CANNOT Do:
Nothing - they have full access

### UI Access:
- Dashboard
- Upload Excel
- View Reports
- Generate Report
- Water Nomination
- Admin Panel ⭐ NEW
- Audit Logs ⭐ NEW
- User Management ⭐ NEW

**Badge Color:** Red

**Use Case Example:**
> "The IT Administrator creates new user accounts, assigns roles, and monitors system activity through audit logs."

---

## 📊 Comparison Table

| Feature | Viewer | Operator | Manager | Admin |
|---------|--------|----------|---------|-------|
| **View Dashboard** | ✅ | ✅ | ✅ | ✅ |
| **View Reports** | ✅ | ✅ | ✅ | ✅ |
| **Generate Reports** | ✅ | ✅ | ✅ | ✅ |
| **Export Data** | ✅ | ✅ | ✅ | ✅ |
| **Upload Excel** | ❌ | ✅ | ✅ | ✅ |
| **Submit Water Nomination** | ❌ | ✅ | ✅ | ✅ |
| **Approve Submissions** | ❌ | ❌ | ✅ | ✅ |
| **Edit Approved Data** | ❌ | ❌ | ✅ | ✅ |
| **Delete Data** | ❌ | ❌ | ✅ | ✅ |
| **View Audit Logs** | ❌ | ❌ | 🟡 Own Plant | ✅ All |
| **Manage Users** | ❌ | ❌ | 🟡 Own Plant | ✅ All |
| **Admin Panel** | ❌ | ❌ | ❌ | ✅ |
| **System Settings** | ❌ | ❌ | ❌ | ✅ |

🟡 = Limited access

---

## 🎯 Permission Matrix

### Data Permissions
| Permission | Viewer | Operator | Manager | Admin |
|------------|--------|----------|---------|-------|
| `can_upload_data` | ❌ | ✅ | ✅ | ✅ |
| `can_approve_data` | ❌ | ❌ | ✅ | ✅ |
| `can_export_data` | ✅ | ✅ | ✅ | ✅ |
| `can_delete_data` | ❌ | ❌ | ✅ | ✅ |
| `can_edit_approved` | ❌ | ❌ | ✅ | ✅ |

### User Management Permissions
| Permission | Viewer | Operator | Manager | Admin |
|------------|--------|----------|---------|-------|
| `can_manage_users` | ❌ | ❌ | 🟡 | ✅ |
| `can_assign_roles` | ❌ | ❌ | ❌ | ✅ |
| `can_view_audit_logs` | ❌ | ❌ | 🟡 | ✅ |
| `can_access_admin` | ❌ | ❌ | ❌ | ✅ |

---

## 🏢 Real-World Workflow Example

### Daily Operations at Agus 1 Plant

**Morning (8:00 AM):**
1. **Operator (operator1)** logs in
2. Uploads yesterday's generation data Excel file
3. Submits water nomination for tomorrow

**Mid-Morning (10:00 AM):**
1. **Manager (manager1)** logs in
2. Reviews the uploaded data
3. Approves the water nomination
4. System sends email notification to grid operator

**Afternoon (2:00 PM):**
1. **Viewer (viewer1)** - Regional Director logs in
2. Views dashboard to check all plants' performance
3. Generates monthly report for executive meeting
4. Exports data to PDF

**End of Day:**
1. **Admin (admin)** checks audit logs
2. Verifies all plants submitted data
3. Reviews any error notifications
4. Prepares system backup

---

## 🔐 Security Features

### Role-Based Access Control (RBAC)
- Users can only access features allowed by their role
- UI automatically hides unauthorized menu items
- API endpoints validate permissions on every request
- Unauthorized access attempts are logged

### Audit Trail
- All actions are logged with:
  - Who performed the action
  - What was changed
  - When it happened
  - IP address and device info
- Managers can view logs for their plant
- Admins can view all system logs

### Data Isolation
- Operators can only upload for their assigned plant
- Managers can only approve for their plant
- Viewers see all data but can't modify
- Admins have full access

---

## 📝 Test Users

The system comes with pre-created test users:

| Username | Password | Role | Plant |
|----------|----------|------|-------|
| viewer1 | test123 | VIEWER | None (all plants) |
| operator1 | test123 | OPERATOR | Agus 1 |
| manager1 | test123 | MANAGER | Agus 1 |
| admin | admin123 | ADMIN | None (all plants) |

---

## 🎨 Visual Indicators

### Role Badges
Each user sees their role badge in the sidebar:
- **VIEWER** - Blue badge
- **OPERATOR** - Green badge
- **MANAGER** - Orange badge
- **ADMIN** - Red badge

### Menu Items
Menu items are shown/hidden based on role:
- Grayed out = No access
- Hidden = Not visible at all
- Highlighted = Current page

---

## 🚀 How to Assign Roles

### For Admins:

**Option 1: Django Admin Panel**
1. Go to http://localhost:8000/admin
2. Click "User profiles"
3. Select user
4. Change "Role" dropdown
5. Save

**Option 2: Python Script**
```python
from django.contrib.auth.models import User
from reports.models import UserProfile

user = User.objects.get(username='john')
profile = user.profile
profile.role = 'OPERATOR'
profile.plant = Plant.objects.get(code='AGUS1')
profile.save()
```

**Option 3: Management Command** (future feature)
```bash
python manage.py assign_role john OPERATOR --plant=AGUS1
```

---

## 💡 Best Practices

### Role Assignment Guidelines

1. **Start with VIEWER**
   - Give new users VIEWER role first
   - Let them learn the system
   - Upgrade role when trained

2. **One Operator per Plant**
   - Assign operators to specific plants
   - Prevents data entry conflicts
   - Clear responsibility

3. **Manager Oversight**
   - Each plant should have a manager
   - Manager approves operator submissions
   - Provides accountability

4. **Limit Admin Access**
   - Only IT staff should be admins
   - Too many admins = security risk
   - Use MANAGER role for plant supervisors

### Security Tips

- Change default passwords immediately
- Use strong passwords (8+ characters, mixed case, numbers)
- Review audit logs regularly
- Disable inactive user accounts
- Don't share login credentials

---

## 🔄 Role Upgrade Path

Typical career progression:

```
VIEWER → OPERATOR → MANAGER → ADMIN
  ↓         ↓          ↓         ↓
Learn    Enter     Approve   Manage
System    Data      Data     System
```

**Example:**
1. New hire starts as VIEWER (1 month)
2. After training, promoted to OPERATOR (6-12 months)
3. Experienced operator becomes MANAGER (2+ years)
4. IT staff or senior manager becomes ADMIN

---

## ❓ FAQ

**Q: Can a user have multiple roles?**
A: No, each user has exactly one role. If someone needs mixed permissions, use MANAGER role.

**Q: Can I create custom roles?**
A: Not currently. The 4 roles cover most use cases. Custom roles can be added in future versions.

**Q: What happens if I change someone's role?**
A: Their permissions update immediately. They'll see different menu items on next page load.

**Q: Can operators see other plants' data?**
A: Yes, they can VIEW all plants, but can only UPLOAD for their assigned plant.

**Q: How do I know who uploaded specific data?**
A: Check the "Uploaded By" column in View Reports, or check Audit Logs (Manager/Admin only).

**Q: Can I temporarily disable a user without deleting?**
A: Yes, admins can set "Is Active" to False in Django admin panel.

---

## 📞 Support

If you need help with roles and permissions:
1. Check this guide first
2. Review the audit logs
3. Contact your system administrator
4. Check the Django admin panel (admins only)

---

**Last Updated:** February 19, 2026
**Version:** 1.0
