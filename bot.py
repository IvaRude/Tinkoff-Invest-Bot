import logging

from aiogram import types
from aiogram.utils import executor

from dispatcher import dp
from tinkoff_bonds.bonds import best_bonds_message

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def info(message: types.Message):
    await message.answer(best_bonds_message())


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
