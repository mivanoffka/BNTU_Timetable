from rebot.ui.text.button_texts import button_labels_rus as _buttons, ButtonKeys
from rebot.ui.text.message_texts import messages_rus as _messages, MessageKeys

_strings: dict[ButtonKeys | MessageKeys, str] = {
    **_buttons, **_messages
}


def get(key: ButtonKeys | MessageKeys) -> str:
    return _strings[key]
