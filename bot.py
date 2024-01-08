import logging

from aiogram import types
from aiogram.utils import executor

import rpc.rpc_client
from dispatcher import dp
from tinkoff_bonds.bonds import best_bonds_message, async_best_bonds_message

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def info(message: types.Message):
    await message.answer(
        'Привет! Выбери какие тебя интересуют облигации. '
        'Если высокого рейтинга, то напиши /high, если среднего - /medium. Если же любого, то /all.')


@dp.message_handler(commands=['all', 'high', 'medium'])
async def info(message: types.Message):
    # await message.answer(best_bonds_message(message.text[1:]))
    # await message.answer(await async_best_bonds_message(message.text[1:]))
    rate = message.text[1:]
    await message.answer(await dp.bond_getter.get_bonds(rate))


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
