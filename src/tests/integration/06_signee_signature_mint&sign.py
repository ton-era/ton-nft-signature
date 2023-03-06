'''
Test usage:
>  cd src
>  python3 -m 'tests.integration.06_signee_signature_mint&sign' 1 item_address [signee_address] [provider_address]
wait...
>  python3 -m 'tests.integration.06_signee_signature_mint&sign' 0 item_address [signee_address] [provider_address]

check:
https://testnet.tonscan.org/address/[signature_address]
'''
import sys

from tonsdk.utils import Address

from py.nft_provider import NFTSignature

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

    # API :: mint & sign
    result = signature.signee_mint(
        op_amount=0.11, message="From Pavel with love..",
        wallet=wallet, client=client, send=send)
    print('-------------- API :: signee_mint --------------')
    print(result)

    # GET :: signature get_info
    result = signature.get_info(client)
    print('-------------- GET :: get_info --------------')
    print(result)

    print(f'contract: {signature.address.to_string(True, True, True)}')
