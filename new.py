import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
import json
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
profile = "C:\\Users\\bouka\\AppData\\Local\\Google\\Chrome\\User Data"
chrome_options.add_argument(f"user-data-dir={profile}")
s = 0
# Set up the ChromeDriver service
service = ChromeService(ChromeDriverManager().install())

# Create a new instance of the Chrome driver with undetected_chromedriver
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("ChromeDriver initialized successfully.")
except Exception as e:
    print("-------------------------------------------------------")
    print(f"Failed to initialize ChromeDriver: {e}")
    print("-------------------------------------------------------")
    exit(1)

# Define directories
root_directory = r'C:\Users\bouka\OneDrive\Bureau\photos\takeout-20240828T024210Z-001\Takeout\Google Photos'
output_directory = r'C:\Users\bouka\OneDrive\Bureau\teste'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through all directories and subdirectories to find JSON files
for dirpath, dirnames, filenames in os.walk(root_directory):
    for filename in filenames:
        if filename.endswith('.json'):
            json_path = os.path.join(dirpath, filename)
            print(f"Processing file: {json_path}")
            s += 1
            # Read the JSON file
            try:
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)

                    # Extract the file URL
                    file_url = data.get('url')
                    if file_url:
                        # Open the URL in Selenium
                        try:
                            driver.get(file_url)
                            print(f"Accessing URL: {file_url}")

                            # Wait for the page to load
                            time.sleep(10)  # Adjust as necessary

                            # Create an ActionChains object
                            actions = ActionChains(driver)

                            # Press Shift + D
                            actions.key_down(Keys.SHIFT).send_keys('d').key_up(Keys.SHIFT).perform()
                            print("Pressed Shift + D to download.")

                        except Exception as e:
                            print(f"Failed to open URL {file_url}: {e}")
            except FileNotFoundError as e:
                print(f"File not found: {json_path}")
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON file {json_path}: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

print(f"THE TOTAL LOOPED FILES ARE : {s}")

# Close the driver
try:
    driver.quit()
    print("ChromeDriver closed successfully.")
except Exception as e:
    print(f"Failed to close the ChromeDriver: {e}")
