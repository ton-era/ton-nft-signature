'''
Test usage:
>  cd src
>  python3 -m tests.integration.provider_deploy 1 [version] [id] [owner_address]
wait...
>  python3 -m tests.integration.provider_deploy 0 [version] [id] [owner_address]

check:
https://testnet.tonscan.org/address/[provider_address]
'''
import sys

from tonsdk.utils import Address

from py.utils import b64_from_addr
from py.nft_provider import NFTSignatureProvider

from .setup import wallet, client, arg


if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    version = int(arg(sys.argv, 2, 1))
    id = int(arg(sys.argv, 3, 1))
    owner_address = arg(sys.argv, 4, wallet.address)

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    provider = NFTSignatureProvider(
        version=version, 
        id=id, 
        owner_address=Address(owner_address))

    # API :: deploy
    result = provider.deploy(
        op_amount=0.11 + 0.01,
        signature_init_amount=0.07,
        signature_init_fee=0.30,
        min_balance=0.11,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: deploy --------------')
    print(result)

    # GET :: get_info
    result = provider.get_info(client)
    print('-------------- GET :: get_info --------------')
    print(result)

    # GET :: get_fees
    result = provider.get_fees(client)
    print('-------------- GET :: get_fees --------------')
    print(result)

    # GET :: get_stats
    result = provider.get_stats(client)
    print('-------------- GET :: get_stats --------------')
    print(result)

    # GET :: get_sign_code
    result = provider.get_sign_code(client)
    print('-------------- GET :: get_sign_code --------------')
    print(result)

    # GET :: get_signature_address
    print('-------------- GET :: get_signature_address --------------')
    item_address_slice = \
        '{"data": {"b64": "' + b64_from_addr(wallet.address.to_string()) + '", "len": 267}, "refs": [] }'
    signee_address_slice = \
        '{"data": {"b64": "' + b64_from_addr(wallet.address.to_string()) + '", "len": 267}, "refs": [] }'
    result = provider.get_signature_address(
        client, stack_data=[['slice', item_address_slice], ['slice', signee_address_slice]])
    print(result)

    print(f'contract: {provider.address.to_string(True, True, True)}')
