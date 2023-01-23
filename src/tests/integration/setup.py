from tonsdk.contract.wallet import WalletV4ContractR2

from py.client import TonCenterTonClient


# consts

NET = 'testnet'
WALLET_ADDR = 'EQCMtNptOpedpgHhvDMAY9_Df1RXxIGywTanzJM-r45ZLZpU'


# wallet
wallet = WalletV4ContractR2(
    private_key=open(f'../secrets/{NET}-{WALLET_ADDR}.pk', 'rb').read(),
    address=WALLET_ADDR)

# TON client
client = TonCenterTonClient()


# utils

def arg(args, i, default=None):
    try:
        return args[i]
    except IndexError:
        return default
