'''
Test usage:
>  cd src
>  python3 -m tests.integration.provider_mint_signature 1 provider_address item_address [signee_address]
wait...
>  python3 -m tests.integration.provider_mint_signature 0 provider_address item_address [signee_address]

check:
https://testnet.tonscan.org/address/[provider_address]
https://testnet.tonscan.org/address/[signature_address]
'''
import sys

from tonsdk.utils import Address

from py.utils import b64_from_addr
from py.nft_provider import NFTSignatureProvider
from py.nft_signature import NFTSignature

from .setup import wallet, client, arg



if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    provider_address = sys.argv[2]
    item_address = sys.argv[3]
    signee_address = arg(sys.argv, 4, wallet.address.to_string(True, True, True))

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    # API :: mint_signature
    provider = NFTSignatureProvider(address=Address(provider_address))
    result = provider.mint_signature(
        op_amount=0.30 + 0.01 + 0.005, item_address=item_address, signee_address=signee_address,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: mint_signature --------------')
    print(result)

    # GET :: get_signature_address
    print('-------------- GET :: get_signature_address --------------')
    item_address_slice = \
        '{"data": {"b64": "' + b64_from_addr(item_address) + '", "len": 267}, "refs": [] }'
    signee_address_slice = \
        '{"data": {"b64": "' + b64_from_addr(signee_address) + '", "len": 267}, "refs": [] }'
    result = provider.get_signature_address(
        client, stack_data=[['slice', item_address_slice], ['slice', signee_address_slice]])
    print(result)

    signature_address = result['data']['signature_address']
    signature = NFTSignature(address=Address(signature_address))

    # GET :: signature get_info
    result = signature.get_info(client)
    print('-------------- GET :: signature get_info --------------')
    print(result)

    print(f'contract: {signature_address}')
