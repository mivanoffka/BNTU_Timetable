from rebot.core import Core
import asyncio
# Эта череда импортов обязательна, чтобы обработчики из модуля logic зарегистрировались в диспетчере бота
from rebot.ui import dialog
from rebot.logic.admin_commands import process_echo_command
# Несмотря на то, что в IDE эти импорты помечаются как ненужные, их НЕЛЬЗЯ УБИРАТЬ!

if __name__ == '__main__':
    asyncio.run(Core().launch())
