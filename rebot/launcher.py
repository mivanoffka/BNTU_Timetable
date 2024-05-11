from rebot.core import Core

# Эта череда импортов обязательна, чтобы обработчики из модуля logic зарегистрировались в диспетчере бота
from rebot.logic import admin_commands
# Несмотря на то, что в IDE эти импорты помечаются как ненужные, их НЕЛЬЗЯ УБИРАТЬ!

if __name__ == '__main__':
    Core().launch()
