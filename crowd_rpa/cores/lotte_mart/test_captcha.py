# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time
#
# driver = webdriver.Chrome()
#
# driver.get("https://www.google.com.vn/")
#
# image_search = driver.find_element(By.CLASS_NAME, "Gdd5U")
# image_search.click()
#
# upload_image = driver.find_element(By.CLASS_NAME, "DV7the")
# upload_image.click()
#
#
# time.sleep(99)

import pyperclip

# Lấy văn bản đang copy
copied_text = pyperclip.paste()

# In văn bản đang copy
print("Văn bản đang copy:", copied_text)