'''
Test usage:
>  cd src
>  python3 -m tests.integration.item_mint 1 index [owner_address]
wait...
>  python3 -m tests.integration.item_mint 0 index [owner_address]

check:
https://testnet.tonscan.org/address/[item-address]
'''
import sys

from py.nft_item import NFTItem

from .setup import wallet, client, arg


if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    index = int(sys.argv[2])
    owner_address = arg(sys.argv, 3, wallet.address.to_string())
    collection_address = wallet.address

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    item = NFTItem(index=index, collection_address=collection_address)

    # API :: deploy
    result = item.mint(
        op_amount=0.02 + 0.01, owner_address=owner_address, content=None,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: deploy --------------')
    print(result)

    # GET :: get_nft_data
    result = item.get_nft_data(client)
    print('-------------- GET :: get_nft_data --------------')
    print(result)

    print(f'contract: {item.address.to_string(True, True, True)}')