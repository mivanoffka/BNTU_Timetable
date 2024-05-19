from rebot.core import Core
from aiogram import types
from aiogram.filters import Command
from aiogram_dialog.api.exceptions import UnknownIntent

core: Core = Core()


@core.message(Command("echo"))
async def process_echo_command(message: types.Message):
    raise UnknownIntent("a")
    print("hi")
    text: str = message.get_args()
    if not text:
        text = "echo"
    await core.messenger.send_independent_message(message.from_id, text)


