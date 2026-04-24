import subprocess
import webbrowser
import time
import os
import sys

def start_fis_system():
    # 1. Base Directory Setup (ISM Patna Report Format Standard)
    # Taaki script kahin se bhi chale, path sahi pakde
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "public", "index.html")
    
    print("\n" + "="*50)
    print("🌌 FIS PRO (Fabric Inspection System) | INDUSTRIAL ENGINE")
    print("="*50)
    print("🛠️  Mode: Real-Image Pathological Scanning (Knot/Warp/Hole)")
    print("🚀 Version: 2.0 (Stable Production)")
    
    # 2. Local Dashboard Launch
    if os.path.exists(html_path):
        print(f"📡 Status: Launching Local GUI...")
        # Local file path formatting for browser
        webbrowser.open(f'file:///{html_path}', new=2)
    else:
        # Agar local file nahi milti toh online wala link khol dega backup ke liye
        print("⚠️  Warning: Local GUI not found. Launching Cloud Dashboard...")
        webbrowser.open('https://fisv.vercel.app', new=2)

    # 3. Port Check & FastAPI Initialization
    print("⚙️  Status: Initializing FastAPI Backend on Port 8000...")
    time.sleep(1.5) # Smooth transition delay

    try:
        # Windows/Mac/Linux cross-platform command
        python_cmd = sys.executable  # Automatically gets the correct python path
        
        # Running Uvicorn as a module
        subprocess.run([
            python_cmd, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n" + "="*50)
        print("🛑 FIS PRO Engine gracefully stopped by User.")
        print("="*50)
    except Exception as e:
        print(f"❌ Critical Fault: {str(e)}")

if __name__ == "__main__":
    start_fis_system()