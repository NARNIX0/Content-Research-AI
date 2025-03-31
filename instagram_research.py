import os
import time
import logging
import platform
import requests
import zipfile
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_research.log'),
        logging.StreamHandler()
    ]
)

class InstagramResearch:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_driver()

    def setup_driver(self):
        """Initialize the Chrome WebDriver with appropriate options."""
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--start-maximized')
            
            # Using Chrome directly without webdriver_manager
            if platform.system() == 'Windows':
                # On Windows, use Edge driver as a fallback if Chrome fails
                try:
                    self.driver = webdriver.Chrome(options=chrome_options)
                except Exception as e:
                    logging.warning(f"Failed to initialize Chrome driver: {str(e)}")
                    logging.info("Trying alternative approach...")
                    
                    # Try with default Chrome driver location
                    try:
                        self.driver = webdriver.Chrome(options=chrome_options)
                    except:
                        # If that fails, try Edge as a fallback
                        from selenium.webdriver.edge.service import Service as EdgeService
                        from selenium.webdriver.edge.options import Options as EdgeOptions
                        
                        edge_options = EdgeOptions()
                        edge_options.add_argument('--start-maximized')
                        self.driver = webdriver.Edge(options=edge_options)
            else:
                # For non-Windows platforms
                self.driver = webdriver.Chrome(options=chrome_options)
                
            self.wait = WebDriverWait(self.driver, 10)
            logging.info("WebDriver initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize WebDriver: {str(e)}")
            raise

    def login_to_instagram(self):
        """Login to Instagram using credentials from .env file."""
        try:
            self.driver.get('https://www.instagram.com/')
            time.sleep(3)  # Wait for page to load

            # Enter username
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(os.getenv('INSTAGRAM_USERNAME'))

            # Enter password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(os.getenv('INSTAGRAM_PASSWORD'))

            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            time.sleep(5)  # Wait for login to complete

            logging.info("Successfully logged in to Instagram")
        except Exception as e:
            logging.error(f"Failed to login: {str(e)}")
            raise

    def search_keyword(self, keyword):
        """Search for a keyword on Instagram."""
        try:
            # Click on search bar
            search_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Search']"))
            )
            search_button.click()
            time.sleep(2)

            # Enter keyword and search
            search_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
            )
            search_input.clear()
            search_input.send_keys(keyword)
            time.sleep(2)
            search_input.send_keys(Keys.ENTER)
            time.sleep(3)

            logging.info(f"Searched for keyword: {keyword}")
        except Exception as e:
            logging.error(f"Failed to search for keyword {keyword}: {str(e)}")
            raise

    def switch_to_reels(self):
        """Switch to the Reels tab in search results."""
        try:
            reels_tab = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/reels/')]"))
            )
            reels_tab.click()
            time.sleep(3)
            logging.info("Switched to Reels tab")
        except Exception as e:
            logging.error(f"Failed to switch to Reels tab: {str(e)}")
            raise

    def scroll_and_collect(self, keyword):
        """Scroll through reels and collect videos with 1M+ views."""
        collected_videos = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while len(collected_videos) < 5:  # Collect at least 5 videos per keyword
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Get all video elements
            video_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/reel/')]")
            
            for video in video_elements:
                try:
                    # Get view count
                    view_count_element = video.find_element(By.XPATH, ".//span[contains(@class, 'view-count')]")
                    view_count_text = view_count_element.text.lower()
                    
                    # Convert view count to number
                    if 'm' in view_count_text:
                        views = float(view_count_text.replace('m', '')) * 1000000
                    else:
                        views = float(view_count_text.replace('k', '')) * 1000

                    if views >= 1000000:  # 1M+ views
                        video_url = video.get_attribute('href')
                        if video_url not in collected_videos:
                            collected_videos.append(video_url)
                            logging.info(f"Found video with {views} views: {video_url}")
                except Exception as e:
                    continue

            # Check if we've reached the bottom
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        return collected_videos

    def process_keywords(self, keywords):
        """Process a list of keywords and collect videos."""
        all_videos = []
        
        for keyword in keywords:
            try:
                self.search_keyword(keyword)
                self.switch_to_reels()
                videos = self.scroll_and_collect(keyword)
                all_videos.extend(videos)
                logging.info(f"Processed keyword: {keyword}, found {len(videos)} videos")
            except Exception as e:
                logging.error(f"Error processing keyword {keyword}: {str(e)}")
                continue

        return all_videos

    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()

def main():
    # List of keywords to search
    keywords = [
        "Nutrition Tips",
        "Weight Loss Tips",
        "healthy recipes",
        "Easy meal prep",
        "High protein meals",
        "Macros explained",
        "Calorie deficit",
        "Nutrition myths",
        "weight loss foods",
        "quick healthy snacks"
    ]

    instagram = None
    try:
        instagram = InstagramResearch()
        instagram.login_to_instagram()
        videos = instagram.process_keywords(keywords)
        logging.info(f"Total videos collected: {len(videos)}")
    except Exception as e:
        logging.error(f"Main process failed: {str(e)}")
    finally:
        if instagram:
            instagram.close()

if __name__ == "__main__":
    main() 