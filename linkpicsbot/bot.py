from aiogram import executor, types
import os, requests
from utils import Initializer


# defining main vars
API_TOKEN = '1781635324:AAFd1clJK_Hl4YXIiguWaE8g-CsPUdMI1MY'
CHANNEL = 'quanticuz'
INVALID_INPUT = 'Rasm yuboring sizga link ko\'rinishida qaytaramiz 😊'
START_MESSAGE = 'Assalomu alaykum, sizda linkga aylantiriladigan rasm bormi? 😊'
RESTRICT_MESSAGE = 'Botimizdan foydalanish uchun kanalimizga a\'zo bo\'lib oling 🙈'

# initialize bot
utils = Initializer(API_TOKEN, CHANNEL)
bot, dp = utils.run_bot()

# call database models
from linkpicsbot.models import BotUser as Model


def get_photo_url(path):
    """ get pic url"""
    response = requests.post(
            'https://telegra.ph/upload',
            files={'file': ('file', open(path, "rb"), 'image/jpg')}
        )
    return response.json()


@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def makelink(message: types.Message):
    """ main func for doing something """

    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        types.InlineKeyboardButton('Kanalga a\'zo bo\'lish',
        url=f'https://t.me/{CHANNEL}'),
    )

    if not utils.is_member(message.from_user.id):
        await message.reply(RESTRICT_MESSAGE, reply_markup=keyboard_markup)
    else:
        keyboard_markup = types.InlineKeyboardMarkup()
        keyboard_markup.add(
            types.InlineKeyboardButton('bot Quantic LLC tomonidan ishlab chiqildi', 
            url=f'https://t.me/{CHANNEL}'),
        )
        path = "photos/"+message.photo[-1]['file_unique_id']+".jpg"
        await message.photo[-1].download(path)
        photo_url = get_photo_url(path)
        await message.reply("https://telegra.ph"+photo_url[0]['src'],
                                    reply_markup=keyboard_markup)
        os.remove(path)


# default handler functions
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """ start up """

    user = message.from_user
    await utils.register(user, Model)
    keyboard_markup = types.InlineKeyboardMarkup()

    keyboard_markup.add(
        types.InlineKeyboardButton('Kanalga a\'zo bo\'lish',
        url=f'https://t.me/{CHANNEL}'),
    )

    if utils.is_member(user.id):
        await message.reply(START_MESSAGE)
    else:
        await message.reply(RESTRICT_MESSAGE, reply_markup=keyboard_markup)


@dp.message_handler()
async def invalid(message: types.Message):
    """ response for invalid input """

    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        types.InlineKeyboardButton('Kanalga a\'zo bo\'lish',
        url=f'https://t.me/{CHANNEL}'),
    )
    if not utils.is_member(message.from_user.id):
        await message.reply(RESTRICT_MESSAGE, reply_markup=keyboard_markup)
    else:
        keyboard_markup = types.InlineKeyboardMarkup()
        keyboard_markup.add(
            types.InlineKeyboardButton('Batafsil ma\'lumot olish uchun', 
            url=f'https://t.me/{CHANNEL}'),
        )
        await message.reply(INVALID_INPUT,
                            reply_markup=keyboard_markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
