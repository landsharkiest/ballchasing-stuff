from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "unknown/",  # Set download directory
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
})

service = Service("C:/Users/Owen/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the page with replays
driver.get("https://ballchasing.com/?player-name=daniel&pro=1&playlist=6")
wait = WebDriverWait(driver, 10)  # Increased wait time

# Scroll down to load all replays
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)  # Allow page to load

# Find all replay links
replay_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".replay-title")))

for i in range(len(replay_links)):
    try:
        # Refresh replay list before clicking
        replay_links = driver.find_elements(By.CSS_SELECTOR, ".replay-title")

        if i >= len(replay_links):
            print(f"Skipping replay {i + 1} - No more elements found.")
            break  # Avoid out-of-range errors

        # Scroll into view before clicking
        driver.execute_script("arguments[0].scrollIntoView();", replay_links[i])
        time.sleep(1)

        # Click on the replay link
        replay_links[i].click()
        time.sleep(3)  # Allow the page to load

        # Find and click the "CSV export" button
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'CSV export')]")))
        download_button.click()
        time.sleep(3)  # Allow download link to appear

        # Find and click the actual CSV download link
        download_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '-team-stats.csv')]")))
        download_link.click()

        print(f"Downloaded replay {i + 1}")

        time.sleep(5)  # Wait for download to complete

        # Navigate back to replay list
        driver.back()
        time.sleep(3)  # Allow the page to reload
        driver.back()
        time.sleep(3)

    except Exception as e:
        print(f"Error on replay {i + 1}: {e}")

# Close browser after completion
driver.quit()
