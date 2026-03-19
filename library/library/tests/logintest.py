from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


driver.get("http://127.0.0.1:8000/auth/login/")


def login(email_value, password_value):
    email = driver.find_element(By.NAME, "email")
    password = driver.find_element(By.NAME, "password")
    email.click()
    email.clear()
    email.send_keys(email_value)
    password.click()
    password.clear()
    password.send_keys(password_value)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)


def check_login_success(email, password):
    login(email, password)
    try:
        logout = driver.find_element(By.PARTIAL_LINK_TEXT, "Logout")
        print(f"Login success: {email}")
        logout.click()
        time.sleep(1)
        print(f"Successfully log out from {email}")
    except NoSuchElementException:
        print(f"Login failed: invalid password or email")


check_login_success("librarian@gmail.com", "banana52")
check_login_success("librarian@gmail.com", "jasdas")
check_login_success("nsnadsd@gmail.com", "banana52")
check_login_success("pavlo@gmail.com", "banana52")

driver.quit()
