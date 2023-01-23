'''
Test usage:
>  cd src
>  python3 -m tests.integration.provider_deploy 1 provider_address [new_owner_address]
wait...
>  python3 -m tests.integration.provider_deploy 0 provider_address [new_owner_address]

check:
https://testnet.tonscan.org/address/[provider_address]
'''
import sys

from tonsdk.utils import Address

from py.nft_provider import NFTSignatureProvider

from .setup import wallet, client, arg



if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    provider_address  = sys.argv[2]
    new_owner_address = arg(sys.argv, 3, wallet.address)

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    # API :: change_owner
    provider = NFTSignatureProvider(address=Address(provider_address))
    result = provider.change_owner(
        amount=0.011, new_owner_address=new_owner_address,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: change_owner --------------')
    print(result)

    # GET :: get_info
    result = provider.get_info(client)
    print('-------------- GET :: get_info --------------')
    print(result)
