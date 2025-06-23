from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random
from selenium_stealth import stealth
from pypasser import reCaptchaV2

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

cookie_found = False

try:
    driver.get('https://portalbnmp.cnj.jus.br/#/captcha/')
    wait = WebDriverWait(driver, 20)

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')))
    time.sleep(random.uniform(0.5, 1.5))
    wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()
    driver.switch_to.default_content()

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='bframe']")))
    except (TimeoutException, NoSuchElementException):
        pass

    try:
        reCaptchaV2(driver=driver, play=True)
    except Exception:
        pass

    timeout = 15
    end_time = time.time() + timeout
    while time.time() < end_time:
        cookies = driver.get_cookies()
        if any(cookie['name'] == 'portalbnmp' for cookie in cookies):
            cookie_found = True
            break
        time.sleep(1)

except Exception:
    cookie_found = False

finally:
    print(cookie_found)
    if 'driver' in locals() and driver:
        driver.quit()
