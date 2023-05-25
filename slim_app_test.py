# from selenium.webdriver import ActionChains
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions
# import time
# from selenium.webdriver.support.select import Select
# import logger
# import pytest

# # @pytest.mark.usefixtures()
# class Test_class(logger):
#         def test_signup(self):

#             chrome_driver_path = ChromeDriverManager().install()
#             chrome_options = Options()
#             chrome_options.add_experimental_option("detach", True)
#             service_obj = Service(chrome_driver_path)
#             driver = webdriver.Chrome(service=service_obj, options=chrome_options)
#             driver.implicitly_wait(5)
#             driver.get("http://0.0.0.0:5000")
#             name = 'eldad'
#             log = self.log_conf()
#             driver.find_element(By.XPATH, "//input[@name='username']").send_keys(name) 
#             driver.find_element(By.XPATH, "//input[@name='password']").send_keys("password13445")
#             driver.find_element(By.XPATH, "//input[@value='signup']").click()
#             element = driver.find_element(By.XPATH, "//body")
#             expected_text = f"Hello {name}!"
#             actual_text = element.text
#             assert expected_text == actual_text, f"Expected '{expected_text}', but found '{actual_text}'"


#             try:
#                         assert expected_text == f"Hello {name}"
#             except AssertionError as msg:
#                         log.error(msg)
#                         raise AssertionError(msg)
#             else:
#                         log.info("Test Passed successfully")

from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from selenium.webdriver.support.select import Select
from logger import BaseClass
import pytest


class TestClass(BaseClass):
    def test_signup(self):
        chrome_driver_path = ChromeDriverManager().install()
        chrome_options = Options()
        chrome_options.add_argument("--headless", "--no-sandbox")
        chrome_options.add_experimental_option("detach", True)
        service_obj = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service_obj, options=chrome_options)
        driver.implicitly_wait(5)
        driver.get("http://44.204.12.118:5000")
        name = 'eldad'
        log = self.log_conf()
        driver.find_element(By.XPATH, "//input[@name='username']").send_keys(name)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys("password13445")
        driver.find_element(By.XPATH, "//input[@value='signup']").click()
        element = driver.find_element(By.XPATH, "//body")
        expected_text = f"Hello {name}!"
        actual_text = element.text
        assert expected_text == actual_text, f"Expected '{expected_text}', but found '{actual_text}'"

        try:
            assert expected_text == f"Hello {name}!"
        except AssertionError as msg:
            log.error(msg)
            raise AssertionError(msg)
        else:
            log.info("Test Passed successfully")


if __name__ == '__main__':
    pytest.main([__file__])

