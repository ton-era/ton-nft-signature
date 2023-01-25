'''
Test usage:
>  cd src
>  python3 -m tests.integration.signature_approve 1 signature_address [item_owner_address] [signee_address]
wait...
>  python3 -m tests.integration.signature_approve 0 signature_address [item_owner_address] [signee_address]

check:
https://testnet.tonscan.org/address/[signature_address]
'''
import sys
import time

from tonsdk.utils import Address

from py.nft_provider import NFTSignatureProvider
from py.nft_signature import NFTSignature
from py.nft_item import NFTItem

from .setup import wallet, client, arg


if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    signature_address  = sys.argv[2]
    item_owner_address = arg(sys.argv, 3, wallet.address)
    signee_address     = arg(sys.argv, 4, None)

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    signature = NFTSignature(address=Address(signature_address))
    result = signature.get_info(client)
    item_address = result['data']['item_address']
    signee_address = signee_address or result['data']['signee_address']
    provider_address = result['data']['provider_address']

    item = NFTItem(address=Address(item_address))
    print(f'item_address: {item.address.to_string(True, True, True)}')
    print(f'signee_address: {signee_address}')
    print(f'provider_address: {provider_address}')

    # API :: approve from NFT owner
    result = item.approve(
        op_amount=0.05, signature_address=signature_address, forward_amount=0.01,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: owner approve --------------')
    print(result)

    if send:
        print('\nwaiting to finalize wallet seqno...\n')
        time.sleep(12)

    # API :: approve from signee
    result = signature.approve_by_signee( 
        op_amount=0.01 + 0.005, query_id=0, payload="From Pavel with love..",
        wallet=wallet, client=client, send=send)
    print('-------------- API :: signee approve --------------')
    print(result)

    # GET :: signature get_info
    result = signature.get_info(client)
    print('-------------- GET :: get_info --------------')
    print(result)

    if (result['data'].get('time_owner_approved') > 0) and (result['data'].get('time_signee_approved') > 0):
        print('\nYor NFT was signed!!! 🎉🎉🎉🎉🎉\n')


    # GET :: signature get_info
    provider = NFTSignatureProvider(address=Address(provider_address))
    result = provider.get_stats(client)
    print('-------------- GET :: get_stats --------------')
    print(result)
