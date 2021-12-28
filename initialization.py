import environ
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from helpers import STATUS

env = environ.Env()
environ.Env.read_env()


class TelegramBot:
    def __init__(self):
        BOT_TOKEN = env('BOT_TOKEN')
        self.bot = Bot(token=BOT_TOKEN)
        self.dispatcher = Dispatcher(self.bot, storage=MemoryStorage())

    @property
    def dp(self):
        return self.dispatcher


class UserBot:
    def __init__(self):
        API_ID = env.int('API_ID')
        API_HASH = env('API_HASH')
        self.client = TelegramClient('session', API_ID, API_HASH)
        self.phone = env('PHONE')
        self.storage = {}

    async def user_bot_joinchanel(self, apigroup: str) -> dict:
        try:
            result = await self.client(JoinChannelRequest(channel=apigroup))
            chat_id = result.chats[0].id
        except (ValueError, TypeError) as e:
            print(repr(e))
            return {'status': STATUS.ERROR,
                    'result': 'Не получилось подключиться к группе'}
        return {'status': STATUS.OK,
                'result': chat_id}

    async def search_text(self, chat_id: str, search: str) -> dict:
        try:
            messages = [message async for message in
                        self.client.iter_messages(entity=chat_id,
                                                  search=search) if
                        message.message]

            messages.sort(key=lambda msg: msg.views if msg.views else int(
                msg.date.timestamp()))

            result_list = messages[:10]
        except Exception as e:
            print(repr(e))
            return {'status': STATUS.ERROR,
                    'result': 'Ошибка при поиске'}
        return {'status': STATUS.OK,
                'result': tuple(map(lambda x: x.message, result_list))}

    async def sign_in(self):
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            await self.client.sign_in(self.phone, input('Enter code: '))
        return STATUS.OK
