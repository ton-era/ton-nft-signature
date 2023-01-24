'''
Test usage:
>  cd src
>  python3 -m tests.integration.provider_return_item 1 provider_address item_address signee_address item_owner_address
wait...
>  python3 -m tests.integration.provider_return_item 0 provider_address item_address signee_address item_owner_address

check:
https://testnet.tonscan.org/address/[provider_address]
https://testnet.tonscan.org/address/[signature_address]
https://testnet.tonscan.org/address/[item_address]
'''
import sys

from tonsdk.utils import Address

from py.nft_provider import NFTSignatureProvider
from py.nft_item import NFTItem

from .setup import wallet, client



if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    provider_address = sys.argv[2]
    item_address = sys.argv[3]
    signee_address = sys.argv[4]
    item_owner_address = sys.argv[5]

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    # API :: mint_signature
    provider = NFTSignatureProvider(address=Address(provider_address))
    result = provider.return_item(
        op_amount=0.01 + 0.005,
        item_address=item_address, signee_address=signee_address, item_owner_address=item_owner_address,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: return_item --------------')
    print(result)

    # GET :: get_nft_data
    item = NFTItem(address=Address(item_address))
    result = item.get_nft_data(client)
    print('-------------- GET :: get_nft_data --------------')
    print(result)
