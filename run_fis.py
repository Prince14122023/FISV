import subprocess
import webbrowser
import time
import os
import sys

def start_fis_system():
    # 1. HTML file ka local path nikalna
    current_dir = os.getcwd()
    html_path = os.path.join(current_dir, "public", "index.html")
    
    print("🌌 Starting FIS (Fabric Inspection System) PRO Engine...")
    print("🛠️  Initializing 13-Defect Logic & Ultra-Modern UI...")

    # 2. Browser mein dashboard kholna (2 sec delay ke saath)
    # Taaki backend ko initialize hone ka time mile
    if os.path.exists(html_path):
        print(f"🚀 Launching Industrial Dashboard: {html_path}")
        webbrowser.open(f'file:///{html_path}', new=2)
    else:
        print("❌ Error: public/index.html nahi mili! Path check karein.")

    # 3. FastAPI Server (Uvicorn) start karna
    # Hum 'api.main:app' use kar rahe hain kyunki file api folder mein hai
    try:
        # Windows par 'py', Mac/Linux par 'python3'
        cmd = "py" if sys.platform == "win32" else "python3"
        subprocess.run([cmd, "-m", "uvicorn", "api.main:app", "--reload", "--port", "8000"], shell=True)
    except KeyboardInterrupt:
        print("\n🛑 FIS PRO Engine gracefully stopped.")

if __name__ == "__main__":
    start_fis_system()