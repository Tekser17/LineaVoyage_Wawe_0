from typing import Any


class InvalidMnemonicLength(Exception):
    """Raised when a length of provided mnemonic is invalid"""

    def __init__(self, mnemonic: list[str]) -> None:
        super().__init__(f"Mnemonic is invalid. Mnemonic has to have length equals to 12. "
                         f"Your mnemonic is: {mnemonic}.")


class InvalidMethodType(TypeError):
    """Raised when a provided method type is not represented as Literal['object', 'static', 'class']"""

    def __init__(self, value: Any):
        super().__init__(f"Method type is not represented as Literal['object', 'static', 'class']. Provided value is "
                         f"{value}")


class InvalidCoinSide(TypeError):
    """Raised if coin side doesn't represent literal type CoinSide"""

    def __init__(self, value: Any):
        super().__init__(f"Coin's side must be represented as Head or Tail. Provided value is: {value}")


class InvalidCoinflipToken(TypeError):
    """Raised if coin side doesn't represent literal type CoinflipToken"""

    def __init__(self, value: Any):
        super().__init__(f"Coin side must be represented as SUI or BUCK. Provided value is: {value}")
