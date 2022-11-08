from pydoc import cli
from aiogram.utils import executor
from create_bot import dp

async def on_startup(_):
    print('Бот вышел в онлайн')

from handlers import client, admin, other

client.reg_hendlers_client(dp)
admin.reg_hendlers_admin(dp)
other.reg_hendlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
