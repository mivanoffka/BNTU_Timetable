from rebot.core import Core
import asyncio
# Эта череда импортов обязательна, чтобы обработчики из модуля logic зарегистрировались в диспетчере бота
import rebot.ui
from rebot.data import tracker
# Несмотря на то, что в IDE эти импорты помечаются как ненужные, их НЕЛЬЗЯ УБИРАТЬ!

if __name__ == '__main__':
    asyncio.run(Core().launch())
