from aiogram import types

from dispatcher import dp, bot
from tinkoff_bonds.bonds import best_bonds_message
from config import TELEGRAM_BOT_OWNER


@dp.message_handler(commands=['start'])
async def info(message: types.Message):
    await bot.send_message(TELEGRAM_BOT_OWNER, 'Бот включен')
    await message.answer(best_bonds_message())
    # print('Message')
