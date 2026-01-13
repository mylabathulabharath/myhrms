#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    print("=== Starting Horilla Deployment ===")
    
    # Step 1: Run makemigrations
    print("Step 1: Making migrations...")
    result = subprocess.run([sys.executable, "manage.py", "makemigrations"], 
                          capture_output=True, text=True)
    if result.returncode != 0 and "No changes detected" not in result.stdout:
        print(f"Makemigrations output: {result.stdout}")
        if result.stderr:
            print(f"Makemigrations errors: {result.stderr}")
    else:
        print("Migrations check complete")
    
    # Step 2: Run migrate
    print("Step 2: Running migrations...")
    result = subprocess.run([sys.executable, "manage.py", "migrate"], 
                          check=True)
    print("Migrations applied successfully")
    
    # Step 3: Compile messages (for translations)
    print("Step 3: Compiling translations...")
    result = subprocess.run([sys.executable, "manage.py", "compilemessages"],
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("Translations compiled successfully")
    else:
        print(f"Translation compilation: {result.stdout}")
        # Don't fail if compilemessages has issues
    
    # Step 4: Get PORT and start Gunicorn
    port = os.environ.get('PORT', '10000')
    print(f"Step 4: Starting Gunicorn on port {port}...")
    
    # Start Gunicorn
    os.execvp('gunicorn', [
        'gunicorn',
        'horilla.wsgi:application',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--timeout', '120',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--log-level', 'info',
        '--preload'
    ])

if __name__ == '__main__':
    main()
