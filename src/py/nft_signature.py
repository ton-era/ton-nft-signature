import base64

from tonsdk.boc import Cell

from .utils import addr_from_b64
from .contract import Contract


OP_MINT = 700
OP_SIGN = 701


class NFTSignature(Contract):
    code = 'B5EE9C7241021701000284000114FF00F4A413F4BCF2C80B0102016202030202CC04050025A14BC3E00BF083F085F087F089F08BF08DF09102012006070201200F1002012008090201200B0C01F7420C700925F04E001D0D3030171B0925F04E0F005FA403081038C82089896805240BEF2F4F844C0009654732024F009DE21D749C120925F04E001D31F8102BC5220BA925F05E08102BD5220BA9331F00AE0821005138D915220BA9331F00CE08102BE5220BA9331F00BE0306C228210D53276DBBAF84112C705B0DC80A00194206E95307001CB0192CF16E28000C8200FFFFF2F000895ED44D0FA4001F861FA4001F862FA4001F86320C7028E103070F86470F86570F8666DF8676DF868E0D401D0D31F01F864D31F01F865D31F01F866FA4030F867F40430F86880201200D0E00513E11BE117E113232C7F2C7F2C7FE11FC00B27E12323E1073C5BE10B3C5BE10F3C584B33D00327B5520007B0C3E1170003E11B0002C644C382082BEBC20286084017D78402D822040AFDC20043232C17E10F3C59400FE8084B2DAB2C7FE1073C5BE10B3C5B25C7EC0200201201112003BD4081C3FC2089E38289797A4081C4FC22E1007979699FFD20187C33F804402012013140201201516007D3E001C14C0208417F30F450860043232C17E1073C5A0822625A03E80B2DAB2C7C532CFFE11F3C584F2C044B280087E80B280325C7EC03E08FE197C01FC01A0003B17C0E040E37E1130803CBCA040E2E082BEBC2004AE7CBCBE08FE193C01A000A32040E1BE1084F1C144BCBD2040E23E11B0803CBCBE0034CFFD01007E1A34800063893E903E80350C2040AF5C20043232C1540173C59400FE8084F2DAB2C7C4B2CFF3325C7EC02456F8BE08FE19BC01FC01A000212040E2BE11C4F1C144BCBD34CFCC3C022043E69E33'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def create_data_cell(self) -> Cell:
        cell = Cell()
        cell.bits.write_address(self.options['item_address'])
        cell.bits.write_address(self.options['signee_address'])
        cell.bits.write_address(self.options['provider_address'])

        return cell

    def create_owner_mint_payload(self, query_id=0):
        cell = Cell()
        cell.bits.write_uint(OP_MINT, 32)
        cell.bits.write_uint(query_id, 64)

        return cell

    def create_signee_mint_payload(self, query_id=0, payload=None):
        cell = Cell()
        cell.bits.write_uint(OP_SIGN, 32)
        cell.bits.write_uint(query_id, 64)

        has_payload = payload is not None

        if has_payload:
            cell.bits.write_int(-1, 1)
            payload_cell = Cell()
            if type(payload) == str:
                if len(payload) > 0:
                    payload_cell.bits.write_uint(0, 32)
                    payload_cell.bits.write_string(payload)
            elif hasattr(payload, 'refs'):
                payload_cell = payload
            else:
                payload_cell.bits.write_bytes(payload)

            cell.refs.append(payload_cell)
        else:
            cell.bits.write_int(0, 1)

        cell.bits.write_int(0, 1) # need_notify

        return cell


    # API

    def signee_mint(self, 
                    op_amount, message,
                    wallet, client, send=True):
        state_init = self.create_state_init()['state_init']
        payload=self.create_signee_mint_payload(payload=message)

        return self.api_call(wallet, client, op_amount, state_init, payload, send)

    def owner_mint(self, 
                   op_amount,
                   wallet, client, send=True):
        state_init = self.create_state_init()['state_init']
        payload=self.create_owner_mint_payload()

        return self.api_call(wallet, client, op_amount, state_init, payload, send)


    # GET

    @Contract.getmethod
    def get_info(self, results):
        payload = None
        has_payload = (results[6][0] == 'cell')
        if has_payload:
            raw_payload = base64.b64decode(results[6][1]['object']['data']['b64']).decode('utf-8')
            payload_type = int.from_bytes(bytes(raw_payload[:4], 'utf-8'), 'big')
            if payload_type == 0:  # simple string
                payload = raw_payload[4:]
            else:
                payload = raw_payload

        return {
            'item_address':     addr_from_b64(results[0][1]['object']['data']['b64'])['b'],
            'signee_address':   addr_from_b64(results[1][1]['object']['data']['b64'])['b'],
            'provider_address': addr_from_b64(results[2][1]['object']['data']['b64'])['b'],
            'time_created':         int(results[3][1], 16),
            'time_owner_approved':  int(results[4][1], 16),
            'time_signee_approved': int(results[5][1], 16),
            'payload': payload,
        }
