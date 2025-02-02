import os
import subprocess
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory where the script is located
INPUT_FILE = os.path.join(SCRIPT_DIR, "list.txt")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "url_list.txt")
UNLINKED_FILE = os.path.join(SCRIPT_DIR, "unlinked.txt")  # File for failed queries
RUN_SCRIPT = os.path.join(SCRIPT_DIR, "run.sh")  # Path to run.sh
YOUTUBE_MUSIC_URL = "https://music.youtube.com"

# XPaths stored as variables to avoid repetition
MENU_BUTTON_XPATH = '/html/body/ytmusic-app/ytmusic-app-layout/div[4]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[2]/ytmusic-card-shelf-renderer/div/div[2]/div[2]/ytmusic-menu-renderer/yt-button-shape/button'
SHARE_BUTTON_XPATH = "//a[@id='navigation-endpoint' and contains(@class, 'yt-simple-endpoint') and contains(@class, 'style-scope') and contains(., 'Share')]"
COPY_BUTTON_XPATH = '/html/body/ytmusic-app/ytmusic-popup-container/tp-yt-paper-dialog[1]/ytmusic-unified-share-panel-renderer/div[3]/yt-third-party-network-section-renderer/div[2]/yt-copy-link-renderer/div/yt-button-renderer/yt-button-shape/button'
CLOSE_SHARE_PANEL_XPATH = '/html/body/ytmusic-app/ytmusic-popup-container/tp-yt-paper-dialog/ytmusic-unified-share-panel-renderer/div[1]/tp-yt-paper-icon-button'

def setup_driver():
    """Sets up the WebDriver with Firefox."""
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    driver.get(YOUTUBE_MUSIC_URL)
    return driver

def reject_cookies(driver):
    """Rejects cookies only once at the beginning."""
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button')
            )
        )
        reject_button = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button')
        reject_button.click()
        print("Cookies rejected")
    except Exception as e:
        print("Cookie rejection button not found or already accepted.")

def search_for_music(driver, query):
    """Searches for the music query in the search box."""
    search_box = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@id="input"]'))
    )
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)  # Simulate hitting Enter
    print(f"Searching for {query}...")
    time.sleep(1)  # Reduced wait time

def wait_for_page_to_load(driver):
    """Waits for the page to load by checking for the presence of the menu button."""
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, MENU_BUTTON_XPATH))
        )
        print("Search results loaded.")
        return True
    except TimeoutException:
        print("Page load timed out or menu button not found.")
        return False

def click_menu_button(driver):
    """Clicks on the menu button, reloads if unable to click."""
    retry_count = 2  # Reduced retry count
    while retry_count > 0:
        try:
            menu_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, MENU_BUTTON_XPATH))
            )
            menu_button.click()
            print("Menu button clicked.")
            time.sleep(1)  # Reduced wait time
            return True
        except TimeoutException:
            retry_count -= 1
            print(f"Menu button timeout, retrying {retry_count} more time(s).")
            time.sleep(1)  # Reduced wait before retrying
    print("Timeout occurred while waiting for the menu button.")
    return False

def click_share_button(driver):
    """Clicks the share button, reloads if unable to click."""
    retry_count = 2
    while retry_count > 0:
        try:
            share_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, SHARE_BUTTON_XPATH))
            )
            share_button.click()
            print("Share button clicked.")
            time.sleep(1)  # Reduced wait time
            return True
        except TimeoutException:
            retry_count -= 1
            print(f"Share button timeout, retrying {retry_count} more time(s).")
            time.sleep(1)  # Reduced wait before retrying
    print("Timeout occurred while waiting for the share button.")
    return False

def click_copy_button(driver):
    """Clicks the 'Copy' button to copy the share URL."""
    retry_count = 2
    while retry_count > 0:
        try:
            copy_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, COPY_BUTTON_XPATH))
            )
            copy_button.click()
            time.sleep(1)  # Reduced wait time after clicking
            print("Copy button clicked.")
            return True
        except TimeoutException:
            retry_count -= 1
            print(f"Copy button timeout, retrying {retry_count} more time(s).")
            time.sleep(1)  # Reduced wait before retrying
    print("Timeout occurred while waiting for the copy button.")
    return False

def get_share_url_from_clipboard():
    """Retrieves the copied URL from the clipboard."""
    time.sleep(1)  # Reduced sleep time to 1 second
    share_url = pyperclip.paste()
    
    # Debugging - print the clipboard contents to verify if the URL is copied
    print(f"Clipboard content: {share_url}")
    
    if not share_url:
        print("Share URL not found in clipboard.")
        return None
    return share_url

