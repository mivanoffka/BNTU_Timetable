from aiogram_dialog.dialog import Dialog
from rebot.ui.pages.start import start_page
from rebot.ui.pages.group_input import group_input_page
from rebot.ui.pages.home import home_page
from rebot.ui.pages.weekdays import weekdays_page
from rebot.ui.pages.distribution import distribution_page
from rebot.ui.pages.options import options_page
from rebot.ui.pages.message import message_page
from rebot.ui.pages.report_input import report_input_page
from rebot.ui.pages.alternative_message import alternative_message_page

import rebot.ui.errors

from rebot.core import core

dialog: Dialog = Dialog(start_page, group_input_page, home_page, weekdays_page, distribution_page,
                        options_page, message_page, report_input_page, alternative_message_page)

core.include_router(dialog)

