from abc import ABC
from selenium.webdriver.chrome.webdriver import WebDriver
from croco_selenium.decorators import handle_pop_up
from .base_account import BaseAccount
from appconnect.abc.wallet import Wallet


class DApp(BaseAccount, ABC):
    """This is an abstract class whose inheritors interact with decentralized apps, based on wallets"""
    def __init__(self, driver: WebDriver, url: str, wallet: Wallet):
        """
        :param driver: Driver to be interacted with
        :param url: URL of a social's logging page
        :param wallet: Instance of wallet-based class
        """
        super().__init__(driver, url, wallet.password, login=''.join(wallet.mnemonic))
        self.__wallet = wallet

    @property
    def wallet(self) -> Wallet:
        """
        Returns an instance of the wallet-based class
        :return: Metamask
        """
        return self.__wallet

    @handle_pop_up()
    def connect(self) -> None:
        """
        Performs the third-party wallet-based account connection
        :return:
        """
        self.wallet.confirm()
