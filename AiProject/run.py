import subprocess
import webbrowser
import time
import os
from threading import Thread
import sys

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = ['flask', 'flask-cors', 'pymongo']
    
    print("Checking requirements...")
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Missing required package: {package}")
            install = input(f"Would you like to install {package}? (y/n): ")
            if install.lower() == 'y':
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            else:
                print(f"Please install {package} to run the application.")
                return False
    return True

def check_mongodb():
    """Check if MongoDB is accessible"""
    from pymongo import MongoClient
    try:
        client = MongoClient("mongodb+srv://sad22639:saadmongo@sad.hdn6hgp.mongodb.net/?retryWrites=true&w=majority&appName=SAD")
        client.server_info()
        print("MongoDB connection successful")
        return True
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return False

def run_backend():
    print("Starting backend server...")
    try:
        # Change directory to Backend folder
        os.chdir("Backend")
        # Run the Flask application
        subprocess.run([sys.executable, "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting backend: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def open_browser():
    # Wait for the backend server to start
    time.sleep(2)
    print("Opening application in browser...")
    try:
        # Open the login page in the default browser
        webbrowser.open('http://localhost:5000')
    except Exception as e:
        print(f"Error opening browser: {e}")

def main():
    print("Starting Bus Management System...")
    
    # Check requirements first
    if not check_requirements():
        print("Missing requirements. Please install required packages.")
        return
    
    # Check MongoDB connection
    if not check_mongodb():
        print("Cannot connect to MongoDB. Please check your connection.")
        return
    
    # Start backend server in a separate thread
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True  # Thread will be terminated when main program exits
    backend_thread.start()
    
    # Open the browser
    open_browser()
    
    try:
        # Keep the main thread running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main() 