#!/usr/bin/env python3
"""
Quick script to restart Django server
"""

import subprocess
import sys
import os

def restart_django_server():
    """Restart the Django development server"""
    print("🔄 Restarting Django Server...")
    print("=" * 40)
    
    try:
        # Change to backend directory
        os.chdir('npc-reporting-system/backend')
        
        print("📍 Current directory:", os.getcwd())
        print("🚀 Starting Django server...")
        
        # Start the server
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n⏹️ Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    restart_django_server()