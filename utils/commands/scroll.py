
from selenium.webdriver.common.by import By # type: ignore

def scroll(driver):
  driver.execute_script(
          'window.scrollBy({ top: 600, behavior: "smooth" });',
        )
       
def scroll_post(driver):
  driver.execute_script(
          'window.scrollBy({ top: 2000, behavior: "smooth" });',
        )