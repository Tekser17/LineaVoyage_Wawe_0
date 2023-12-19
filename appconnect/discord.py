import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from croco_selenium.decorators import handle_pop_up
from croco_selenium.actions import silent_send_keys
from appconnect.email import Email
from appconnect.abc import BaseAccount
from appconnect.captcha import CaptchaWaiter, CaptchaType
from typing import Optional


class Discord(BaseAccount):
    """This is a class interacting with Discord"""
    def __init__(self, driver, password: str, email: Email, token: Optional[str] = None):
        """
        The fast way to sign in into a Discord account is passing authentication token with other arguments
        :param driver: Driver to be interacted with
        :param password: Password of a Discord's account
        :param email: Instance of the Email created from Discord's credentials
        :param token: Authentication token
        """
        url = 'https://discord.com'
        super().__init__(driver, url, password, email)
        self.__token = token

    @property
    def token(self) -> str | None:
        """
        Returns authentication token
        :return: str
        """
        return self.__token

    def __enter_credentials(self) -> None:
        driver = self.driver

        login_input = WebDriverWait(driver, 150).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@name="email"]')))
        silent_send_keys(login_input, self.login)

        password_input = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]')))
        silent_send_keys(password_input, self.password)

        WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).click()

    def sign_in(self) -> None:
        """
        Authorizes into the Discord. If you have no an authentication token or don't pass it and log in from a
        different proxy than the last time you logged in, you need to use Capmonster or another captcha-solving tool.
        :return: None
        """
        driver = self.driver
        if self.token:
            driver.get('https://discord.com')
            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//body")))
            js = """let token = "%s";

                    function login(token) {
                        setInterval(() => {
                          document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                        }, 50);
                        setTimeout(() => {
                          location.reload();
                        }, 2500);
                      }
                    
                    login(token);
                    """ % self.token
            driver.execute_script(js)
            time.sleep(5)
        else:
            driver.get('https://discord.com/login')
            self.__enter_credentials()

            try:
                CaptchaWaiter.wait_for_solving(driver, CaptchaType.H_CAPTCHA)
            except:
                pass

            verifying_urls = self.email.search_content(r'https:\/\/click\.discord\.com\/ls\/click\?upn=[^\s/$.?#].[^\s]*')
            if verifying_urls is not None:
                verifying_url = verifying_urls[-2]
                driver.get(verifying_url)

                submit_button_xpath = '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/section/div[2]/button'
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, submit_button_xpath))).click()
                try:
                    self.__enter_credentials()
                except:
                    pass
            time.sleep(5)

    @handle_pop_up()
    def connect(self) -> None:
        """
        Performs the third-party Discord connection
        :return: None
        """
        driver = self.driver
        WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/div/div[2]/button[2]'))).click()

