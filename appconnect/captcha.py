import time
from enum import Enum
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional


class ElementType(Enum):
    FRAME = 'frame'
    BOX = 'box'
    INVISIBLE = 'invisible'


class CaptchaType(Enum):
    H_CAPTCHA = 'h_captcha'
    RE_CAPTCHA = 're_captcha'


class CaptchaWaiter:
    """This is a class waiting for solving of different types of captcha"""

    @classmethod
    def wait_for_solving(
            cls, driver: WebDriver,
            captcha_type: CaptchaType,
            deadline: Optional[int] = None,
            element_type: ElementType = ElementType.FRAME
    ) -> None:
        """
        Performs waiting for captcha. If you want to limit waiting for captcha time, you can specify a deadline
        Same captcha type in the different sites may be provided as various HTML elements, for this reason you can
        specify element_type.

        :param driver: Driver to be interacted with
        :param captcha_type: Type of captcha. Can take in captcha types such as hCaptcha, reCaptcha
        :param deadline: Waiting deadline in seconds
        :param element_type: Type of captcha element. Can take in ElementType.FRAME, ElementType.BOX
        :return:
        """
        match captcha_type:
            case CaptchaType.H_CAPTCHA:
                cls.wait_for_h_captcha(driver, deadline)
            case CaptchaType.RE_CAPTCHA:
                cls.wait_for_re_captcha(driver, deadline, element_type)

    @staticmethod
    def __wait_by_checkbox(checkbox: WebElement, deadline: Optional[int] = None):
        if not deadline:
            try:
                while checkbox.get_attribute("aria-checked") != 'true':
                    pass
            except:
                pass
        else:
            start_time = datetime.now()

            while True:
                current_time = datetime.now()
                time_range = (current_time - start_time).total_seconds()
                if time_range >= deadline:
                    raise Exception("Captcha is not solved")

                if checkbox.get_attribute("aria-checked") == 'true':
                    break

    @classmethod
    def wait_for_h_captcha(cls, driver: WebDriver, deadline: Optional[int] = None) -> None:
        """
        Performs waiting for hCaptcha. If you want to limit waiting for captcha time, you can specify a deadline
        Same captcha type in the different sites may be provided as various HTML elements, for this reason you can
        specify element_type.

        :param driver: Driver to be interacted with
        :param deadline: Waiting deadline in seconds
        :return: None
        """
        WebDriverWait(driver, 15).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, '//iframe[@data-hcaptcha-widget-id]')))

        checkbox = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="checkbox"]')))

        cls.__wait_by_checkbox(checkbox, deadline)

        driver.switch_to.parent_frame()

    @classmethod
    def wait_for_re_captcha(
            cls,
            driver: WebDriver,
            deadline: Optional[int] = None,
            element_type: ElementType = ElementType.FRAME
    ) -> None:
        """
        Performs waiting for hCaptcha. If you want to limit waiting for captcha time, you can specify a deadline
        Same captcha type in the different sites may be provided as various HTML elements, for this reason you can
        specify element_type.
        :param driver: Driver to be interacted with
        :param deadline: Waiting deadline in seconds
        :param element_type: Type of captcha element. Can take in ElementType.FRAME, ElementType.BOX
        :return: None
        """
        match element_type:
            case ElementType.FRAME:
                cls.__handle_frame_re_captcha(driver, deadline)
            case ElementType.BOX:
                cls.__handle_box_re_captcha(driver, deadline)

    @classmethod
    def __handle_frame_re_captcha(cls, driver: WebDriver, deadline: Optional[int] = None) -> None:
        WebDriverWait(driver, 15).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@title="reCAPTCHA"]')))

        checkbox = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="recaptcha-anchor"]')))

        cls.__wait_by_checkbox(checkbox, deadline)

        driver.switch_to.parent_frame()
        time.sleep(1)

    @classmethod
    def __handle_box_re_captcha(cls, driver: WebDriver, deadline: Optional[int] = None) -> None:
        checkbox_xpath = '//span[contains(@class, "recaptcha-checkbox")]'
        checkbox = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, checkbox_xpath)))
        cls.__wait_by_checkbox(checkbox, deadline)
        time.sleep(1)
