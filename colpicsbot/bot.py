from aiogram import executor, types
import os, requests
from utils import Initializer


# defining main vars
API_TOKEN = '1768766909:AAEmG8Wnl1ri_4mWDeNPE6nsGW_8eyMnYC4'
CHANNEL = 'quanticuz'
INVALID_INPUT = 'Oq-Qora rasm yuboring sizga rangli ko\'rinishida qaytaramiz 😊'
START_MESSAGE = 'Assalomu alaykum, sizda oq-qora rasm bormi? Biz uni rangli qilib beramiz. 😊'
RESTRICT_MESSAGE = 'Botimizdan foydalanish uchun kanalimizga a\'zo bo\'lib oling 🙈'

# initialize bot
utils = Initializer(API_TOKEN, CHANNEL)
bot, dp = utils.run_bot()

# call database models
from colpicsbot.models import BotUser as Model


@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT])
async def colorize(message: types.Message):

    user = message.from_user
    keyboard_markup = types.InlineKeyboardMarkup()

    keyboard_markup.add(
        types.InlineKeyboardButton('Kanalga a\'zo bo\'lish',
        url=f'https://t.me/{CHANNEL}'),
    )
    if not utils.is_member(user.id):
        await message.reply(RESTRICT_MESSAGE, reply_markup=keyboard_markup)
    else:
        await message.answer("Qabul qildim kutib turing...")
        keyboard_markup = types.InlineKeyboardMarkup()
        keyboard_markup.add(
            types.InlineKeyboardButton('bot Quantic LLC tomonidan ishlab chiqildi', 
            url='https://t.me/quanticuz'),
        )
        if 'document' in message and message.document['mime_type']=='image/png':
            path = "photos/"+message.document['file_unique_id']+".jpg"
            await message.document.download(path)
        elif 'document' in message and not message.document['mime_type']=='image/png':
            return await message.answer("Faqat rasm turidagi fayllar qabul qilinadi!")
        else:
            path = "photos/"+message.photo[-1]['file_unique_id']+".jpg"
            await message.photo[-1].download(path)

        r = requests.post(
            "https://api.deepai.org/api/colorizer",
            files={
                'image': open(path, 'rb'),
            },
            headers={'api-key': '80f8a4de-a59f-410a-b5d2-4d234cc3bf5e'}
        )
        await message.reply_document(r.json()['output_url'],
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
