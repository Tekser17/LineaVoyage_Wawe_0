import re
import time
from appconnect.email import Email
from appconnect.abc.base_account import BaseAccount
from selenium.webdriver.common.by import By
from croco_selenium.decorators import handle_pop_up
from croco_selenium import silent_send_keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


class Twitter(BaseAccount):
    """This is a class interacting with Twitter"""
    def __init__(self, driver, password: str, email: Email):
        """
        :param driver: Driver to be interacted with
        :param password: Password of a Discord's account
        :param email: Instance of the Email created from Twitter's credentials
        """
        url = 'https://twitter.com/'
        self.timeout = 20
        super().__init__(driver, url, password, email)

    def sign_in(self) -> None:
        """
        Authorizes into the Twitter
        :return: None
        """
        driver = self.driver
        login = self.login
        password = self.password

        driver.get('https://twitter.com/i/flow/login')
        wait = WebDriverWait(driver, 10)

        login_input_xpath = "//input[@name='text']"
        login_input = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, login_input_xpath)))
        silent_send_keys(self.driver, self.timeout, login_input, login)

        continue_button_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[' \
                                '2]/div/div/div/div[6]'

        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, continue_button_xpath)))
        continue_button.click()

        password_input_xpath = "//input[@name='password']"
        password_input = wait.until(EC.element_to_be_clickable((By.XPATH, password_input_xpath)))
        silent_send_keys(self.driver, self.timeout, password_input, password)

        continue_button_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[' \
                                '2]/div/div[1]/div/div/div'
        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, continue_button_xpath)))
        continue_button.click()

        try:
            code_input_xpath = '//input[@data-testid="ocfEnterTextTextInput"]'
            code_input = wait.until(EC.element_to_be_clickable((By.XPATH, code_input_xpath)))
        except:
            pass
        else:
            code = self.__get_verifying_code()
            silent_send_keys(self.driver, self.timeout, code_input, code)

            submit_button_xpath = '//div[@data-testid="ocfEnterTextNextButton"]'
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
            submit_button.click()
            time.sleep(8)

    def __get_verifying_code(self) -> str:
        body = self.email.get_mails_by_sender('info@x.com')[-1]
        pattern = r'(?<=is\s)(\S+)'
        code = re.search(pattern, body).group(1)
        if not code:
            raise Exception("Code isn't parsed")
        return code

    @handle_pop_up()
    def connect(self) -> None:
        """
        Performs the third-party Twitter connection
        :return: None
        """
        WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="OAuth_Consent_Button"]'))).click()

    @handle_pop_up()
    def connect_v1(self) -> None:
        """
        Performs enabling Twitter V1 API
        :return: None
        """
        WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@id="allow"]'))).click()
