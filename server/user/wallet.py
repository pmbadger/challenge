from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from web3 import Web3


def validate_wallet(wallet):
    if wallet:
        regex_validator = RegexValidator(regex=r'^0x[a-fA-F0-9]{40}$', message='Invalid Ethereum address')
        try:
            regex_validator(wallet)
        except Exception as e:
            raise ValidationError(e)


def get_balance(address):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/bc9e864d4dcb4fcea20b32230aabcf29'))
    balance = w3.eth.get_balance(address)
    eth_balance = w3.from_wei(balance, 'ether')
    return eth_balance
