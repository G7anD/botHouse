import logging
from aiogram import Bot, Dispatcher, executor, types
import os
import requests

API_TOKEN = '1781635324:AAFd1clJK_Hl4YXIiguWaE8g-CsPUdMI1MY'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        types.InlineKeyboardButton('Batafsil ma\'lumot olish uchun', 
        url='https://t.me/quanticuz'),
    )
    await message.reply("Assalomu alaykum, sizda " \
                        "linkga aylantiriladigan rasm bormi? 😊",
                        reply_markup=keyboard_markup)


def get_photo_url(path):
    response = requests.post(
            'https://telegra.ph/upload',
            files={'file': ('file', open(path, "rb"), 'image/jpg')}
        )
    return response.json()

@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def makelink(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        types.InlineKeyboardButton('bot Quantic LLC tomonidan ishlab chiqildi', 
        url='https://t.me/quanticuz'),
    )
    path = "photos/"+message.photo[-1]['file_unique_id']+".jpg"
    await message.photo[-1].download(path)
    photo_url = get_photo_url(path)
    await message.reply("https://telegra.ph"+photo_url[0]['src'],
                                reply_markup=keyboard_markup)
    os.remove(path)


@dp.message_handler()
async def echo(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        types.InlineKeyboardButton('Batafsil ma\'lumot olish uchun', 
        url='https://t.me/quanticuz'),
    )
    await message.reply("Rasm yuboring sizga link ko'rinishida qaytaramiz 😊",
                                    reply_markup=keyboard_markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
