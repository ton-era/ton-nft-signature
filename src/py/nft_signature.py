import decimal

from tonsdk.utils import Address, to_nano, b64str_to_hex
from tonsdk.boc import Cell

from .utils import addr_from_b64
from .contract import Contract


class NFTSignature(Contract):
    code = 'B5EE9C7241021401000261000114FF00F4A413F4BCF2C80B0102016202030202CC04050029A14BC3E009F083F085F087F089F08BF08DF091F09302012006070201480E0F00D3D106380492F827000E8698180B8D8492F82707D201878027C2260004980F8047019C081C641044C4B4009DF09797A698FC0815EA9105D4998F804F041080289C6C8A9105D4998F805F040815F29105D4998F805701841086A993B6DDD7C21096382D86E41007FFFF978402012008090201200A0B0201200C0D00A33B51343E90007E187E90007E18BE90007E18C835D27000274C1C3E191C3E195C3E199C3E19F834C7C07E1934C7C07E1974C7C07E198835D270803E19FE11E674C7C07E1A350C3E1A65CC1C3E1A1B7E1A78A000513E11BE117E11323E1073C5BE10B3C5BE10F3C5B2C7F2C7F2C7FE11E63E127E121632C7F337B27B5520005B3E1170003E11B0002C771C2040AFC860043232C17E1073C5887E80B2DAB2C7F2CFFE10B3C5BE10F3C5B25C7EC020008134CFFE900C1C14C0208417F30F450860043232C17E10B3C5A0822625A03E80B2DAB2C7C572CFD400F3C584F2C07280087E80B280325C7EC03E08FE197C01BC016002012010110201201213004F0C2040E17E1044B1C17CBD2040E37E1130803CBCA040E2D6682082E4E1C02E7CBCBE08FE193C016000B92040E1BE10C4F1C144BCBD2040E23E11B0803CBCB4C0007E19FE11E674C7C07E1A35007E1A77B4C0006389B4CFFE903E80350C2040AF1C20043232C1540173C59400FE8084F2DAB2C7C4B2CFF3325C7EC0244C38BE08FE19BC01BC0160001B2040E2BE1044F1C144BCBD3C01E0002D2040E1FE1084F1C144BCBD2040E27E1170803CBCBC01E0C561F7FE'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def create_data_cell(self) -> Cell:
        cell = Cell()
        cell.bits.write_address(self.options['provider_address'])
        cell.bits.write_address(self.options['item_address'])
        cell.bits.write_address(self.options['signee_address'])

        return cell


    def create_init_payload(self):
        cell = Cell()
        cell.bits.write_uint(1, 1)  # any non empty body to handle init

        return cell


    # API

    def mint(self, 
               op_amount,
               wallet, client, send=True):
        state_init = self.create_state_init()['state_init']
        payload=self.create_init_payload()

        return self.api_call(wallet, client, op_amount, state_init, payload, send)



    # GET

    @Contract.getmethod
    def get_info(self, results):
        return {
            'provider_address': addr_from_b64(results[0][1]['object']['data']['b64'])['b'],
            'item_address':     addr_from_b64(results[1][1]['object']['data']['b64'])['b'],
            'signee_address':   addr_from_b64(results[2][1]['object']['data']['b64'])['b'],
            'time_created':        int(results[3][1], 16),
            'time_owner_approve':  int(results[4][1], 16),
            'time_signee_approve': int(results[5][1], 16),
            'payload_code': int(results[6][1], 16),
            'payload':      results[7][1],
        }
