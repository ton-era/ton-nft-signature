'''
Test usage:
>  cd src
>  python3 -m tests.integration.09_signee_signature_sign 1 signature_address
wait...
>  python3 -m tests.integration.09_signee_signature_sign 0 signature_address

check:
https://testnet.tonscan.org/address/[signature_address]
'''
import sys
import time

from tonsdk.utils import Address

from py.nft_provider import NFTSignatureProvider
from py.nft_signature import NFTSignature
from py.nft_item import NFTItem
from py.utils import b64_from_addr

from .setup import wallet, client, arg


if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    signature_address  = sys.argv[2]

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    signature = NFTSignature(address=Address(signature_address))
    result = signature.get_info(client)
    item_address = result['data']['item_address']
    signee_address = result['data']['signee_address']
    provider_address = result['data']['provider_address']

    # API :: sign
    result = signature.signee_sign(
        op_amount=0.035, message="From Pavel with love..",
        wallet=wallet, client=client, send=send)
    print('-------------- API :: signee_sign --------------')
    print(result)

    if send:
        print('\nwaiting to finalize trans in blockchain...\n')
        time.sleep(15)

    # GET :: signature get_info
    result = signature.get_info(client)
    print('-------------- GET :: get_info --------------')
    print(result)

    if (result['data'].get('time_owner_approved') > 0) and (result['data'].get('time_signee_approved') > 0):
        print('\nYor NFT was signed!!! 🎉🎉🎉🎉🎉\n')

    # GET :: get_nft_data
    item = NFTItem(address=Address(item_address))
    print(f'item_address: {item_address}')
    print(f'signee_address: {signee_address}')
    print(f'provider_address: {provider_address}')

    result = item.get_nft_data(client)
    print('-------------- GET :: get_nft_data --------------')
    print(result)

    # GET :: provider get_stats
    provider = NFTSignatureProvider(address=Address(provider_address))
    result = provider.get_stats(client)
    print('---------------- GET :: get_stats ---------------')
    print(result)
 