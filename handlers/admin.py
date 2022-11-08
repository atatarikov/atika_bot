from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text


ID = None
class FSMAdmon(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что хозяин надо???')
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

        async with state.proxy() as data: 
            await massage.reply(str(data))

        await state.finish()

# Выход из состояний
async def cancel_handler(massage: types.Message, state: FSMContext):
    if massage.from_user.id == ID:
        curret_state = await state.get_state()
        if curret_state is None:
            return
        await state.finish()
        await massage.reply('OK')

def reg_hendlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['модератор'], is_chat_admin=True)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['Отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmon.photo)
    dp.register_message_handler(load_description, state=FSMAdmon.description)
    dp.register_message_handler(load_name, state=FSMAdmon.name)
    dp.register_message_handler(load_price, state=FSMAdmon.price)
