# Document Manager - Purpose and Usage Guide

## 🎯 Purpose of the Document Manager

The **Document Manager** is the central hub for the **E-Signature Workflow System** in the NPC Reporting System. It serves as a comprehensive solution for managing digital documents that require official signatures and approvals.

### Primary Functions:

## 1. 📄 Document Creation & Management
- **Create Documents**: Generate new documents requiring signatures (PSR reports, approvals, contracts)
- **Document Types**: Support for PSR, Daily Reports, Monthly Reports, and Custom Documents
- **Content Management**: Store document content directly or upload document files
- **Status Tracking**: Monitor document lifecycle (Draft → Pending Signature → Signed → Completed)

## 2. ✍️ Digital Signature Workflow
- **Request Signatures**: Send signature requests to specific individuals via email
- **Multiple Signers**: Support for multiple signers per document with different roles
- **Secure Links**: Generate unique, token-based signature links for security
- **Signature Types**: Support for hand-drawn, uploaded image, and typed signatures
- **Expiration Control**: Set expiration dates for signature requests

## 3. 📧 Email Notification System
- **Automatic Emails**: Send signature request emails with secure links
- **Real-time Updates**: Notify when signatures are completed
- **Reminder System**: Track pending signatures and send reminders
- **Professional Templates**: Use branded email templates for requests

## 4. 🔒 Security & Compliance
- **Token-based Security**: Each signature link has a unique, secure token
- **Audit Trail**: Complete logging of all signature activities
- **Verification**: Hash-based signature verification for authenticity
- **IP Tracking**: Log IP addresses and user agents for security
- **Expiration**: Automatic expiration of signature links

## 5. 📊 Tracking & Reporting
- **Status Dashboard**: View all documents and their signature status
- **Progress Tracking**: Monitor how many signatures are completed
- **Audit Logs**: Complete history of all signature-related activities
- **Compliance Reports**: Generate reports for regulatory compliance

---

## 🚀 How to Use the Document Manager

### For Document Creators:

#### Step 1: Access Document Manager
1. Login to the NPC Reporting System
2. Click **"Document Manager"** in the left sidebar
3. You'll see your documents dashboard

#### Step 2: Create a New Document
1. Click **"Create Document"** button
2. Fill in document details:
   - **Title**: Name of the document
   - **Type**: PSR, Daily, Monthly, or Custom
   - **Content**: Document text or upload file
3. Save as **Draft**

#### Step 3: Request Signatures
1. Select your document
2. Click **"Request Signatures"**
3. Add signers:
   - **Name**: Full name of signer
   - **Email**: Email address for notifications
   - **Role**: Their role (e.g., "Prepared by", "Approved by")
4. Set expiration time (default: 72 hours)
5. Send requests

#### Step 4: Track Progress
1. Monitor signature status in real-time
2. View who has signed and who hasn't
3. Receive email notifications when signatures are completed
4. Download completed documents

### For Signers:

#### Step 1: Receive Email
- Get signature request email with secure link
- Email contains document details and signing instructions

#### Step 2: Access Signing Page
- Click the secure link in the email
- Opens the signing page with the document

#### Step 3: Create Signature
Choose your preferred signature method:
- **Draw**: Use mouse or finger to draw signature
- **Upload**: Upload an image of your signature
- **Type**: Type your name as signature

#### Step 4: Submit Signature
- Review your signature
- Click **"Sign Document"**
- Signature is saved and document updated

---

## 🏢 Business Use Cases

### 1. **Plant Status Reports (PSR)**
- Generate daily/monthly PSR reports
- Request signatures from plant managers
- Get approvals from supervisors
- Maintain audit trail for compliance

### 2. **Official Approvals**
- Budget approvals
- Maintenance authorizations
- Policy changes
- Equipment purchases

### 3. **Contracts & Agreements**
- Vendor contracts
- Service agreements
- Employment documents
- Partnership agreements

### 4. **Compliance Documents**
- Regulatory filings
- Safety certifications
- Environmental reports
- Audit documents

---

## 🔧 Technical Features

### API Endpoints:
- `GET /api/documents/` - List documents
- `POST /api/documents/` - Create document
- `GET /api/documents/{id}/` - Get specific document
- `POST /api/documents/{id}/request_signatures/` - Request signatures
- `GET /api/signature-requests/` - List signature requests
- `POST /api/sign/{token}/` - Sign document with token

### Security Features:
- JWT authentication required
- Token-based signature links
- IP address logging
- User agent tracking
- Signature verification hashes
- Automatic link expiration

### Email Integration:
- Gmail SMTP configured
- Professional email templates
- Automatic notifications
- Real-time delivery

---

## 📈 Benefits

### For Organizations:
- **Paperless Process**: Eliminate physical document handling
- **Faster Approvals**: Reduce approval time from days to hours
- **Cost Savings**: Reduce printing, scanning, and storage costs
- **Compliance**: Maintain complete audit trails
- **Security**: Secure, verifiable digital signatures

### For Users:
- **Convenience**: Sign documents from anywhere
- **Mobile Friendly**: Works on phones and tablets
- **Real-time Updates**: Know immediately when documents are signed
- **Easy Tracking**: See all pending signatures in one place

---

## 🎉 Current Status

✅ **Fully Implemented and Ready**
- All API endpoints working
- Frontend components complete
- Email notifications functional
- Database migrations applied
- Sidebar navigation integrated

The Document Manager is now fully operational and ready for production use in the NPC Reporting System!

---

**Last Updated**: March 16, 2026
**Status**: ✅ PRODUCTION READY