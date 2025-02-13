from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from multiprocessing import Process

# List of different URLs for each bot
urls = [
    "https://ballchasing.com/?player-name=flitz&pro=1&playlist=6",
    "https://ballchasing.com/?player-name=gyro.&pro=1&playlist=6",
    "https://ballchasing.com/?player-name=hockser&pro=1&playlist=6",
    "https://ballchasing.com/?player-name=lionblaze&pro=1&playlist=6"
]

# Set up Selenium WebDriver
def run_bot(bot_id, url):
    print(f"Bot {bot_id} started - Visiting: {url}")

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "C:/Users/Owen/Downloads/ballchasing stuff/unknown/",  # Unique folder per bot
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    })

    service = Service("C:/Users/Owen/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        # Open the page with replays
        driver.get(url)

        # Scroll down to load all replays
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Find all replay links
        replay_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".replay-title")))

        for i in range(len(replay_links)):
            try:
                # Refresh replay list before clicking
                replay_links = driver.find_elements(By.CSS_SELECTOR, ".replay-title")

                if i >= len(replay_links):
                    print(f"Bot {bot_id}: Skipping replay {i + 1} - No more elements found.")
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

                print(f"Bot {bot_id}: Downloaded replay {i + 1}")

                time.sleep(5)  # Wait for download to complete

                # Navigate back to replay list
                driver.back()
                time.sleep(3)
                driver.back()
                time.sleep(3)

            except Exception as e:
                print(f"Bot {bot_id} - Error on replay {i + 1}: {e}")

    finally:
        driver.quit()
        print(f"Bot {bot_id} finished.")

# Start multiple bot processes
if __name__ == "__main__":
    processes = []

    for i, url in enumerate(urls):
        p = Process(target=run_bot, args=(i, url))
        p.start()
        processes.append(p)
        time.sleep(2)  # Small delay to avoid overwhelming the server

    for p in processes:
        p.join()
