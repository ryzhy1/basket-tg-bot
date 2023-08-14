from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
inline_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
inline_builder_two: InlineKeyboardBuilder = InlineKeyboardBuilder()

# main = builder.row(KeyboardButton(text='Admin'))

choose_fac = inline_builder.row(
                 InlineKeyboardButton(text='ТИНТ', callback_data='ТИНТ'),
                 InlineKeyboardButton(text='ФТМИ', callback_data='ФТМИ'),
                 InlineKeyboardButton(text='ФТМФ', callback_data='ФТМФ'),
                 InlineKeyboardButton(text='КТУ', callback_data='КТУ'),
                 InlineKeyboardButton(text='НОЖ', callback_data='НОЖ'),
width=1)

teams = inline_builder_two.row(
                    InlineKeyboardButton(text='Да', callback_data='Да'),
                    InlineKeyboardButton(text='Нет', callback_data='Нет'))