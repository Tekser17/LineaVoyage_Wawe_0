from abc import ABC, abstractmethod
from selenium.webdriver.chrome.webdriver import WebDriver
from .base_account import BaseAccount


class SocialConnector(ABC):
    """This is an abstract class whose inheritors connecting other accounts to itself"""
    def __init__(self, driver: WebDriver):
        """
        :param driver: Driver to be interacted with
        """
        self.__driver = driver

    @property
    def driver(self) -> WebDriver:
        """
        Returns a driver to be interacted with
        :return: WebDriver
        """
        return self.__driver

    @abstractmethod
    def sign_in(self) -> None:
        """
        Authorizes into the account or opens its main page
        :return: None
        """
        raise NotImplementedError("Authorization is not implemented for this class.")

    @abstractmethod
    def connect_accounts(self, accounts: list[BaseAccount]) -> None:
        """
        Connects specified socials to itself
        :param accounts: List of accounts are to be connected
        :return: None
        """
        raise NotImplementedError("Connecting third-party apps is not implemented for this class")
