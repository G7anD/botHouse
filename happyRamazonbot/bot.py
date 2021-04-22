from aiogram import executor, types
import os
import requests
from utils import Initializer
from nider.models import Header
from nider.models import Content
from nider.models import Image
from nider.core import Font


# defining main vars
API_TOKEN = '1784556940:AAGPZKwdcjr9RbkSnc2JnRvRSzQC-Q7oIM0'
CHANNEL = 'INVESTOR_HD'
INVALID_INPUT = 'Ko\'proq ma\'lumot uchun /help buyrug\'idan foydalaning'
START_MESSAGE = 'Assalomu alaykum, Ramazon tabriklariga ismingizni yozdirmoqchimisiz? 😊'
RESTRICT_MESSAGE = 'Botimizdan foydalanish uchun kanalimizga a\'zo bo\'lib oling 🙈'

# initialize bot
utils = Initializer(API_TOKEN, CHANNEL)
bot, dp = utils.run_bot()

# call database models
from happyRamazonbot.models import BotUser as Model



@dp.callback_query_handler(lambda query: True if query.data.split('_')[0] == 'gen' else False)
async def generate(query: types.CallbackQuery):
    current_number = int(query.data.split('_')[1])
    fonts_folder = 'happyRamazonbot/fonts/'
    header = Header(text='',
                font=Font(fonts_folder + 'ArchitectsDaughter-Regular.ttf', 20),
                text_width=50,
                align='center',
                color='#000100',
                )

    content = Content(header=header)

    img = Image(content,
                fullpath=f'happyRamazonbot/pictures/{current_number}.jpg',
                width=600,
                height=314
                )
    img.draw_on_image(f'happyRamazonbot/pictures/{current_number}.jpg')
    await bot.send_photo(query.message.chat.id,
    open(f'happyRamazonbot/pictures/{current_number}.jpg', 'rb'))
    return

@dp.callback_query_handler(lambda query: True if query.data.split('_')[0] == 'choose' else False)
async def start_choosing(query: types.CallbackQuery):
    current_number = int(query.data.split('_')[1])
    inline_key = types.InlineKeyboardMarkup()
    inline_key.row(
        *(types.InlineKeyboardButton('⏪',
                                        callback_data=f'navi_{current_number-1}'),
            types.InlineKeyboardButton('⏩',
                                        callback_data=f'navi_{current_number+1}'),
            )
    )
    inline_key.row(
        types.InlineKeyboardButton('Ism qo\'shish',
                                    callback_data=f'gen_{current_number}'),
    )
    
    await bot.send_photo(query.message.chat.id, 
    open(f'happyRamazonbot/pictures/{current_number}.jpg', 'rb'),
    reply_markup=inline_key)


@dp.callback_query_handler(lambda query: True if query.data.split('_')[0] == 'navi' else False)
async def navigation_based(query: types.CallbackQuery):
    current_number = int(query.data.split('_')[1])
    inline_key = types.InlineKeyboardMarkup()

    max_number = len(os.listdir('happyRamazonbot/pictures'))
    if current_number < max_number:
        inline_key.row(
            *(types.InlineKeyboardButton('⏪',
                                         callback_data=f'navi_{current_number-1}'),
              types.InlineKeyboardButton('⏩',
                                         callback_data=f'navi_{current_number+1}'),
              )
        )
        inline_key.row(
        types.InlineKeyboardButton('Ism qo\'shish',
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
        types.InlineKeyboardButton('Ism qo\'shish',
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
        types.InlineKeyboardButton('Ism qo\'shish',
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
