'''
Test usage:
>  cd src
>  python3 -m 'tests.integration.07_owner_signature_mint&approve' 1 item_address [signee_address] [provider_address]
wait...
>  python3 -m 'tests.integration.07_owner_signature_mint&approve' 0 item_address [signee_address] [provider_address]

check:
https://testnet.tonscan.org/address/[signature_address]
'''
import sys
import time

from tonsdk.utils import Address

from py.nft_provider import NFTSignature
from py.nft_item import NFTItem

from .setup import wallet, client, arg


if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    item_address = Address(sys.argv[2])
    signee_address = Address(arg(sys.argv, 3, wallet.address))
    provider_address = Address(arg(sys.argv, 4, wallet.address))

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    signature = NFTSignature(
        item_address=item_address,
        signee_address=signee_address,
        provider_address=provider_address)
    print(f'contract: {signature.address.to_string(True, True, True)}')

    # API :: mint
    result = signature.owner_mint(
        op_amount=0.11,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: mint --------------')
    print(result)

    if send:
        print('\nwaiting to finalize wallet seqno...\n')
        time.sleep(12)

    # API :: approve from NFT owner
    item = NFTItem(address=Address(item_address))

    result = item.approve(
        op_amount=0.11, signature_address=signature.address, forward_amount=0.08,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: owner approve --------------')
    print(result)

    # GET :: get_nft_data
    result = item.get_nft_data(client)
    print('-------------- GET :: get_nft_data --------------')
    print(result)

    # GET :: signature get_info
    result = signature.get_info(client)
    print('-------------- GET :: get_info --------------')
    print(result)

    print(f'contract: {signature.address.to_string(True, True, True)}')
