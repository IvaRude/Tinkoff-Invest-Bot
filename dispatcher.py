from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TELEGRAM_BOT_TOKEN
from interfaces import TinkoffBondGetter
from rpc.rpc_tinkoff_bond_getter import RPCTinkoffBondGetter

bot = Bot(token=TELEGRAM_BOT_TOKEN)


class TinkoffBondDispatcher(Dispatcher):
    def __init__(self, *args, **kwargs):
        self.bond_getter: TinkoffBondGetter = RPCTinkoffBondGetter()
        super().__init__(*args, **kwargs)


# dp = Dispatcher(bot, storage=MemoryStorage())
dp = TinkoffBondDispatcher(bot, storage=MemoryStorage())
