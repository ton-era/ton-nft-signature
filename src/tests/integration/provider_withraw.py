'''
Test usage:
>  cd src
>  python3 -m tests.integration.provider_withraw 1 amount provider_address [to_address]
wait...
>  python3 -m tests.integration.provider_withraw 0 amount provider_address [to_address]

check:
https://testnet.tonscan.org/address/[provider_address]
'''
import sys

from tonsdk.utils import Address

from py.nft_provider import NFTSignatureProvider

from .setup import wallet, client, arg



if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    amount = float(sys.argv[2])
    provider_address = sys.argv[3]
    to_address = arg(sys.argv, 4, wallet.address)

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    # API :: change_owner
    provider = NFTSignatureProvider(address=Address(provider_address))
    result = provider.withraw(
        op_amount=0.011, amount=amount, to_address=to_address,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: withraw --------------')
    print(result)

    # GET :: get_info
    result = provider.get_info(client)
    print('-------------- GET :: get_info --------------')
    print(result)
