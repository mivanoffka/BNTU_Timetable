from rebot.core import Core
from aiogram import types

core: Core = Core()


@core.message_handler(commands=["echo"])
async def process_echo_command(message: types.Message):
    text: str = message.get_args()
    await core.dialog.send_independent_message(message.from_id, text)


