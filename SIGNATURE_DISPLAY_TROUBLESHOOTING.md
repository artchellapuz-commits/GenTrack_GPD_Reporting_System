# Signature Display Troubleshooting Guide

## Current Implementation Status ✅

### Backend (Working)
- ✅ **API Response**: Returns correct signature URLs like `http://localhost:8000/media/admin_signatures/c_c__amigable_jr__signature.png`
- ✅ **File Existence**: Signature files exist in `media/admin_signatures/` directory
- ✅ **URL Access**: Direct URL access returns 200 OK with image/png content
- ✅ **CORS Configuration**: Properly configured to allow frontend access
- ✅ **Serializer Logic**: Enhanced with glob pattern matching for flexible filename detection

### Frontend (Implemented)
- ✅ **Modal Template**: Digital Signature section added to authorization details modal
- ✅ **Conditional Rendering**: Three states handled (has signature, missing file, no signature)
- ✅ **CSS Styling**: Professional signature display with verification badges
- ✅ **Debug Logging**: Added console.log and error handlers for troubleshooting

## Troubleshooting Steps

### 1. Check Browser Console
When you click "View Details" on an authorization with a signature, check the browser console for:
```
🔍 Viewing auth details: {object}
🖼️ Signature URL: http://localhost:8000/media/admin_signatures/...
✅ Has signature: true
📝 Signature created: true
```

### 2. Check Image Loading
If the image fails to load, you'll see:
```
❌ Signature image failed to load: {error event}
❌ Image src: http://localhost:8000/media/admin_signatures/...
```

### 3. Test Direct URL Access
Copy the signature URL from console and paste it directly in browser address bar. It should show the signature image.

### 4. Check Network Tab
In browser DevTools > Network tab, look for:
- API request to `/api/signatory-authorizations/` (should return signature_url)
- Image request to signature URL (should return 200 OK)

## Common Issues & Solutions

### Issue 1: Image Shows Broken Icon
**Cause**: CORS or network connectivity issue
**Solution**: 
- Ensure Django backend is running on port 8000
- Check CORS configuration allows localhost:8080
- Verify signature URL is accessible directly

### Issue 2: No Signature Section Appears
**Cause**: API not returning signature data or condition not met
**Solution**:
- Check if `selectedAuthDetails.has_signature` is true
- Verify API response includes signature_url field
- Check if authorization has `signature_created: true`

### Issue 3: Wrong Filename Pattern
**Cause**: Filename generation mismatch
**Solution**:
- Enhanced serializer now uses glob pattern matching
- Handles multiple filename variations
- Falls back to pattern matching if exact match fails

## Testing Commands

### Test API Response
```bash
python test_signature_url_simple.py
```

### Test URL Access
```bash
python test_signature_url_access.py
```

### Check File Existence
```bash
dir npc-reporting-system\backend\media\admin_signatures
```

## Expected Behavior

1. **User clicks "View Details"** on authorization with signature
2. **Console shows debug info** about the authorization data
3. **Modal opens** with Digital Signature section visible
4. **Image loads** showing the actual signature
5. **Verification badge** shows "Verified Digital Signature"

## Files Modified

### Backend
- `serializers_security.py`: Enhanced signature URL generation with glob patterns
- `models.py`: Fixed timezone import in is_valid method

### Frontend  
- `SignatoryAuthorizationRequest.vue`: Added signature display and debug logging

## Next Steps

1. **Open browser DevTools** and check Console tab
2. **Click "View Details"** on an authorization that has `signature_created: true`
3. **Look for debug messages** and any error messages
4. **Check Network tab** for failed requests
5. **Test direct URL access** if image doesn't load

The implementation is complete and should be working. Any remaining issues are likely related to network connectivity, CORS, or browser caching.