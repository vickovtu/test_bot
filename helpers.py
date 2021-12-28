from enum import Enum

from aiogram.utils.helper import Helper, ListItem, HelperMode


class BOT_STATE(Helper):
    mode = HelperMode.snake_case
    STATE_GROUP = ListItem()
    STATE_SEARCH = ListItem()


class STATUS(Enum):
    OK = 'ok'
    ERROR = 'error'
