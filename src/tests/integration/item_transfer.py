'''
Test usage:
>  cd src
>  python3 -m tests.integration.item_transfer 1 item_address new_owner_address
wait...
>  python3 -m tests.integration.item_transfer 0 item_address new_owner_address

check:
https://testnet.tonscan.org/address/[item-address]
'''
import sys

from tonsdk.utils import Address

from py.nft_item import NFTItem

from .setup import wallet, client, arg


if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    item_address = sys.argv[2]
    new_owner_address = sys.argv[3]

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    item = NFTItem(address=Address(item_address))
    print(f'contract: {item.address.to_string(True, True, True)}')

    # API :: transfer
    result = item.transfer(
        op_amount=0.03, new_owner_address=new_owner_address,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: transfer --------------')
    print(result)

    # GET :: get_nft_data
    result = item.get_nft_data(client)
    print('-------------- GET :: get_nft_data --------------')
    print(result)
