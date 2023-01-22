from tonsdk.contract.wallet import Wallets, WalletContract, WalletV4ContractR2
from tonsdk.utils import bytes_to_b64str, Address, to_nano
from tonsdk.contract.token.nft import NFTCollection, NFTItem
from tonsdk.provider import prepare_address
from tonsdk.crypto import mnemonic_to_wallet_key

from .client import TonCenterTonClient


class SNFTCollection(NFTCollection):
    code = 'B5EE9C72410213010001FE000114FF00F4A413F4BCF2C80B0102016202030202CD04050201200D0E03EBD10638048ADF000E8698180B8D848ADF07D201800E98FE99FF6A2687D20699FEA6A6A184108349E9CA829405D47141BAF8280E8410854658056B84008646582A802E78B127D010A65B509E58FE59F80E78B64C0207D80701B28B9E382F970C892E000F18112E001718119026001F1812F82C207F9784060708020120090A00603502D33F5313BBF2E1925313BA01FA00D43028103459F0078E1201A44343C85005CF1613CB3FCCCCCCC9ED54925F05E200A6357003D4308E378040F4966FA5208E2906A4208100FABE93F2C18FDE81019321A05325BBF2F402FA00D43022544B30F00723BA9302A402DE04926C21E2B3E6303250444313C85005CF1613CB3FCCCCCCC9ED54002801FA40304144C85005CF1613CB3FCCCCCCC9ED54002D501C8CB3FF828CF16C97020C8CB0113F400F400CB00C980201200B0C001B3E401D3232C084B281F2FFF27420003D16BC015C087C019DE0063232C15633C594013E8084F2DAC4B333325C7EC0200201200F100025BC82DF6A2687D20699FEA6A6A182DE86A182C40043B8B5D31ED44D0FA40D33FD4D4D43010245F04D0D431D430D071C8CB0701CF16CCC980201201112002FB5DAFDA89A1F481A67FA9A9A860D883A1A61FA61FF480610002DB4F47DA89A1F481A67FA9A9A86028BE09E00AE003E00D03E355572'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == '__main__':
    # mnemonics = ''.split()
    # pub_k, priv_k = mnemonic_to_wallet_key(mnemonics)
    # open('../secrets/twallet.pk', 'wb').write(priv_k)

    address = 'EQCMtNptOpedpgHhvDMAY9_Df1RXxIGywTanzJM-r45ZLZpU'
    wallet = WalletV4ContractR2(
        private_key=open(f'../secrets/test-{address}.pk', 'rb').read(),
        address=address)

    print(wallet.address.to_string(True, True, True))

    collection = SNFTCollection(
        royalty=5,
        royalty_address=Address(address),
        owner_address=Address(address),
        collection_content_uri='https://google.com/collection/11',
        nft_item_content_base_uri='https://google.com/',
        nft_item_code_hex=NFTItem.code,
    )

    coll_address = collection.address.to_string(True, True, True)
    print(coll_address)

    # client = TonCenterTonClient(
    #     base_url='https://toncenter.com/api/v2/',
    #     api_key='ca69977285f93d2de70a061b9740ac23605f4cc8ddc06b7ec4ddccb58c0ac9d9')
    client = TonCenterTonClient()
    seqno = client.seqno(wallet.address.to_string())
    seqno = int(seqno[0]['stack'][0][1], 16)
    print(f'seqno: {seqno}')

    query = wallet.create_transfer_message(
        to_addr=collection.address,
        amount=to_nano(0.04, 'ton'),
        seqno=seqno, 
        state_init=collection.create_state_init()['state_init'],
    )
    transfer_boc = query["message"].to_boc(False)
    print(f'transfer boc created: {bytes_to_b64str(transfer_boc)}')

    result = client.send_boc(transfer_boc)
    print(result)
