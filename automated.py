from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from multiprocessing import Process, current_process

# Get the absolute path of the project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(PROJECT_DIR, "unknown")

# Ensure the "unknown" folder exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# List of different URLs for each bot
urls = [
    "https://ballchasing.com/?player-name=flitz&pro=1&playlist=6",
    "https://ballchasing.com/?player-name=gyro.&pro=1&playlist=6",
    "https://ballchasing.com/?player-name=hockser&pro=1&playlist=6",
    "https://ballchasing.com/?player-name=lionblaze&pro=1&playlist=6"
]

# Function to run the bot
def run_bot(bot_id, url):
    process_name = current_process().name
    print(f"[{process_name}] Bot {bot_id} started - Visiting: {url}")

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
    # Run Chrome in headless mode to reduce resource usage
    chrome_options.add_argument("--headless")  # Run without UI
    chrome_options.add_argument("--disable-gpu")  # Fix for certain headless issues
    chrome_options.add_argument("--no-sandbox")  # Helps with multiprocessing
    chrome_options.add_argument("--disable-dev-shm-usage")  # Fixes memory issues

    service = Service("C:/Users/Owen/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(url)

        # Scroll down to load all replays
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Find all replay links
        replay_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".replay-title")))

        for i in range(len(replay_links)):
            try:
                replay_links = driver.find_elements(By.CSS_SELECTOR, ".replay-title")

                if i >= len(replay_links):
                    print(f"[{process_name}] Bot {bot_id}: No more replays.")
                    break

                # Scroll into view before clicking
                driver.execute_script("arguments[0].scrollIntoView();", replay_links[i])
                time.sleep(1)

                # Click on the replay link
                replay_links[i].click()
                time.sleep(3)  # Allow the page to load

                # Find and click the "CSV export" button
                download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'CSV export')]")))
                download_button.click()
                time.sleep(3)

                # Find and click the actual CSV download link
                download_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '-team-stats.csv')]")))
                download_link.click()

                print(f"[{process_name}] Bot {bot_id}: Downloaded replay {i + 1}")

                time.sleep(5)  # Wait for download to complete

                # Navigate back to replay list
                driver.back()
                time.sleep(3)
                driver.back()
                time.sleep(3)

            except Exception as e:
                print(f"[{process_name}] Bot {bot_id} - Error on replay {i + 1}: {e}")

    finally:
        driver.quit()
        print(f"[{process_name}] Bot {bot_id} finished.")

# Start multiple bot processes
if __name__ == "__main__":
    processes = []

    for i, url in enumerate(urls):
        p = Process(target=run_bot, args=(i, url), name=f"Bot-{i}")
        p.start()
        processes.append(p)
        time.sleep(5)  # Increased delay to prevent conflicts

    for p in processes:
        p.join()
