from aiogram import executor, types
import os
from utils import Initializer
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import datetime
import time


# defining main vars
API_TOKEN = '1784556940:AAGPZKwdcjr9RbkSnc2JnRvRSzQC-Q7oIM0'
CHANNEL = 'HappyRamazon'
INVALID_INPUT = 'Ko\'proq ma\'lumot uchun /help buyrug\'idan foydalaning'
START_MESSAGE = 'Assalomu alaykum, Ramazon tabriklariga ismingizni yozdirmoqchimisiz? 😊'
RESTRICT_MESSAGE = 'Botimizdan foydalanish uchun kanalimizga a\'zo bo\'lib oling 🙈'

# initialize bot
utils = Initializer(API_TOKEN, CHANNEL)
bot, dp = utils.run_bot()

# call database models
from happyRamazonbot.models import BotUser as Model
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


TEXT_STYLE = {
    1: (520, 580, (251, 250, 85), 85, False),
    2: (520, 520, (194, 218, 251), 85, False),
    3: (460, 450, (251, 250, 85), 120, False),
    4: (665, 630, (255, 245, 204), 27, True),
    5: (540, 617, (250, 232, 110), 170, False),
    6: (820, 780, (226, 170, 87), 120, False),
    7: (540, 540, (216, 187, 111), 75, False),
    8: (500, 580, (215, 158, 42), 95, False),
    9: (70, 680, (240, 206, 98), 110, True),
    10: (540, 420, (103, 103, 103), 40, False),
    11: (580, 80, (255, 186, 3), 130, True),
    12: (580, 80, (255, 186, 3), 130, False),
}


@dp.callback_query_handler(lambda query: True if query.data.split('_')[0] == 'gen' else False)
async def generate(query: types.CallbackQuery):
    # setup default data
    try:
        user = Model.objects.get(user_id=query.message.chat.id)
        name = user.custom_name
    except:
        name = "Ism o'rnatilmagan"

    current_number: int = int(query.data.split('_')[1])
    w, h, font_color, font_size, not_center = TEXT_STYLE[current_number]

    # prepare
    choosen_img = Image.open(f'happyRamazonbot/pictures/{current_number}.jpg')
    W, H = choosen_img.size
    drawen_photo = ImageDraw.Draw(choosen_img)
    Font = ImageFont.truetype(
        f'happyRamazonbot/fonts/{current_number}.ttf', font_size)

    # Add Text to an image
    w_, h_ = drawen_photo.textsize(name, font=Font)
    width = w if not_center else (W-w_)/2
    drawen_photo.text((width, h), name, font=Font, fill=font_color)

    # save image to memory
    final_image = BytesIO()
    final_image.name = 'ramadan.jpg'
    choosen_img.save(final_image, "JPEG")
    final_image.seek(0)

    await bot.send_photo(query.message.chat.id, final_image)


