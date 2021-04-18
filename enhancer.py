import logging
from aiogram import Bot, Dispatcher, executor, types
import numpy as np
from PIL import Image
from ISR.models import RDN
import os, sys
import json
import django


path_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(path_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
django.setup()
from .models import EnhanceUser
from asgiref.sync import sync_to_async


rdn = RDN(arch_params={'C':6, 'D':20, 'G':64, 'G0':64, 'x':2})
rdn.model.load_weights('./models/noise.hdf5')
API_TOKEN = '1108700993:AAElQREFLmwdx0MR9hJKlUf2Wk5Rd0uDc30'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def is_member(user_id):
    """ check user is member of channel """

    TOKEN = "1108700993:AAElQREFLmwdx0MR9hJKlUf2Wk5Rd0uDc30"
    CHANNEL_ID = "@quanticuz"

    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={CHANNEL_ID}&user_id={user_id}"

    response = requests.get(url)
    is_member = json.loads(response.text)

    if is_member['ok']:
        return is_member['result']['status'] in ['creator', 'administrator', 'member']
    else:
        return False


@sync_to_async
def register(user):
    try:
        EnhanceUser(user_id=user.id, firstname=user.first_name,
                lastname=user.last_name, username=user.username).save()
    except EnhanceUser.DoesNotExist:
        pass

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
