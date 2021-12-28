from aiogram import Dispatcher, executor, types

from helpers import BOT_STATE, STATUS
from initialization import TelegramBot, UserBot

dp = TelegramBot().dp
user_bot = UserBot()


@dp.message_handler(state='*', commands="start")
async def start_handler(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Начать поиск"))
    poll_keyboard.add(types.KeyboardButton(text="Отмена"))
    await message.answer(
        "Введите /help  чтобы узнать как работать с ботом или "
        "нажмите на кнопку ниже чтобы перейти к поиску!",
        reply_markup=poll_keyboard)


@dp.message_handler(state='*', commands="help")
async def help_handler(message: types.Message):
    await message.answer(
        "Этот бот ищет заданный текст в каналах, "
        "Чтобы начать поиск нажимаете на кнопку 'Начать поиск', "
        "потом введите канал в котором надо произвести поиск, "
        "а затем текст который искать",
        reply=False)


@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer(
        "Действие отменено. Введите /start, чтобы начать заново.",
        reply_markup=remove_keyboard)


@dp.message_handler(lambda message: message.text == "Начать поиск")
async def connect_group(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await state.set_state(BOT_STATE.all()[0])
    await message.answer(
        "введите название группы в формате https://t.me/ + название канала")


@dp.message_handler(state=BOT_STATE.STATE_GROUP)
async def connect_to_chanel(message: types.Message):
    argument = message.text
    res = await user_bot.user_bot_joinchanel(argument)
    if res['status'] == STATUS.OK:
        user_bot.storage[message.from_user.id] = res['result']
        await message.reply(
            'подключились к каналу, введите текст который искать !',
            reply=False)
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(BOT_STATE.all()[1])
    else:
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()
        await message.reply('Подключиться не получилось!', reply=False)


@dp.message_handler(state=BOT_STATE.STATE_SEARCH)
async def search_text(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    apigroup = user_bot.storage.get(message.from_user.id)
    await state.reset_state()
    if not apigroup:
        await message.reply('Что-то пошло не так начните поиск заново!',
                            reply=False)
    res = await user_bot.search_text(apigroup, message.text)
    if res['status'] == STATUS.ERROR:
        await message.reply('Что-то пошло не так начните поиск заново!',
                            reply=False)
    if not len(res['result']):
        await message.reply('Мы ничего не нашли!', reply=False)
    else:
        for line in res['result']:
            await message.answer(line)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    client = user_bot.client
    with client:
        result = client.loop.run_until_complete(user_bot.sign_in())
        executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
