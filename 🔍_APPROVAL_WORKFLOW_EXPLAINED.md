# 🔍 Approval Workflow & User Management - Complete Guide

## ❗ IMPORTANT CLARIFICATIONS

You asked three excellent questions that reveal what's IMPLEMENTED vs what needs UI:

1. **Why can operator approve his own water nomination?**
2. **How does admin create user accounts?**
3. **How does manager approve data uploads and water nominations?**

---

## 1. 🚫 OPERATOR CANNOT APPROVE (Backend is Correct!)

### Current Implementation ✅

The **backend permission system is correctly implemented**:

```python
# In models.py - UserProfile
def can_approve_data(self):
    """Check if user can approve data"""
    return self.role in ['MANAGER', 'ADMIN'] or self.user.is_staff
```

**This means:**
- ✅ VIEWER: Cannot approve (can_approve_data = False)
- ✅ OPERATOR: Cannot approve (can_approve_data = False)
- ✅ MANAGER: Can approve (can_approve_data = True)
- ✅ ADMIN: Can approve (can_approve_data = True)

### The Problem 🐛

The **WaterNomination.vue frontend component** doesn't check permissions before showing the "Approve" button!

**Current behavior (WRONG):**
- Operator sees "Approve" button
- Operator clicks it
- Backend rejects it (because permission check fails)
- But operator shouldn't see the button at all!

**What needs to be fixed:**
```vue
<!-- WRONG (current) -->
<button @click="approveNomination(nomination)">
  Approve
</button>

<!-- CORRECT (should be) -->
<button 
  v-if="canApproveData()" 
  @click="approveNomination(nomination)">
  Approve
</button>
```

---

## 2. 👤 HOW ADMIN CREATES USER ACCOUNTS

### Current Implementation ✅

Admins can create users through **Django Admin Panel**:

**Step-by-Step:**

1. **Access Admin Panel**
   ```
   URL: http://localhost:8000/admin
   Login: admin / admin123
   ```

2. **Create New User**
   - Click "Users" → "Add User"
   - Enter username and password
   - Click "Save"

3. **Assign Role**
   - After creating user, click on the username
   - Scroll to "User profiles" section
   - Set:
     - Role: VIEWER / OPERATOR / MANAGER / ADMIN
     - Plant: (if operator/manager)
     - Department, Position, Phone, etc.
   - Click "Save"

### What's Missing ❌

**No frontend UI for user management!**

The system needs:
- User Management page (for admins)
- Create User form
- Edit User form
- Assign Role dropdown
- Assign Plant dropdown

**This is a FUTURE FEATURE** (Week 3-4 priority)

### Workaround (Current)

