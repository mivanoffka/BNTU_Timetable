class ButtonLabelKeys:
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


_ = ButtonLabelKeys

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

}


def get_button_label(key: int) -> str:
    return button_labels_rus[key]


