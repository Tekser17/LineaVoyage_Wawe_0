import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from croco_selenium_actions import switch_to_another_window
from croco_selenium_actions.decorators import handle_pop_up
from typing import Literal, cast, Self
from appconnect.common import Wallet


_SigningType = Literal['create', 'import']


class Metamask(Wallet):
    """This is a class interacting with Metamask"""
    def __init__(
            self,
            driver: WebDriver,
            password: str,
            mnemonic: str,
            extension_id: str = 'nkbihfbeogaeaoehlefnkodbefgpgknn'
    ) -> None:
        """
        :param driver: Driver to be interacted with
        :param password: Password for Metamask wallet
        :param mnemonic: Mnemonic of Metamask's wallet
        :param extension_id: Extension's'id
        """
        extension_url = ['chrome-extension://', '/home.html']
        super().__init__(driver, password, mnemonic, extension_url, extension_id)

    @staticmethod
    def __agree_to_terms(driver: WebDriver, signing_type: _SigningType) -> None:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="onboarding__terms-checkbox"]'))).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//button[@data-testid="onboarding-{signing_type}-wallet"]'))).click()

        WebDriverWait(driver, 1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="metametrics-i-agree"]'))).click()

    def __enter_mnemonic(self, driver: WebDriver) -> None:
        mnemonic = self.mnemonic
        input_number = 0
        for word in mnemonic:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.ID, f'import-srp__srp-word-{input_number}'))).send_keys(word)
            input_number += 1

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="import-srp-confirm"]'))).click()

    @staticmethod
    def __get_mnemonic(driver: WebDriver) -> list[str]:
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="secure-wallet-recommended"]'))).click()

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="recovery-phrase-reveal"]'))).click()

        mnemonic = []
        for word_number in range(12):
            word = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//div[@data-testid="recovery-phrase-chip-{word_number}"]'))).text
            mnemonic.append(word)

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="recovery-phrase-next"]'))).click()
        return mnemonic

    @staticmethod
    def __verify_mnemonic(driver: WebDriver, mnemonic: list[str]) -> None:
        def send_words(numbers: list[int]):
            for number in numbers:
                word = mnemonic[number]
                xpath = f'//input[@data-testid="recovery-phrase-input-{number}"]'
                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, xpath))).send_keys(word)

        send_words([2, 3, 7])
        time.sleep(1)
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="recovery-phrase-confirm"]'))).click()

    @staticmethod
    def __create_password(driver: WebDriver, signing_type: _SigningType, password: str) -> None:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[@data-testid="create-password-new"]'))).send_keys(password)

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[@data-testid="create-password-confirm"]'))).send_keys(password)

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[@data-testid="create-password-terms"]'))).click()

        xpath = ''
        if signing_type == 'import':
            xpath = '//button[@data-testid="create-password-import"]'
        elif signing_type == 'create':
            xpath = '//button[@data-testid="create-password-wallet"]'

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath))).click()

    @staticmethod
    def __complete(driver: WebDriver) -> None:
        while True:
            try:
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//button[@data-testid="onboarding-complete-done"]'))).click()
            except:
                pass
            else:
                break

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="pin-extension-next"]'))).click()

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="pin-extension-done"]'))).click()

    def __handle_error(self) -> None:
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//span[@id="critical-error-button"]'))).click()
        except:
            pass
        else:
            driver.get(self.extension_url)

    def sign_in(self) -> None:
        """
        Authorizes into the metamask
        :return:
        """
        driver = self.driver
        driver.get(self.extension_url)
        signing_type = cast(_SigningType, 'import')
        password = self.password
        self.__agree_to_terms(driver, signing_type)
        self.__enter_mnemonic(driver)
        self.__create_password(driver, signing_type, password)
        self.__complete(driver)

    @classmethod
    def sign_up(
            cls,
            driver: WebDriver,
            password: str,
            extension_id: str = 'nkbihfbeogaeaoehlefnkodbefgpgknn'
    ) -> Self:
        """
        Creates an instance of Metamask by the creating all-new wallet
        For more information about extension IDs go to BrowserExtension documentation
        :param driver: Driver to be interacted with
        :param password: Password for Metamask wallet
        :param extension_id: Extension's'id
        :return: Metamask
        """
        signing_type = cast(_SigningType, 'create')

        driver.get(f'chrome-extension://{extension_id}/home.html')
        cls.__agree_to_terms(driver, signing_type)
        cls.__create_password(driver, signing_type, password)
        mnemonic = cls.__get_mnemonic(driver)
        cls.__verify_mnemonic(driver, mnemonic)
        cls.__complete(driver)
        return cls(driver, password, ' '.join(mnemonic), extension_id)

    @handle_pop_up()
    def connect(self) -> None:
        """
        Performs the third-party Metamask connection
        :return: None
        """
        driver = self.driver

        try:
            WebDriverWait(driver, 7).until(
                EC.element_to_be_clickable(
                    (By.ID, 'password'))).send_keys(self.password)

            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@data-testid="unlock-submit"]'))).click()
        except:
            pass

        try:
            for _ in range(3):
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//button[@data-testid="page-container-footer-next"]'))).click()
        except:
            pass

    def confirm(self) -> None:
        """
        Performs confirming operation. Confirming operations appear in such actions as minting NFT, snapshot voting and
        other. Most of the time, you need to use it after function connect()
        :return: None
        """
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(1))
        except:
            pass

        original_window_handle = driver.current_window_handle
        switch_to_another_window(driver)

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//i[@aria-label="Scroll down"]'))).click()
        except:
            pass

        WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-testid="page-container-footer-next"]'))).click()

        driver.switch_to.window(original_window_handle)
