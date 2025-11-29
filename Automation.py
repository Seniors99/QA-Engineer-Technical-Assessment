"""
Selenium WebDriver Automation - BlazeDemo Flight Purchase
Language: Python
Pattern: Page Object Model (POM)
Test Framework: Pytest (Assertions)
HTML Reporting: pytest-html
"""

import random
import string
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# ---------------------------------------
# Logging Setup
# ---------------------------------------
logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Automation Script Started")

# ---------------------------------------
# Utility Functions
# ---------------------------------------
def random_string(n=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))

def random_number(n=6):
    return ''.join(random.choice(string.digits) for _ in range(n))

# ---------------------------------------
# Base Page
# ---------------------------------------
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_click(self, locator): #waits until an element is clickable and clicks it.
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def wait_visible(self, locator): #waits until an element is visible and returns it.
        return self.wait.until(EC.visibility_of_element_located(locator))

# ---------------------------------------
# Page Objects
# ---------------------------------------
class HomePage(BasePage):
    URL = "https://blazedemo.com/"

    def open(self):
        self.driver.get(self.URL)

    def select_departure(self, city):
        Select(self.driver.find_element(By.NAME, "fromPort")).select_by_visible_text(city)

    def select_destination(self, city):
        Select(self.driver.find_element(By.NAME, "toPort")).select_by_visible_text(city)

    def click_find_flights(self):
        self.wait_click((By.CSS_SELECTOR, "input[type='submit']"))
        return FlightsPage(self.driver)

class FlightsPage(BasePage):
    def select_flight(self, flightSeq):
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        if flightSeq < 1 or flightSeq > len(rows):
            raise ValueError(f"Invalid flight number {flightSeq}. Only {len(rows)} flights available.")
        rows[flightSeq - 1].find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        return PurchasePage(self.driver)

class PurchasePage(BasePage):
    def fill_user_data(self, name, address, city, state, zip, card):
        self.driver.find_element(By.ID, "inputName").send_keys(name)
        self.driver.find_element(By.ID, "address").send_keys(address)
        self.driver.find_element(By.ID, "city").send_keys(city)
        self.driver.find_element(By.ID, "state").send_keys(state)
        self.driver.find_element(By.ID, "zipCode").send_keys(zip)
        self.driver.find_element(By.ID, "creditCardNumber").send_keys(card)

    def click_purchase(self):
        self.wait_click((By.CSS_SELECTOR, "input[type='submit']"))
        return ConfirmationPage(self.driver)

class ConfirmationPage(BasePage):
    def get_status(self): #returns flight purchase status (e.g., "PendingCapture").
        return self.wait_visible((By.XPATH, "//td[.='Status']/following-sibling::td")).text

    def get_price(self): #extracts and converts the purchase price to float.
        price_text = self.wait_visible((By.XPATH, "//td[.='Amount']/following-sibling::td")).text
        cleaned = price_text.replace('$', '').replace('USD', '').strip()
        return float(cleaned)

# ---------------------------------------
# Core Function (End-to-End)
# ---------------------------------------
def purchaseEndToEnd(driver, deptCity=None, desCity=None, flightSeq=None):
    dept_cities = ["Paris", "Philadelphia", "Boston", "Portland", "San Diego", "Mexico City", "São Paolo"]
    des_cities = ["Rome", "New York", "London", "Berlin", "Dublin", "Cairo"]

    deptCity = deptCity if deptCity else random.choice(dept_cities)
    desCity = desCity if desCity else random.choice(des_cities)
    flightSeq = flightSeq if flightSeq is not None else random.randint(1, 5)

    # Validations
    if deptCity == desCity:
        raise ValueError("Departure and destination cannot be the same.")
    if deptCity not in dept_cities:
        raise ValueError(f"Invalid departure city: {deptCity}")
    if desCity not in des_cities:
        raise ValueError(f"Invalid destination city: {desCity}")
    if flightSeq < 1:
        raise ValueError("Flight number must be >= 1.")

    logging.info(f"=== Running Test: {deptCity} → {desCity}, Flight #{flightSeq} ===")

    home = HomePage(driver)
    home.open()
    home.select_departure(deptCity)
    home.select_destination(desCity)
    flights = home.click_find_flights()
    purchase = flights.select_flight(flightSeq)

    # Random user data
    name = random_string()
    address = random_string(6)
    city = random_string(5)
    state = random_string(4)
    zip_code = random_number(5)
    card = random_number(12)

    purchase.fill_user_data(name, address, city, state, zip_code, card)
    confirm = purchase.click_purchase()

    status = confirm.get_status()
    price = confirm.get_price()

    assert status == "PendingCapture", f"❌ Status mismatch: {status}"
    assert price > 100.0, f"❌ Price too low: {price}"

    logging.info(f"✔ Test Passed – Status: {status}, Price: ${price}")

# ---------------------------------------
# Pytest Fixture
# ---------------------------------------
@pytest.fixture
def driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    yield driver
    driver.quit()

# ---------------------------------------
# Pytest Tests
# ---------------------------------------
def test_case_1(driver):
    purchaseEndToEnd(driver, "Boston", "Berlin", 2)

def test_case_2_random(driver):
    purchaseEndToEnd(driver)

def test_invalid_same_city(driver):
    with pytest.raises(ValueError):
        purchaseEndToEnd(driver, "Boston", "Boston", 1)

def test_invalid_flight_number(driver):
    with pytest.raises(ValueError):
        purchaseEndToEnd(driver, "Paris", "Berlin", 0)



def test_case_custom(driver):
    purchaseEndToEnd(driver, "Paris", "London", 3)

# ---------------------------------------
# Run Directly via Pytest
# ---------------------------------------
if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html", __file__])