def close_share_panel(driver):
    """Closes the share panel."""
    try:
        close_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, CLOSE_SHARE_PANEL_XPATH))
        )
        close_button.click()
        print("Share panel closed.")
    except TimeoutException:
        print("Timeout occurred while closing the share panel.")

def reload_and_retry(driver, query):
    """Reloads the page, re-enters the search query, and retries the process."""
    print("Reloading the page and re-inputting the query.")
    driver.refresh()
    time.sleep(2)  # Reduced wait for the page to reload
    search_for_music(driver, query)
    if not wait_for_page_to_load(driver):
        return None

    # After reloading, go through the process again: menu, share, copy
    if not click_menu_button(driver):
        return None
    if not click_share_button(driver):
        return None
    if not click_copy_button(driver):
        return None
    return True

def process_music_query(driver, query):
    """Handles the entire process of searching, copying the URL, and returning it."""
    reject_cookies(driver)  # Reject cookies only once
    search_for_music(driver, query)
    if not wait_for_page_to_load(driver):  # Ensure the page has fully loaded
        return None

    # Try to click the menu button, reload if unable to click
    if not click_menu_button(driver):
        if not reload_and_retry(driver, query):
            return None
        # After reload, go through the sequence: menu -> share -> copy
        if not click_menu_button(driver):
            return None
    
    # Try to click the share button, reload if unable to click
    if not click_share_button(driver):
        if not reload_and_retry(driver, query):
            return None
        # After reload, go through the sequence: menu -> share -> copy
        if not click_share_button(driver):
            return None
    
    # Try to click the copy button, reload if unable to click
    if not click_copy_button(driver):
        if not reload_and_retry(driver, query):
            return None
        # After reload, go through the sequence: menu -> share -> copy
        if not click_copy_button(driver):
            return None
    
    share_url = get_share_url_from_clipboard()
    if share_url:
        close_share_panel(driver)
    return share_url

def get_last_processed_url_index():
    """Returns the index of the last processed URL from OUTPUT_FILE."""
    if not os.path.exists(OUTPUT_FILE):
        return -1  # No URLs processed yet
    
    with open(OUTPUT_FILE, 'r') as file:
        lines = file.readlines()
        if not lines:
            return -1
        last_url = lines[-1].strip()
        return len(lines)  # The number of processed URLs (starting from 0)

def ensure_files_exist():
    """Creates output and unlinked files if they do not already exist."""
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'w') as file:
            pass  # Just create an empty file if it doesn't exist
        print(f"Created new file: {OUTPUT_FILE}")

    if not os.path.exists(UNLINKED_FILE):
        with open(UNLINKED_FILE, 'w') as file:
            pass  # Just create an empty file if it doesn't exist
        print(f"Created new file: {UNLINKED_FILE}")

def process_file():
    """Reads the input file, processes each name, and saves share URLs to the output file."""
    ensure_files_exist()  # Ensure the files exist before proceeding
    
    with open(INPUT_FILE, 'r') as file:
        names = [line.strip() for line in file.readlines()]

    # Get the last processed index
    last_index = get_last_processed_url_index()

    if last_index == -1:
        print("No URLs have been processed yet. Starting fresh.")
    else:
        print(f"Resuming from index {last_index}.")

    total_names = len(names)  # Total number of names to process
    driver = setup_driver()  # Start the browser session

    # Open the output files for appending
    with open(OUTPUT_FILE, 'a') as output_file, open(UNLINKED_FILE, 'a') as unlinked_file:
        for index, name in enumerate(names[last_index:], start=last_index):
            print(f"Processing: {name}")
            url = process_music_query(driver, name)
            if url:
                output_file.write(f"{url}\n")  # Write the URL to the file
                output_file.flush()  # Flush to ensure data is written immediately
                print(f"Added URL: {url}")
            else:
                unlinked_file.write(f"{name}\n")  # Write the failed query to unlinked file
                unlinked_file.flush()  # Flush to ensure data is written immediately
                print(f"Added '{name}' to unlinked.")

            # Display progress as a percentage
            processed_count = index + 1  # Number of names processed (index is 0-based)
            progress_percentage = (processed_count / total_names) * 100
            print(f"Progress: {processed_count}/{total_names} ({progress_percentage:.2f}%)")

    # Quit the driver after all operations are done
    driver.quit()

    # After all processing, run the shell script
    run_shell_script()


def run_shell_script():
    """Runs the run.sh script after processing."""
    try:
        print("Running run.sh script...")
        subprocess.run([RUN_SCRIPT], check=True, shell=True)
        print("run.sh executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running run.sh: {e}")

if __name__ == "__main__":
    process_file()