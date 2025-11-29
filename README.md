# QA-Engineer-Technical-Assessment
---

BlazeDemo Automation — Setup & How to Run

This project contains automated tests for the BlazeDemo flight booking website.
It uses Python, Selenium, Pytest, and HTML reports, and follows the Page Object Model structure.

The goal is simple: run end-to-end tests that search for flights, select one, enter user information, and verify the booking result.


1. How to Set Up the Environment

Follow these steps before running the tests.


Step 1: Install Python

If you don’t already have Python (version 3.10 or newer), download it from:

[https://www.python.org/downloads/](https://www.python.org/downloads/)


Step 2: Install the required libraries

Open Command Prompt inside your project folder and run:

pip install selenium pytest pytest-html webdriver-manager


2. How to Run the Tests

 Run the script directly

```
python Automation.py
```

This will automatically run Pytest and generate the HTML report as well.


3. Project Files

```
Automation.py      → Main automation code + test cases
README.md          → Instructions (this file)
automation.log     → Log file (generated automatically)
report.html        → Test results (generated after running pytest)
```

---

4. What the Tests Do

Each test:

* Opens BlazeDemo
* Selects a departure & destination city
* Picks a flight
* Fills the purchase form with random data
* Confirms the order
* Checks the price and booking status
* Logs everything and produces an HTML report

There are also negative tests—for example, testing invalid flight numbers or selecting the same departure and destination.


5. Adding More Tests

If you want to add your own test, just create a new def function in the file:

def test_custom_trip(driver):
    purchaseEndToEnd(driver, "Paris", "Rome", 3)

Pytest will find it automatically.

---
Done, Thanks for your time!

Regards,
Sultan Alkanain


