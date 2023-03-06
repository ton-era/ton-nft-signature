import decimal

from tonsdk.utils import Address
from tonsdk.boc import Cell
from tonsdk.utils import Address, to_nano, b64str_to_hex

from .utils import addr_from_b64
from .contract import Contract
from .nft_signature import NFTSignature


OP_WITHRAW = 750
OP_CHANGE_OWNER = 751


class NFTSignatureProvider(Contract):
    code = 'B5EE9C7241021A010001A2000114FF00F4A413F4BCF2C80B01020120020302014804050004F2300202CC0607020120141502012008090201D412130201200A0B0201200C0D009D420C700925F04E001D0D3030171B0925F04E0FA4030F00581032A82084C4B4014BE13F2F4D31F8102EE5220BA9331F007E0338102EF5210BA943001F008E08102BFBA9301F009E05B8200FFFFF2F0800335C85003CF1601CF1658CF16C97020C8CB0113F400F400CB00C980201200E0F0201201011001B3E401D3232C084B281F2FFF2742000373B513434C3C07E1874C7C07E18BE90007E18F4C7C07E19350C3E1960002F3E117E113E10BE107232C3F2C7FE10F3C5B2C7F3327B552000672040C87E10C4F1C144BCBD3E802040C9E0821312D0148C28052E44FCBC807E900C1C20043232C15633C5963E80B2DAB25C7EC02000252040C8FE10C4F1C144BCBD3E900C3E18FC01A000413E903E900C3E0A3E1150CC3C00DC007C012040CAD671C17CBD3E11293E193C01A0000DBD0AD7802FC224020120161702012018190021B9CE2F005F828F8454330F0037001F0048000DB4741E00BF08B00015B4BC3E00BF083F085F08708012502D'

    def __init__(self, **kwargs):
        kwargs['nft_signature_code_hex'] = NFTSignature.code

        super().__init__(**kwargs)


    def create_data_cell(self) -> Cell:
        cell = Cell()
        cell.bits.write_uint(self.options['version'], 16)
        cell.bits.write_uint(self.options['id'], 32)
        cell.bits.write_address(self.options['owner_address'])
        cell.bits.write_uint(0, 32)  # initial signature_commit_cnt
        cell.refs.append(Cell.one_from_boc(self.options['nft_signature_code_hex']))

        return cell

    def create_init_payload(self):
        return None

    def create_change_owner_body(self, new_owner_address: str) -> Cell:
        body = Cell()
        body.bits.write_uint(OP_CHANGE_OWNER, 32)
        body.bits.write_address(Address(new_owner_address))

        return body

    def create_withraw_body(self, amount, to_address: str) -> Cell:
        body = Cell()
        body.bits.write_uint(OP_WITHRAW, 32)
        body.bits.write_coins(decimal.Decimal(amount))
        body.bits.write_address(Address(to_address))

        return body


    # API

    def deploy(self, 
               op_amount,
               wallet, client, send=True):
        state_init = self.create_state_init()['state_init']
        payload = self.create_init_payload()  # None

        return self.api_call(wallet, client, op_amount, state_init, payload, send)


    def change_owner(self,
                     op_amount, new_owner_address,
                     wallet, client, send=True):
        payload=self.create_change_owner_body(new_owner_address)
        return self.api_call(wallet, client, op_amount, None, payload, send)


    def withraw(self, 
                op_amount, amount, to_address,
                wallet, client, send=True):
        payload=self.create_withraw_body(to_nano(amount, 'ton'), to_address)
        return self.api_call(wallet, client, op_amount, None, payload, send)


    # GET

    @Contract.getmethod
    def get_info(self, results):
        return {
            'version': int(results[0][1], 16),
            'id': int(results[1][1], 16),
            'owner_address': addr_from_b64(results[2][1]['object']['data']['b64'])['b'],
        }

    @Contract.getmethod
    def get_stats(self, results):
        return {
            'signature_commit_cnt': int(results[0][1], 16),
        }

    @Contract.getmethod
    def get_sign_code(self, results):
        return {
            'signature_code': b64str_to_hex(results[0][1]['bytes']).upper(),
        }

    @Contract.getmethod
    def get_signature_address(self, results):
        return {
            'signature_address': addr_from_b64(results[0][1]['object']['data']['b64'])['b'],
        }
