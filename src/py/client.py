import asyncio
import aiohttp

from tvm_valuetypes import serialize_tvm_stack
from tonsdk.provider import prepare_address, address_state
from tonsdk.utils import TonCurrencyEnum, from_nano
from tonsdk.boc import Cell
from tonsdk.provider import ToncenterClient


TESTNET_URL    = 'https://testnet.toncenter.com/api/v2/'
TESTNET_APIKEY = '76577d29bdc879791f7470c117c3aac144d0b41583dd81fbe4e831740313bce5'


class TonCenterTonClient:
    '''
    TON Client backend.
    '''
    def __init__(self,
                 base_url=TESTNET_URL,
                 api_key=TESTNET_APIKEY):
        self.loop = asyncio.get_event_loop()
        self.base_url = base_url
        self.api_key = api_key
        self.provider = ToncenterClient(base_url=base_url, api_key=api_key)

    def get_address_information(self, address: str,
                                currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton):
        return self.get_addresses_information([address], currency_to_show)[0]

    def get_addresses_information(self, addresses,
                                  currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton):
        if not addresses:
            return []

        tasks = []
        for address in addresses:
            address = prepare_address(address)
            tasks.append(self.provider.raw_get_account_state(address))

        results = self._run(tasks, single_query=False)

        for result in results:
            result["state"] = address_state(result)
            if "balance" in result:
                if int(result["balance"]) < 0:
                    result["balance"] = 0
                else:
                    result["balance"] = from_nano(
                        int(result["balance"]), currency_to_show)

        return results
    
    def seqno(self, addr: str):
        addr = prepare_address(addr)
        result = self._run(self.provider.raw_run_method(addr, "seqno", []))

        if 'stack' in result and ('@type' in result and result['@type'] == 'smc.runResult'):
            result['stack'] = serialize_tvm_stack(result['stack'])

        return result

    def send_boc(self, boc: Cell):
        return self._run(self.provider.raw_send_message(boc))

    async def __execute(self, to_run, single_query):
        timeout = aiohttp.ClientTimeout(total=5)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            if single_query:
                to_run = [to_run]

            tasks = []
            for task in to_run:
                tasks.append(task["func"](
                    session, *task["args"], **task["kwargs"]))

            return await asyncio.gather(*tasks)

    def _run(self, to_run, *, single_query=True):
        try:
            return self.loop.run_until_complete(
                self.__execute(to_run, single_query))

        except Exception:  # ToncenterWrongResult, asyncio.exceptions.TimeoutError, aiohttp.client_exceptions.ClientConnectorError
            raise
