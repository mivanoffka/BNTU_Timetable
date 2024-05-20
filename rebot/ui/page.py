from typing import Optional, List

from aiogram.fsm.state import State
from aiogram.types import UNSET_PARSE_MODE
from aiogram.types.base import UNSET_DISABLE_WEB_PAGE_PREVIEW
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog.widgets.markup.inline_keyboard import InlineKeyboardFactory
from aiogram_dialog.api.internal.widgets import MarkupFactory
from aiogram_dialog.widgets.utils import WidgetSrc, GetterVariant

from rebot.core import core

_DEFAULT_MARKUP_FACTORY = InlineKeyboardFactory()


class Page(Window):

    def __init__(self,
                 *widgets: WidgetSrc,
                 state: State,
                 getter: GetterVariant = None,
                 markup_factory: MarkupFactory = _DEFAULT_MARKUP_FACTORY,
                 parse_mode: Optional[str] = UNSET_PARSE_MODE,
                 disable_web_page_preview: Optional[bool] = UNSET_DISABLE_WEB_PAGE_PREVIEW,  # noqa: E501
                 preview_add_transitions: Optional[List[Keyboard]] = None,
                 preview_data: GetterVariant = None):

        super().__init__(*widgets,
                         state=state,
                         getter=getter,
                         markup_factory=markup_factory,
                         parse_mode=parse_mode,
                         disable_web_page_preview=disable_web_page_preview,
                         preview_add_transitions=preview_add_transitions,
                         preview_data=preview_data)

        core.include_window(self)
