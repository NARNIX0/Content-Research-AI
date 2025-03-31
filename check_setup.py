import os
import sys
import platform
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_chrome_installed():
    """Check if Chrome is installed on the system."""
    try:
        system = platform.system()
        if system == 'Windows':
            # Paths to check for Chrome on Windows
            chrome_paths = [
                os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Google\\Chrome\\Application\\chrome.exe'),
                os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Google\\Chrome\\Application\\chrome.exe'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google\\Chrome\\Application\\chrome.exe')
            ]
            
            for path in chrome_paths:
                if os.path.exists(path):
                    logging.info(f"Chrome found at: {path}")
                    return True
            
            logging.error("Chrome not found. Please install Chrome browser.")
            return False
        
        elif system == 'Darwin':  # macOS
            try:
                subprocess.run(['open', '-a', 'Google Chrome'], check=True)
                logging.info("Chrome is installed on macOS.")
                return True
            except subprocess.CalledProcessError:
                logging.error("Chrome not found on macOS. Please install Chrome browser.")
                return False
        
        elif system == 'Linux':
            try:
                subprocess.run(['which', 'google-chrome'], check=True, stdout=subprocess.PIPE)
                logging.info("Chrome is installed on Linux.")
                return True
            except subprocess.CalledProcessError:
                logging.error("Chrome not found on Linux. Please install Chrome browser.")
                return False
        
        else:
            logging.error(f"Unsupported operating system: {system}")
            return False
            
    except Exception as e:
        logging.error(f"Error checking Chrome installation: {str(e)}")
        return False

def check_environment():
    """Check the Python environment and dependencies."""
    logging.info(f"Python version: {platform.python_version()}")
    logging.info(f"Operating System: {platform.system()} {platform.version()}")
    
    # Check for required packages
    try:
        import selenium
        logging.info(f"Selenium version: {selenium.__version__}")
    except ImportError:
        logging.error("Selenium is not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import dotenv
        # python-dotenv doesn't have a __version__ attribute in the dotenv module
        logging.info("python-dotenv is installed")
    except ImportError:
        logging.error("python-dotenv is not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import requests
        logging.info(f"requests version: {requests.__version__}")
    except ImportError:
        logging.error("requests is not installed. Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all checks and report status."""
    logging.info("Starting environment check...")
    
    env_check = check_environment()
    chrome_check = check_chrome_installed()
    
    if env_check and chrome_check:
        logging.info("✓ All checks passed. You should be able to run the script.")
        return True
    else:
        logging.warning("❌ Some checks failed. Please resolve the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 