#!/usr/bin/env python3
"""
Debug URL resolution to see which view is actually handling the request
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.urls import resolve
from django.test import RequestFactory

def debug_url_resolution():
    """Debug URL resolution"""
    print("🔍 Debugging URL Resolution")
    print("=" * 50)
    
    # Test the URL that should go to our custom action
    url_path = '/api/signatory-authorizations/request/'
    
    try:
        resolved = resolve(url_path)
        print(f"URL: {url_path}")
        print(f"View function: {resolved.func}")
        print(f"View name: {resolved.view_name}")
        print(f"URL name: {resolved.url_name}")
        print(f"Args: {resolved.args}")
        print(f"Kwargs: {resolved.kwargs}")
        
        # Get the actual view class
        if hasattr(resolved.func, 'cls'):
            view_class = resolved.func.cls
            print(f"View class: {view_class}")
            print(f"View class module: {view_class.__module__}")
            
            # Check if it's our ViewSet
            from reports.views_authorization import SignatoryAuthorizationViewSet
            if view_class == SignatoryAuthorizationViewSet:
                print("✅ URL resolves to our SignatoryAuthorizationViewSet")
                
                # Check what action it would call
                factory = RequestFactory()
                request = factory.post(url_path)
                
                # Create view instance
                view = resolved.func.view_class()
                view.request = request
                view.format_kwarg = None
                
                # Get the action
                if hasattr(view, 'get_action'):
                    action = view.get_action()
                    print(f"Action that would be called: {action}")
                else:
                    print("❌ View doesn't have get_action method")
                    
            else:
                print(f"❌ URL resolves to different ViewSet: {view_class}")
        else:
            print("❌ Resolved function doesn't have cls attribute")
            
    except Exception as e:
        print(f"❌ Error resolving URL: {e}")
        import traceback
        traceback.print_exc()
    
    # Also test the base URL
    print("\n" + "=" * 50)
    base_url = '/api/signatory-authorizations/'
    
    try:
        resolved = resolve(base_url)
        print(f"Base URL: {base_url}")
        print(f"View function: {resolved.func}")
        print(f"View name: {resolved.view_name}")
        print(f"URL name: {resolved.url_name}")
        
        if hasattr(resolved.func, 'cls'):
            view_class = resolved.func.cls
            print(f"Base view class: {view_class}")
            
    except Exception as e:
        print(f"❌ Error resolving base URL: {e}")

if __name__ == "__main__":
    debug_url_resolution()