For now, admins must use:
1. Django Admin Panel (http://localhost:8000/admin)
2. Python script (see below)

---

## 3. 📋 HOW MANAGER APPROVES SUBMISSIONS

### Water Nomination Approval

**Backend API exists:**
```python
# In views.py - WaterNominationViewSet
@action(detail=True, methods=['post'])
def approve(self, request, pk=None):
    """Approve a submitted nomination"""
    nomination = self.get_object()
    
    if nomination.status != 'SUBMITTED':
        return Response({'error': 'Only submitted nominations can be approved'})
    
    nomination.status = 'APPROVED'
    nomination.approved_at = datetime.now()
    nomination.approved_by = request.user
    nomination.save()
    
    return Response({'message': 'Nomination approved successfully'})
```

**API Endpoint:**
```
POST /api/water-nominations/{id}/approve/
```

**Frontend Implementation:**

The WaterNomination.vue component has the approve function, but it needs permission checks:

```javascript
// Current (in WaterNomination.vue)
async approveNomination(nomination) {
  try {
    await axios.post(`/api/water-nominations/${nomination.id}/approve/`);
    this.loadNominations(); // Refresh list
  } catch (error) {
    console.error('Approval failed:', error);
  }
}
```

**What's Missing:**
- Permission check before showing "Approve" button
- Approval queue/list view for managers
- Notification when approval is needed

### Data Upload Approval

**Currently NOT implemented!**

The system allows operators to upload data, but there's no approval workflow for uploads yet.

**What exists:**
- Operators can upload Excel files
- Data is immediately imported
- No approval step

**What needs to be built:**
- Upload status: PENDING → APPROVED → COMPLETED
- Manager reviews upload before data is imported
- Approval queue for managers

---

## 🎯 WHAT'S IMPLEMENTED vs WHAT'S MISSING

### ✅ IMPLEMENTED (Backend)

| Feature | Status | Location |
|---------|--------|----------|
| User roles (VIEWER, OPERATOR, MANAGER, ADMIN) | ✅ | models.py |
| Permission checks (can_upload, can_approve, etc.) | ✅ | models.py |
| Water nomination approval API | ✅ | views.py |
| Role-based API access control | ✅ | permissions.py |
| Audit logging | ✅ | models.py, signals.py |
| Email notifications | ✅ | email_service.py |

### ❌ MISSING (Frontend UI)

| Feature | Status | Priority |
|---------|--------|----------|
| Permission checks in WaterNomination.vue | ❌ | HIGH |
| Approval queue page for managers | ❌ | HIGH |
| User management page (admin) | ❌ | MEDIUM |
| Upload approval workflow | ❌ | MEDIUM |
| Notification center | ❌ | LOW |

---

## 🔧 HOW TO FIX: Water Nomination Approval

### Step 1: Add Permission Check to Frontend

Update `WaterNomination.vue`:

```vue
<script>
import { canApproveData, isManagerOrAbove } from '@/utils/auth';

export default {
  methods: {
    canApprove() {
      return canApproveData();
    },
    
    showApproveButton(nomination) {
      // Only show if:
      // 1. User can approve
      // 2. Nomination is submitted (not draft or already approved)
      // 3. User didn't submit it (can't approve own submission)
      return this.canApprove() && 
             nomination.status === 'SUBMITTED' &&
             nomination.submitted_by_username !== this.currentUsername;
    }
  }
}
</script>

<template>
  <!-- In the nominations table -->
  <button 
    v-if="showApproveButton(nomination)"
    @click="approveNomination(nomination)"
    class="btn-success">
    <i class="pi pi-check"></i> Approve
  </button>
</template>
```

### Step 2: Create Approval Queue Page

Create `frontend/src/components/ApprovalQueue.vue`:

```vue
<template>
  <div class="approval-queue">
    <h2>Pending Approvals</h2>
    
    <!-- Water Nominations -->
    <div class="section">
      <h3>Water Nominations</h3>
      <div v-for="nomination in pendingNominations" :key="nomination.id">
        <div class="approval-card">
          <div class="info">
            <strong>{{ nomination.plant_name }}</strong>
            <span>{{ nomination.nomination_date }}</span>
            <span>Submitted by: {{ nomination.submitted_by_username }}</span>
          </div>
          <div class="actions">
            <button @click="approve(nomination)" class="btn-success">
              Approve
            </button>
            <button @click="reject(nomination)" class="btn-danger">
              Reject
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Data Uploads (future) -->
    <div class="section">
      <h3>Data Uploads</h3>
      <p>Coming soon...</p>
    </div>
  </div>
</template>
```

---

## 👥 HOW TO CREATE USERS (Current Methods)

### Method 1: Django Admin Panel (Easiest)

```
1. Go to http://localhost:8000/admin
2. Login as admin
3. Click "Users" → "Add User"
4. Fill in username and password
5. Click "Save and continue editing"
6. Scroll to "User profiles" section
7. Set role, plant, department, etc.
8. Click "Save"
```

### Method 2: Python Script

Create `backend/create_user.py`:

```python
from django.contrib.auth.models import User
from reports.models import UserProfile, Plant

# Create user
user = User.objects.create_user(
    username='john_operator',
    password='password123',
    email='john@npc.gov.ph',
    first_name='John',
    last_name='Doe'
)

# Get or create profile
profile, created = UserProfile.objects.get_or_create(user=user)

# Set role and plant
profile.role = 'OPERATOR'
profile.plant = Plant.objects.get(code='AGUS1')
profile.department = 'Operations'
profile.position = 'Plant Operator'
profile.phone = '+63 912 345 6789'
profile.save()

print(f"User {user.username} created with role {profile.role}")
```

Run it:
```bash
cd backend
python manage.py shell < create_user.py
```

### Method 3: Management Command (Future)

```bash
# This doesn't exist yet, but should be created
python manage.py create_user john_operator --role=OPERATOR --plant=AGUS1
```

---

## 📊 APPROVAL WORKFLOW DIAGRAM

```
OPERATOR                    MANAGER                     SYSTEM
   |                           |                           |
   |-- Submit Nomination ----->|                           |
   |                           |                           |
   |                           |-- Review Submission       |
   |                           |                           |
   |                           |-- Click "Approve" ------->|
   |                           |                           |
   |<------------------------- Email Notification ---------|
   |                           |                           |
   |                           |<----- Email Notification -|
   |                           |                           |
   |                           |                           |-- Status: APPROVED
   |                           |                           |-- Audit Log Created
   |                           |                           |-- Send to Grid Operator
```

---

## 🚀 PRIORITY FIXES NEEDED

### HIGH PRIORITY (Do Now)

1. **Fix WaterNomination.vue**
   - Add permission checks for approve button
   - Hide approve button for operators
   - Prevent self-approval

2. **Create Approval Queue Page**
   - List pending nominations
   - Filter by plant (for managers)
   - Show all (for admins)

### MEDIUM PRIORITY (Week 3-4)

3. **User Management UI**
   - Create user form
   - Edit user form
   - Assign roles
   - Assign plants

4. **Upload Approval Workflow**
   - Add approval step to uploads
   - Manager reviews before import
   - Reject with reason

### LOW PRIORITY (Future)

5. **Notification Center**
   - In-app notifications
   - Notification bell icon
   - Mark as read

6. **Approval History**
   - Who approved what
   - When approved
   - Approval comments

---

## 📝 SUMMARY

**Your Questions Answered:**

1. **Why can operator approve?**
   - Backend: Operator CANNOT approve (correct ✅)
   - Frontend: Button shows for everyone (bug 🐛)
   - Fix: Add permission check to hide button

2. **How does admin create users?**
   - Current: Django Admin Panel only
   - Future: User Management UI page
   - Workaround: Python script

3. **How does manager approve?**
   - Backend API: Exists and works ✅
   - Frontend: Needs permission checks
   - Missing: Approval queue page

**Next Steps:**
1. Fix WaterNomination.vue permission checks
2. Create ApprovalQueue.vue component
3. Add route for /approval-queue
4. Test with manager1 account

---

**Last Updated:** February 19, 2026
