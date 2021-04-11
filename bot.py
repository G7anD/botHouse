import logging
from aiogram import Bot, Dispatcher, executor, types
import numpy as np
from PIL import Image
from ISR.models import RDN
import os


rdn = RDN(arch_params={'C':6, 'D':20, 'G':64, 'G0':64, 'x':2})
rdn.model.load_weights('./models/noise.hdf5')
API_TOKEN = '1108700993:AAElQREFLmwdx0MR9hJKlUf2Wk5Rd0uDc30'
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
                        "kattalashtiriladigan rasm bormi? 😊",
                        reply_markup=keyboard_markup)

def image(pil):
    from io import BytesIO
    location = BytesIO()
    location.name = 'image.jpg'
    pil.save(location, 'JPEG')
    location.seek(0)
    return location

@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def enhance(message: types.Message):
    global rdn
    path = "photos/"+message.photo[-1]['file_unique_id']+".jpg"
    await message.photo[-1].download(path)
    await message.answer("Qabul qildim kutib turing...")
    img = Image.open(path)
    sr_img = rdn.predict(np.array(img))
    await message.reply_document(image(Image.fromarray(sr_img)))
    os.remove(path)


@dp.message_handler()
async def echo(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        types.InlineKeyboardButton('Batafsil ma\'lumot olish uchun', 
        url='https://t.me/quanticuz'),
    )
    await message.reply("Rasm yuboring sizga 2x kattalashtirib jo'natamiz 😊",
                                    reply_markup=keyboard_markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
