'''
Test usage:
>  cd src
>  python3 -m tests.integration.signature_mint 1 [provider_address] [item_address] [signee_address]
wait...
>  python3 -m tests.integration.signature_mint 0 [provider_address] [item_address] [signee_address]

check:
https://testnet.tonscan.org/address/[signature_address]
'''
import sys

from py.nft_provider import NFTSignature

from .setup import wallet, client, arg


if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    provider_address = arg(sys.argv, 2, wallet.address)
    item_address = arg(sys.argv, 3, wallet.address)
    signee_address = arg(sys.argv, 4, wallet.address)

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    signature = NFTSignature(
        provider_address=provider_address,
        item_address=item_address,
        signee_address=signee_address)
    print(f'contract: {signature.address.to_string(True, True, True)}')

    # API :: deploy
    result = signature.mint(
        op_amount=0.03 + 0.01,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: deploy --------------')
    print(result)

    # GET :: signature get_info
    result = signature.get_info(client)
    print('-------------- GET :: get_info --------------')
    print(result)
