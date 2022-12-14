from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ID = None
class FSMAdmon(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=admin_kb.button_case_admin)
    await message.delete()

# Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(massage: types.Message):
    if massage.from_user.id == ID:
        await FSMAdmon.photo.set()
        await massage.reply('Загрузи фото')

# Ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmon.photo)
async def load_photo(massage: types.Message, state: FSMContext):
    if massage.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = massage.photo[0].file_id
        await FSMAdmon.next()
        await massage.reply('Теперь введи название')

# Ловим второй ответ
# @dp.message_handler(state=FSMAdmon.name)
async def load_name(massage: types.Message, state: FSMContext):
    if massage.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = massage.text
        await FSMAdmon.next()
        await massage.reply('Введи описание')

# Ловим второй ответ
# @dp.message_handler(state=FSMAdmon.description)
async def load_description(massage: types.Message, state: FSMContext):
    if massage.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = massage.text
        await FSMAdmon.next()
        await massage.reply('Теперь укажите цену')

# Ловим Последний ответ
# @dp.message_handler(state=FSMAdmon.price)
async def load_price(massage: types.Message, state: FSMContext):
    if massage.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(massage.text)

        # async with state.proxy() as data:
        #     await massage.reply(str(data))
        await sqlite_db.sql_add_command(state)
        await state.finish()

# Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        curret_state = await state.get_state()
        if curret_state is None:
            return
        await state.finish()
        await message.reply('OK')

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callbek_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f"{callback_query.data.replace('del ','')} удалена.", show_alert=True)

@dp.message_handler(commands='Удалить')
async def delete_item(message: types.message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


def reg_hendlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['модератор'], is_chat_admin=True)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['Отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmon.photo)
    dp.register_message_handler(load_description, state=FSMAdmon.description)
    dp.register_message_handler(load_name, state=FSMAdmon.name)
    dp.register_message_handler(load_price, state=FSMAdmon.price)
