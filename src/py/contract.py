'''
    Proxy base contract class.
'''
from abc import abstractmethod

from tonsdk.contract import Contract as ContractBase
from tonsdk.boc import Cell
from tonsdk.utils import to_nano, bytes_to_b64str


class Contract(ContractBase):
    def __init__(self, **kwargs):
        self.code = kwargs.get('code') or self.code
        kwargs['code'] = Cell.one_from_boc(self.code)

        super().__init__(**kwargs)


    @abstractmethod
    def create_data_cell(self) -> Cell:
        pass

    # API

    def api_call(self, 
                 wallet, client,
                 op_amount, state_init=None, payload=None,
                 send=True):
        seqno = client.seqno(wallet.address.to_string())
        seqno = int(seqno[0]['stack'][0][1], 16)

        query = wallet.create_transfer_message(
            to_addr=self.address,
            amount=to_nano(op_amount, 'ton'),
            seqno=seqno,
            state_init=state_init,
            payload=payload,
        )
        transfer_boc = query['message'].to_boc(False)

        result = client.send_boc(transfer_boc) if send else None

        return { 'boc': bytes_to_b64str(transfer_boc), 'result': result }

    # GET

    @staticmethod
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
