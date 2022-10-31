from aiogram import types, Dispatcher
from create_bot import dp, bot

# @dp.message_handler()
async def echo_send(message: types.Message):
    if message.text == 'Привет':
        await message.answer('И тебе привет!')
    await message.reply("репл " + message.text)
    await bot.send_message(message.from_user.id, "сендМес " + message.text)
    await message.answer("ансв " + message.text)

def reg_hendlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send )