from aiogram import executor, types
import os, requests
from utils import Initializer


# defining main vars
API_TOKEN = '1108700993:AAElQREFLmwdx0MR9hJKlUf2Wk5Rd0uDc30'
CHANNEL = 'QuanticUz'
INVALID_INPUT = 'Rasm yuboring sizga 2x kattalashtirib jo\'natamiz 😊'
START_MESSAGE = 'Assalomu alaykum, sizda kattalashtiriladigan rasm bormi? 😊'
RESTRICT_MESSAGE = 'Botimizdan foydalanish uchun kanalimizga a\'zo bo\'lib oling 🙈'

# initialize bot
utils = Initializer(API_TOKEN, CHANNEL)
bot, dp = utils.run_bot()

# call database models
from photogrybot.models import BotUser as Model
import numpy as np
from PIL import Image
from ISR.models import RDN

rdn = RDN(arch_params={'C':6, 'D':20, 'G':64, 'G0':64, 'x':2})
rdn.model.load_weights('./models/noise.hdf5')


def image(pil):
    """ image object """
    from io import BytesIO
    location = BytesIO()
    location.name = 'image.jpg'
    pil.save(location, 'JPEG')
    location.seek(0)
    return location


@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT])
async def enhance(message: types.Message):
    """ main func for doing something """
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        types.InlineKeyboardButton('Kanalga a\'zo bo\'lish',
        url=f'https://t.me/{CHANNEL}'),
    )
    if not utils.is_member(message.from_user.id):
        await message.reply(RESTRICT_MESSAGE, reply_markup=keyboard_markup)
    else:
        global rdn
        await message.answer("Qabul qildim kutib turing...")
        if 'document' in message and message.document['mime_type']=='image/png':
            path = "photos/"+message.document['file_unique_id']+".jpg"
            await message.document.download(path)
        elif 'document' in message and not message.document['mime_type']=='image/png':
            return await message.answer("Faqat rasm turidagi fayllar qabul qilinadi!")
        else:
            path = "photos/"+message.photo[-1]['file_unique_id']+".jpg"
            await message.photo[-1].download(path)
        keyboard_markup = types.InlineKeyboardMarkup()
        keyboard_markup.add(
            types.InlineKeyboardButton('bot Quantic LLC tomonidan ishlab chiqildi', 
            url=f'https://t.me/{CHANNEL}'),
        )
        img = Image.open(path)
        sr_img = rdn.predict(np.array(img))
        await message.reply_document(image(Image.fromarray(sr_img)), reply_markup=keyboard_markup)
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