@dp.callback_query_handler(lambda query: query.data == 'change_name')
async def start_choosing(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    try:
        user = Model.objects.get(user_id=chat_id)
        user.custom_name_change_is_open = True
        user.save()
    except:
        pass

    await bot.send_message(chat_id, "Ismingizni yuboring 🖋")


@dp.callback_query_handler(lambda query: True if query.data.split('_')[0] == 'choose' else False)
async def start_choosing(query: types.CallbackQuery):
    current_number = int(query.data.split('_')[1])
    inline_key = types.InlineKeyboardMarkup()
    max_number = len(os.listdir('happyRamazonbot/pictures'))
    inline_key.row(
        *(types.InlineKeyboardButton('⏪',
                                     callback_data=f'navi_{max_number}'),
            types.InlineKeyboardButton('⏩',
                                       callback_data=f'navi_{current_number+1}'),
          )
    )
    inline_key.row(
        types.InlineKeyboardButton('Ismni o\'zgartirish ✍️',
                                   callback_data=f'change_name'),
        types.InlineKeyboardButton('Yasash ✅',
                                   callback_data=f'gen_{current_number}'),
    )

    await bot.send_photo(query.message.chat.id,
                         open(
                             f'happyRamazonbot/pictures/{current_number}.jpg', 'rb'),
                         reply_markup=inline_key)


@dp.callback_query_handler(lambda query: True if query.data.split('_')[0] == 'navi' else False)
async def navigation_based(query: types.CallbackQuery):
    current_number = int(query.data.split('_')[1])
    inline_key = types.InlineKeyboardMarkup()

    max_number = len(os.listdir('happyRamazonbot/pictures'))
    if current_number < max_number and current_number != 1:
        inline_key.row(
            *(types.InlineKeyboardButton('⏪',
                                         callback_data=f'navi_{current_number-1}'),
              types.InlineKeyboardButton('⏩',
                                         callback_data=f'navi_{current_number+1}'),
              )
        )
        inline_key.row(
            types.InlineKeyboardButton('Ismni o\'zgartirish ✍️',
                                       callback_data=f'change_name'),
            types.InlineKeyboardButton('Yasash ✅',
                                       callback_data=f'gen_{current_number}'),
        )

    elif current_number == max_number:
        inline_key.row(
            *(types.InlineKeyboardButton('⏪',
                                         callback_data=f'navi_{current_number-1}'),
              types.InlineKeyboardButton('⏩',
                                         callback_data=f'navi_{1}'),
              )
        )
        inline_key.row(
            types.InlineKeyboardButton('Ismni o\'zgartirish ✍️',
                                       callback_data=f'change_name'),
            types.InlineKeyboardButton('Yasash ✅',
                                       callback_data=f'gen_{current_number}'),
        )

    elif current_number == 1:
        inline_key.row(
            *(types.InlineKeyboardButton('⏪',
                                         callback_data=f'navi_{max_number}'),
              types.InlineKeyboardButton('⏩',
                                         callback_data=f'navi_{current_number+1}'),
              )
        )
        inline_key.row(
            types.InlineKeyboardButton('Ismni o\'zgartirish ✍️',
                                       callback_data=f'change_name'),
            types.InlineKeyboardButton('Yasash ✅',
                                       callback_data=f'gen_{current_number}'),
        )

    await bot.edit_message_media(
        types.input_media.InputMediaPhoto(
            open(f'happyRamazonbot/pictures/{current_number}.jpg', 'rb')),
        query.message.chat.id, query.message.message_id, reply_markup=inline_key)


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
        inline_key = types.InlineKeyboardMarkup()
        inline_key.add(
            types.InlineKeyboardButton('Rasm tanlash',
                                       callback_data='choose_1'),
        )
        await message.reply(START_MESSAGE, reply_markup=inline_key)
    else:
        await message.reply(RESTRICT_MESSAGE, reply_markup=keyboard_markup)


def make_stat():
    inline_key = types.InlineKeyboardMarkup()
    all_user = Model.objects.all().count()
    left = Model.objects.filter(is_send=False).count()
    send = Model.objects.filter(is_send=True).count()

    today = datetime.date.today()

    todays = Model.objects.filter(
        created_at__year=today.year,
        created_at__month=today.month,
        created_at__day=today.day).count()

    yesterdays_user = Model.objects.filter(
        created_at__year=today.year,
        created_at__month=today.month,
        created_at__day=today.day-1).count()

    statistics = "📊 *Statistika*\n"\
                 f"🔹 Barcha foydalanuvchilar: *{all_user}*\n"\
                 f"🔹 Bugun qo'shilganlar: *{todays}*\n"\
                 f"🔹 Kecha qo'shilganlar: *{yesterdays_user}*\n\n"\
                 f"📨 *So'nggi jo'natilgan xabar*\n"\
                 f"🔸 Xabar jo'natilmaganlar: *{left}*\n"\
                 f"🔸 Xabar jo'natilganlar: *{send}*"
    inline_key.add(
        types.InlineKeyboardButton('Hisoblagichni yangilash 🔄',
                                   callback_data='renew'),
    )
    return (statistics, inline_key, send)


@dp.callback_query_handler(lambda query: query.data == 'renew')
async def renew_counter(query: types.CallbackQuery):
    try:
        Model.objects.all().update(is_send=False)
        statistics, __, _ = make_stat()
    except:
        pass

    await query.message.edit_text(statistics, parse_mode='Markdown')


@dp.message_handler(user_id=['228305651', '1703644018'], commands=['stat'])
async def stat(message: types.Message):
    """ getting stat from db """
    statistics, inline_key, is_blank = make_stat()
    if is_blank != 0:
        await message.reply(statistics, reply_markup=inline_key, parse_mode='Markdown')
    else:
        await message.reply(statistics, parse_mode='Markdown')


# default handler functions
@dp.message_handler(user_id=['228305651', '1703644018'])
async def ads(message: types.Message):
    """ start up """
    if 'forward_from' in message:
        users = Model.objects.all()
        for user in users:
            if not user.is_send:
                try:
                    await message.send_copy(user.user_id)
                except Exception as e:
                    e = str(e)
                    if "Flood" in e:
                        user.send_error = "flood"
                    elif "bot was blocked" in e:
                        user.send_error = "bot was blocked by the user"
                    else:
                        user.send_error = str(e)
                user.is_send = True
                user.save()


@dp.message_handler()
async def invalid(message: types.Message):
    """ response for invalid input """

    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.add(
        types.InlineKeyboardButton('Kanalga a\'zo bo\'lish',
                                   url=f'https://t.me/{CHANNEL}'),
    )

    try:
        user = Model.objects.get(user_id=message.from_user.id)
        state = user.custom_name_change_is_open
    except:
        state = False

    if not utils.is_member(message.from_user.id):
        await message.reply(RESTRICT_MESSAGE, reply_markup=keyboard_markup)
    elif state:
        user.custom_name = message.md_text
        user.custom_name_change_is_open = False
        user.save()
        await message.reply("Saqlandi 🎯")
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
