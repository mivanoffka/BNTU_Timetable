from enum import Enum


class ButtonKeys(Enum):
    BACK: int = 0,
    CANCEL: int = 1,
    GROUP_INPUT: int = 2,

    TODAY: int = 3,
    TOMORROW: int = 4,
    WEEKDAYS: int = 5,
    DISTRIBUTION: int = 6,
    OPTIONS: int = 7,

    TRY_AGAIN: int = 8,
    CONTINUE: int = 9,

    WEBSITE: int = 10,
    DONATIONS: int = 11,
    HELP: int = 12,
    REPORT: int = 13,

    HOME: int = 14,

    MORNING: int = 15,
    EVENING: int = 16,
    SILENT: int = 17,

    MONDAY: int = 18,
    TUESDAY: int = 19,
    WEDNESDAY: int = 20,
    THURSDAY: int = 21,
    FRIDAY: int = 22,
    SATURDAY: int = 23,
    SUNDAY: int = 24

    YES: int = 25
    NO: int = 26

    GROUP_INPUT_SHORTENED: int = 27,
    WEBSITE_SHORTENED: int = 28
    ADMIN_PANEL: int = 29,

    BROADCAST: int = 30,
    TIMETABLE_SETTINGS: int = 31,
    STATS: int = 32,
    ROLLBACK: int = 33,
    MESSENGER: int = 34


_ = ButtonKeys

button_labels_rus: dict[int, str] = {
    _.BACK: "Назад ↩️",
    _.CANCEL: "Отмена ✖️",
    _.GROUP_INPUT: "Указать группу ✏️",

    _.TODAY: "Сегодня 📓",
    _.TOMORROW: "Завтра 📔",
    _.WEEKDAYS: "Выбрать день недели 🔍",
    _.DISTRIBUTION: "Рассылка 📩",
    _.OPTIONS: "Опции ⚙️️",

    _.TRY_AGAIN: "Повторить ввод 🔄",
    _.CONTINUE: "Продолжить ➡️",

    _.WEBSITE: "Сайт БНТУ 🏛️",
    _.DONATIONS: "Поддержать нас денюжкой 🏦💞",
    _.REPORT: "Отзыв 📬️",
    _.HELP: "Справка 💡",
    _.HOME: "На главную 🏠",

    _.MORNING: "Утром 🌇",
    _.EVENING: "Вечером 🌃",
    _.SILENT: "Никогда 🔕",

    _.MONDAY: "Пн. ⚫",
    _.TUESDAY: "Вт. ⚪️",
    _.WEDNESDAY: "Ср. ⚫",
    _.THURSDAY: "Чт. ⚪",
    _.FRIDAY: "Пт. ⚫",
    _.SATURDAY: "Сб. ⚪",

    _.YES: "Да ✅",
    _.NO: "Нет ❌",

    _.GROUP_INPUT_SHORTENED: "Группа ✏️",
    _.WEBSITE_SHORTENED: "Сайт 🏛️",
    _.ADMIN_PANEL: "Панель 🛠️",

    _.BROADCAST: "Новость 🗞️",
    _.STATS: "Статистика 📊",
    _.TIMETABLE_SETTINGS: "Настройки расписания 📚",
    _.ROLLBACK: "Откат 🔻",
    _.MESSENGER: "Сообщения 💬"

}

