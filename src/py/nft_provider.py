import decimal

from tonsdk.utils import Address
from tonsdk.boc import Cell
from tonsdk.utils import Address, to_nano, b64str_to_hex

from .utils import addr_from_b64
from .contract import Contract
from .nft_signature import NFTSignature


OP_WITHRAW        = 750
OP_UPDATE_FEES    = 751
OP_CHANGE_OWNER   = 752
OP_MINT_SIGNATURE = 753


class NFTSignatureProvider(Contract):
    code = 'B5EE9C7241022501000333000114FF00F4A413F4BCF2C80B01020120020302014804050004F2300202CC06070201201D1E020120080902014817180201200A0B02012011120201200C0D0201200F1001F50831C02497C138007434C0C05C6C2497C1383E900C3C00FE11F00024C07C01B82040CAA0822625A014902FBCBD0074C7E040BB94882EA54C5B04BC01F82040BBD4882EA4CC7C01780D2040BC14842EA54C0C407C02382040BC54842EA50C163C02780CA040BC94882EA50C407C02B82040BCC4AEA4C07C02F816E00E003332140133C59633C58073C5B25C083232C044FD003D0032C03260000C8200FFFFF2F0001B3E401D3232C084B281F2FFF27420008F3B513434C3C07E1874C7C07E18BE90007E18F5007E190835D2700023840C1C3E195C3E199C3E19DC3E1A1C3E1A7834C7C07E1974C7C07E19BE80007E19FE80007E1A3E800C3E1A6002012013140201201516004F3E113E11BE117E10BE107232C3F2C7FE10F3C5B2C7F2C7FE11FE80BE123E80BE127E80B3327B552000AF2040C8BE10C4F1C144BCBD3E803E803E800C2040CA2082E4E1C014902E7CBCA040CA2084023C3460148C2E7CBCA040CA14C8EE7CBCA040CA2084017D784014882E7CBCA040C99415283E126E44FCBCBE19FE1A3E1A7C012000172040C97E11F0803CBCBC0160006D2040C87E10C4F1C144BCBD3E802040C9FE12548C2820822625A028052E44FCBC807E900C1C20043232C15633C5963E80B2DAB25C7EC020020120191A0201201B1C00252040C8FE10C4F1C144BCBD3E900C3E18FC0120008B0C7E903E900C2040CA7E1220822625A028052F84FCBD3E0A3E1104FC005C087C009C7232C0325DE0063232C15400F3C5BE11FE8084B2DAC4B333325C7EC03E11693E197C012000413E903E900C3E0A3E1110CC3C005C007C00A040CAD671C17CBD3E11A93E19BC012000852040C93E10C4F1C144BCBD3E903E903E900C3E0A3E11110C3C005C007C009C2040AFC860043232C1540133C5A0823938703E8084F2DA84B2C7F2CFC073C5B25C7EC0200201481F2002012021220015B4E21E007F08FF091F09300011B42B5E007F08BF08D002012023240021B9CE2F003F828F8444330F0017001F0028000DB4741E007F08900015B4BC3E007F083F085F08708A7538EC'

    def __init__(self, **kwargs):
        kwargs['nft_signature_code_hex'] = NFTSignature.code

        super().__init__(**kwargs)


    def create_data_cell(self) -> Cell:
        cell = Cell()
        cell.bits.write_uint(self.options['version'], 16)
        cell.bits.write_uint(self.options['id'], 32)
        cell.bits.write_address(self.options['owner_address'])
        cell.refs.append(Cell.one_from_boc(self.options['nft_signature_code_hex']))

        return cell


    def create_init_payload(self, signature_init_amount: int, signature_init_fee: int, min_balance: int):
        cell = Cell()
        cell.bits.write_coins(decimal.Decimal(signature_init_amount))
        cell.bits.write_coins(decimal.Decimal(signature_init_fee))
        cell.bits.write_coins(decimal.Decimal(min_balance))

        return cell


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


    def create_update_fees_body(self,
        new_init_amount, new_init_fee, new_min_balance) -> Cell:
        body = Cell()
        body.bits.write_uint(OP_UPDATE_FEES, 32)
        body.bits.write_coins(decimal.Decimal(new_init_amount))
        body.bits.write_coins(decimal.Decimal(new_init_fee))
        body.bits.write_coins(decimal.Decimal(new_min_balance))

        return body


    def create_mint_signature_body(self, item_address, signee_address) -> Cell:
        body = Cell()
        body.bits.write_uint(OP_MINT_SIGNATURE, 32)
        body.bits.write_address(Address(item_address))
        body.bits.write_address(Address(signee_address))

        return body

    # API

    def deploy(self, 
               op_amount, signature_init_amount, signature_init_fee, min_balance,
               wallet, client, send=True):
        state_init = self.create_state_init()['state_init']
        payload=self.create_init_payload(
                to_nano(signature_init_amount, 'ton'),
                to_nano(signature_init_fee, 'ton'),
                to_nano(min_balance, 'ton'))

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

    def update_fees(self, 
                    op_amount, new_init_amount, new_init_fee, new_min_balance,
                    wallet, client, send=True):
        payload=self.create_update_fees_body(
            to_nano(new_init_amount, 'ton'),
            to_nano(new_init_fee, 'ton'),
            to_nano(new_min_balance, 'ton'),
        )
        return self.api_call(wallet, client, op_amount, None, payload, send)

    def mint_signature(self, 
                       op_amount, item_address, signee_address,
                       wallet, client, send=True):
        payload=self.create_mint_signature_body(item_address, signee_address)
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
    def get_fees(self, results):
        return {
            'signature_init_amount': int(results[0][1], 16),
            'signature_init_fee': int(results[1][1], 16),
            'min_balance': int(results[2][1], 16),
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
