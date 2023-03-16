from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token='6261194334:AAFYNtLG8jcHJn8LmN6axv6tbtOVw5SsiLA')
dp = Dispatcher(bot)

BASE = {}
@dp.message_handler(commands=['start'])
async def start(message):
    BASE[message.chat.id] = ['', message.from_user.username, True, 0]
    await bot.send_message(message.chat.id, "Привет, я бот, который мало чего умеет, поэтому меня называют Шляпный. Напиши /help, если тебе всё ещё интересно.")
    print(BASE)

@dp.message_handler(commands=['help'])
async def help(message):
    await bot.send_message(message.chat.id, "/reg - Познакомиться\n"
                                            "/help - Что умеет бот\n"
                                            "/start - Запуск бота")
    print(BASE)
@dp.message_handler(commands=['reg'])
async def reg(message):
    BASE[message.chat.id] = ['', message.from_user.username, True]
    await bot.send_message(message.chat.id, "Как тебя зовут?")
    print(BASE)

@dp.message_handler(content_types=['text'])
async def main(message):
    global BASE
    keys = list(BASE.keys())
    if message.chat.id not in keys:
       await bot.send_message(message.chat.id, "Тебе нужно заргистрироваться, напиши /start")
    else:
        keys.pop(keys.index(message.chat.id))
        from_user = BASE[message.chat.id].copy()

        btn_n = KeyboardButton('База данных')
        btn_ch = KeyboardButton('Изменить данные')
        btn_help = KeyboardButton('Обратная связь')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_ch, btn_n, btn_help)

        if from_user[2]:
            from_user[2] = False
            from_user[0] = message.text
            if len(keys) == 0:
                await bot.send_message(message.chat.id, 'Приятно познакомиться!', reply_markup=markup)
            else:
                await bot.send_message(message.chat.id, f"Первая строка:\n"
                                                        f"{BASE[keys[0]][0]}\n"
                                                        f"Telegram: @{BASE[keys[0]][1]}", reply_markup=markup)
                from_user[3] += 1
        else:
            if message.text == 'Приятно познакомиться!':
                await bot.send_message(message.chat.id, 'Как тебя зовут?')
                from_user[2] = True
            elif message.text == 'Приятно познакомиться!':
                await bot.send_message(message.chat.id, 'Бот в разработке, если что пиши сюда - @DocLives')
            elif message.text == 'Next':
                if len(keys) == 0:
                    await bot.send_message(message.chat.id, 'Данные пока отсутствуют в базе, немного подождите...')
                else:
                    an = BASE[keys[from_user[3] % len(keys)]]
                    await bot.send_message(message.chat.id, f"Next:\n"
                                                            f"{an[0]}\n"
                                                            f"Telegram: @{an[1]}")
                    from_user[3] += 1
            else:
                await bot.send_message(message.chat.id, 'Нет такой команды')
        if from_user[3] % 100 == 0 and from_user[3] != 0:
            await bot.send_message(message.chat.id, f"Просмотрено{from_user[3]} данных")
        BASE[message.chat.id] = from_user.copy()
        from_user.clear()
        print(BASE)

if __name__ == '__main__':
    executor.start_polling(dp)