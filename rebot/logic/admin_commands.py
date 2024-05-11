from rebot.core import Core
from aiogram import types
from aiogram.filters import Command

core: Core = Core()


@core.message(Command("echo"))
async def process_echo_command(message: types.Message):
    print("hi")
    text: str = message.get_args()
    if not text:
        text = "echo"
    await core.dialog.send_independent_message(message.from_id, text)


