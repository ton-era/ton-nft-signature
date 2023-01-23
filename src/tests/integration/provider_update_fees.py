'''
Test usage:
>  cd src
>  python3 -m tests.integration.provider_update_fees 1 new_init_amount new_init_fee new_min_balance provider_address
wait...
>  python3 -m tests.integration.provider_update_fees 0 new_init_amount new_init_fee new_min_balance provider_address

check:
https://testnet.tonscan.org/address/[provider_address]
'''
import sys

from tonsdk.utils import Address

from py.nft_provider import NFTSignatureProvider

from .setup import wallet, client, arg



if __name__ == '__main__':
    send = bool(int(sys.argv[1]))
    new_init_amount = float(sys.argv[2])
    new_init_fee = float(sys.argv[3])
    new_min_balance = float(sys.argv[4])
    provider_address = sys.argv[5]

    print(sys.argv)
    print(f' ------------------- send to blockchain: {send} ------------------- ')

    # API :: change_owner
    provider = NFTSignatureProvider(address=Address(provider_address))
    result = provider.update_fees(
        op_amount=0.011, new_init_amount=new_init_amount, new_init_fee=new_init_fee, new_min_balance=new_min_balance,
        wallet=wallet, client=client, send=send)
    print('-------------- API :: update_fees --------------')
    print(result)

    # GET :: get_info
    result = provider.get_fees(client)
    print('-------------- GET :: get_fees --------------')
    print(result)
