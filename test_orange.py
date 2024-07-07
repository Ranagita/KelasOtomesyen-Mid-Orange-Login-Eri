from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.chrome.options import Options
import pytest

@pytest.fixture
def setup():
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach",True)
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.positive
# Positive test case
def test_valid_login(setup):
    setup.find_element(by.XPATH,"//input[@name='username']").send_keys("Admin")
    setup.find_element(by.XPATH,"//input[@name='password']").send_keys("admin123")
    setup.find_element(by.CSS_SELECTOR,".oxd-button").click()
    text = setup.find_element(by.CSS_SELECTOR,".oxd-text--h6").text
    assert text=="Dashboard"

credentials = [
    ('kominfo','Admin123'),
    ('Admin','Admin1234'),
    ('kominfo','Admin1234')
]
@pytest.mark.negative
@pytest.mark.parametrize('username,pswd',credentials)
# negative test case
def test_invalid_login(setup,username,pswd):
    setup.find_element(by.XPATH,"//input[@name='username']").send_keys(username)
    setup.find_element(by.XPATH,"//input[@name='password']").send_keys(pswd)
    setup.find_element(by.CSS_SELECTOR,".oxd-button").click()
    text = setup.find_element(by.CSS_SELECTOR,".oxd-alert-content-text").text
    assert text=="Invalid credentials"


    """
    To run positive test only of the above code, type the below
    pytest test_orange.py -W ignore -m positive --html=positive_login_test_repot.html
    To runs negative test only of the above code, type the below
    pytest test_orange.py -W ignore -m negative --html=negative_login_test_report.html
    To runs complete test, type the below
    pytest test_orange.py -W ignore --html=login_test_report.html
    """