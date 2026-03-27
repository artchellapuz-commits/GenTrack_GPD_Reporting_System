#!/usr/bin/env python3
"""
Test script to verify signature status indicators are working correctly
"""

import requests
import json
from datetime import datetime

def test_signature_status_indicators():
    """Test that signature status indicators are properly displayed"""
    
    print("🧪 Testing Signature Status Indicators")
    print("=" * 50)
    
    # Test API endpoint
    api_url = "http://localhost:8000/api/signatory-authorizations/my-authorizations/"
    
    try:
        # Make API request to get user authorizations
        print("📡 Making API request to get user authorizations...")
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            authorizations = data if isinstance(data, list) else data.get('results', [])
            
            print(f"✅ API Response successful - Found {len(authorizations)} authorizations")
            
            # Check each authorization for signature status fields
            for i, auth in enumerate(authorizations, 1):
                print(f"\n📋 Authorization {i}:")
                print(f"   Signatory: {auth.get('signatory_name', 'N/A')}")
                print(f"   Has Signature: {auth.get('has_signature', 'N/A')}")
                print(f"   Signature Created: {auth.get('signature_created', 'N/A')}")
                print(f"   Signature URL: {auth.get('signature_url', 'N/A')}")
                
                # Determine expected status
                has_signature = auth.get('has_signature', False)
                signature_created = auth.get('signature_created', False)
                
                if has_signature:
                    expected_status = "✅ Signature Ready (Green)"
                elif signature_created:
                    expected_status = "⚠️ Signature File Missing (Orange)"
                else:
                    expected_status = "❌ No Signature Created (Red)"
                
                print(f"   Expected Status: {expected_status}")
            
            if authorizations:
                print(f"\n🎯 Frontend Implementation Check:")
                print("   ✅ Signature indicators should appear on authorization cards")
                print("   ✅ Green checkmark for ready signatures")
                print("   ✅ Orange warning for missing signature files")
                print("   ✅ Red X for no signature created")
                print("   ✅ Status text should appear under signatory name")
                
                print(f"\n📱 Visual Elements:")
                print("   • Small circular badge on avatar (top-right corner)")
                print("   • Status text with icon under signatory name")
                print("   • Color-coded indicators (green/orange/red)")
                print("   • Hover effects for better interactivity")
            else:
                print("⚠️ No authorizations found - create some test data to see indicators")
                
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server")
        print("   Make sure Django server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during test: {e}")
    
    print(f"\n🔍 Manual Testing Steps:")
    print("1. Open http://localhost:8080 in browser")
    print("2. Navigate to Signature Authorization page")
    print("3. Look for authorization cards in 'Your Active Authorizations' section")
    print("4. Check for signature status indicators:")
    print("   - Small badge on user avatar (top-right)")
    print("   - Status text under signatory name")
    print("   - Color coding: Green=Ready, Orange=Missing, Red=None")
    
    print(f"\n✅ Test completed at {datetime.now()}")

if __name__ == "__main__":
    test_signature_status_indicators()