from interfaces import TinkoffBondGetter
from rpc.rpc_client import get_rpc_client


class RPCTinkoffBondGetter(TinkoffBondGetter):
    def __init__(self):
        self.rpc_generator = get_rpc_client()

    async def get_bonds(self, rate: str):
        rpc_client = await anext(self.rpc_generator)
        bonds_answer = await rpc_client.call('get_bonds_message', kwargs=dict(rate=rate))
        return bonds_answer
