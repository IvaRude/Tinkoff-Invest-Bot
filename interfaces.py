from abc import abstractmethod


class TinkoffBondGetter:
    @abstractmethod
    async def get_bonds(self, rate: str):
        pass
