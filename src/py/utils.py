'''
TON blockchain utility finctions.
'''
import base64
from tonsdk.utils import crc16
from bitstring import BitArray


BOUNCEABLE_TAG = b'\x11'
NONBOUNCEABLE_TAG = b'\x51'


def addr_from_b64(b64_addr):
    b64_bytes = base64.b64decode(b64_addr)
    
    bits = BitArray(b64_bytes)
    flag_bits = bits[:3]
    wc_bits = int.from_bytes(bits[3:11], byteorder='big', signed=True).to_bytes(4, "big")
    addr_bits = bits[11:-5]
    b64_bytes = (addr_bits + wc_bits).bytes

    return addr_from_bytes(b64_bytes)


def addr_from_bytes(bytes):
    addr_bytes, wc_bytes = bytes[:32], bytes[32:]
    wc = int.from_bytes(wc_bytes, byteorder='big', signed=True)
    wc_bytes = b'\xff' if wc == -1 else wc.to_bytes(1, "big")
    
    preaddr_b = BOUNCEABLE_TAG + wc_bytes + addr_bytes
    preaddr_u = NONBOUNCEABLE_TAG + wc_bytes + addr_bytes
    b64_b = base64.urlsafe_b64encode(preaddr_b + crc16(preaddr_b)).decode('utf8')
    b64_u = base64.urlsafe_b64encode(preaddr_u + crc16(preaddr_u)).decode('utf8')

    return { 'b': b64_b, 'u': b64_u }


def b64_from_addr(addr):
    b64_bytes = base64.urlsafe_b64decode(addr.encode('utf8'))[1:-2]
    bits = [1,0,0] + BitArray(b64_bytes) + [0, 0, 0, 0, 0]
    return base64.b64encode(bits.bytes).decode('utf8')


def getmethod(func):
    def wrapper(contract, client, stack_data=None):
        stack_data = stack_data or []
        method = func.__name__
        task = client.provider.raw_run_method(
            contract.address.to_string(),
            method=method,
            stack_data=stack_data)
        results = client._run(task)
        exit_code = results[0]['exit_code']

        if exit_code == 0:
            data = func(contract, results[0]['stack'])
            extra = None
        else:
            data = None
            extra = results

        return {'exit_code': exit_code, 'data': data, 'extra': extra}
    return wrapper
