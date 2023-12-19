from abc import ABC, abstractmethod
from selenium.webdriver.chrome.webdriver import WebDriver
from croco_selenium.decorators import handle_pop_up
from appconnect.email import Email
from typing import Optional


class BaseAccount(ABC):
    """This is an abstract class whose inheritors interact with socials"""
    def __init__(
            self,
            driver: WebDriver,
            url: str,
            password: str,
            email: Optional[Email] = None,
            login: Optional[str] = None
    ):
        """
        :param driver: Driver to be interacted with
        :param url: URL of a social's logging page
        :param password: Password of a social's account
        :param email: Instance of the Email created from account's credentials
        :param login: Login of a social's account. Most of the time, an email address or username
        are used as the login
        """
        self.__driver = driver
        self.__url = url
        self.__login = login if login else email.login
        self.__password = password
        self.__email = email

    def __enter__(self):
        self.sign_in()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sign_out()

    @property
    def driver(self) -> WebDriver:
        """
        Returns a driver to be interacted with
        :return: WebDriver
        """
        return self.__driver

    @property
    def url(self) -> str:
        """
        Returns URL of the social's logging page
        :return: str
        """
        return self.__url

    @property
    def login(self) -> str | None:
        """
        Returns a login of the current social's account.
        Most of the time, an email address or username are used as the login
        :return: str
        """
        return self.__login

    @property
    def password(self) -> str:
        """
        Returns a password of the current social's account
        :return: str
        """
        return self.__password

    @property
    def email(self) -> Email | None:
        """
        Returns an instance of the account's Email

        :return: Email
        """
        return self.__email

    @abstractmethod
    def sign_in(self) -> None:
        """
        Authorizes into the account or opens its main page
        :return: None
        """
        raise NotImplementedError("Authorization is not implemented for this class.")

    @abstractmethod
    @handle_pop_up()
    def connect(self) -> None:
        """
        Performs the third-party account connection
        :return: None
        """
        raise NotImplementedError("Third-party connection is not implemented for this class.")

    def sign_out(self) -> None:
        """
        Logs out from the account
        :return: None
        """
        driver = self.driver
        driver.get(self.url)
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.refresh()
