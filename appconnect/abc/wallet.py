from typing import Self
from selenium.webdriver.chrome.webdriver import WebDriver
from abc import abstractmethod
from croco_selenium.decorators import handle_pop_up
from .base_account import BaseAccount
from .browser_extension import BrowserExtension
from appconnect.exceptions import InvalidMnemonicLength


class Wallet(BaseAccount, BrowserExtension):
    """This is an abstract class whose inheritors interact with digital wallets"""

    def __init__(
            self,
            driver: WebDriver,
            password: str,
            mnemonic: str,
            extension_url: list[str],
            extension_id: str
    ) -> None:
        """
        For more information about extension IDs go to BrowserExtension documentation

        :param driver: Driver to be interacted with
        :param password: Password for wallet
        :param mnemonic: Mnemonic of wallet
        :param extension_url: Parts of extension's url provided as ['chrome-extension://', main_page_url].
        :param extension_id: Extension's'id
        """
        url = extension_url.copy()
        url.insert(1, extension_id)
        url = ''.join(url)
        BaseAccount.__init__(self, driver, url, password, login=mnemonic)
        BrowserExtension.__init__(self, driver, extension_url, extension_id)
        mnemonic_split = mnemonic.split()

        if len(mnemonic_split) != 12:
            InvalidMnemonicLength(mnemonic_split)

        self.__mnemonic = mnemonic.split()
        self.__public_key = None

    @property
    def mnemonic(self) -> list[str]:
        """
        Returns wallet's mnemonic
        :return: list[str]
        """
        return self.__mnemonic

    @property
    def public_key(self) -> str | None:
        """
        Returns wallet's public key
        :return: str | None
        """
        return self.__public_key

    @public_key.setter
    def public_key(self, value: str):
        if isinstance(value, str):
            self.__public_key = value

    @abstractmethod
    def sign_in(self) -> None:
        """
        Authorizes into the wallet
        :return: None
        """
        raise NotImplementedError("Authorization is not implemented for this wallet.")

    @abstractmethod
    @handle_pop_up()
    def connect(self) -> None:
        """
        Performs the third-party wallet connection
        :return: None
        """
        raise NotImplementedError("Third-party connection is not implemented for this wallet.")

    @classmethod
    @abstractmethod
    def sign_up(
            cls,
            driver: WebDriver,
            password: str,
            extension_id: str
    ) -> Self:
        """
        For more information about extension IDs go to BrowserExtension documentation

        Creates an instance of digital wallet by the creating all-new wallet
        :param driver: Driver to be interacted with
        :param password: Password for wallet
        :param extension_id: Extension's'id
        :return: Wallet
        """
        pass

    @abstractmethod
    def confirm(self) -> None:
        """
        Performs confirming operation. Confirming operations appear in such actions as minting NFT, snapshot voting and
        other. Most of the time, you need to use it after function connect()
        :return: None
        """
        pass
