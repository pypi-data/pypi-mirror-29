from selenium import webdriver
import time


class BaseSelenium():

    def __init__(self):
        self.browser = webdriver.Firefox()
        self.timeout = 2

    def set_timeout(self, timeout):
        # Sets the max timeout to wait until the page loads
        self.timeout = timeout

    def save_screencap(self, url, file_name="screencap", path="testing"):
        print("[INFO] Loading URL")
        self.browser.get(url)
        time.sleep(self.timeout)
        file_path = "{}/{}.png".format(path, file_name)
        print("[INFO] Saving screenshot as {}".format(file_path))
        self.browser.save_screenshot(file_path)

    def close_browser(self):
        self.browser.quit()
