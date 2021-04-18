import logging
from aiogram import Bot, Dispatcher, executor, types
import os
import requests


API_TOKEN = '1768766909:AAEmG8Wnl1ri_4mWDeNPE6nsGW_8eyMnYC4'
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
                        "oq-qora rasm bormi? Biz uni rangli qilib beramiz. 😊",
                        reply_markup=keyboard_markup)


@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def makelink(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        types.InlineKeyboardButton('bot Quantic LLC tomonidan ishlab chiqildi', 
        url='https://t.me/quanticuz'),
    )
    path = "photos/"+message.photo[-1]['file_unique_id']+".jpg"
    await message.photo[-1].download(path)
    r = requests.post(
        "https://api.deepai.org/api/colorizer",
        files={
            'image': open(path, 'rb'),
        },
        headers={'api-key': '80f8a4de-a59f-410a-b5d2-4d234cc3bf5e'}
    )
    await message.reply_photo(r.json()['output_url'],
                        reply_markup=keyboard_markup)
    os.remove(path)


@dp.message_handler()
async def echo(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        types.InlineKeyboardButton('Batafsil ma\'lumot olish uchun', 
        url='https://t.me/quanticuz'),
    )
    await message.reply("Oq-Qora rasm yuboring sizga rangli ko'rinishida qaytaramiz 😊",
                                    reply_markup=keyboard_markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
