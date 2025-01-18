# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# import time

# # Initialize the Chrome driver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# try:
#     # Navigate to the Dino game page
#     driver.get("https://chrome-dino-game.github.io/")
#     time.sleep(2)  # Wait for the page to load

#     # Create an ActionChains object
#     actions = ActionChains(driver)

#     # Start the game by pressing the space bar
#     actions.send_keys(Keys.SPACE).perform()
#     time.sleep(1)  # Wait for the game to start

#     # Game loop to simulate jumping and other actions
#     for _ in range(10):  # Adjust the range for how long you want to play
#         # Simulate pressing the space key to jump
#         actions.send_keys(Keys.SPACE).perform()
#         time.sleep(1)  # Adjust the sleep time as needed

#         # You can also simulate pressing the up arrow key
#         actions.send_keys(Keys.ARROW_UP).perform()
#         time.sleep(1)  # Adjust the sleep time as needed

#         # Simulate pressing the down arrow key
#         actions.send_keys(Keys.ARROW_DOWN).perform()
#         time.sleep(1)  # Adjust the sleep time as needed

# except Exception as e:
#     print(f"An error occurred: {e}")

# finally:
#     # Close the browser
#     driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from PIL import Image
import os
from io import BytesIO
from selenium.webdriver.common.by import By
# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Navigate to the Dino game page
driver.get("https://chrome-dino-game.github.io/")
time.sleep(2)  # Wait for the page to load

    # Find all image elements
images = driver.find_elements(By.TAG_NAME, 'img')

# Create a directory to save images
os.makedirs('images', exist_ok=True)

# Download each image
for index, img in enumerate(images):
    img_url = img.get_attribute('src')
    if img_url:
        try:
            response = requests.get(img_url)
            with open(f'images/image_{index}.png', 'wb') as file:
                file.write(response.content)
            print(f'Downloaded: image_{index}.png')
        except Exception as e:
            print(f'Error downloading {img_url}: {e}')

# Close the WebDriver
driver.quit()
