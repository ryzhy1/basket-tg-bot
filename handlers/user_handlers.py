from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards import keyboards as kb
from database import database as db
from lexicon.lexicon import LEXICON_RU
from config_data.config import Config, load_config

router: Router = Router()

config: Config = load_config()
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

class User(StatesGroup):
    name = State()
    photo = State()
    faculty = State()
    faculty_choose = State()
    teams = State()
    isu = State()
    contact = State()

@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext) -> None:
    await state.set_state(User.name)
    await message.answer(text=LEXICON_RU['/start'])
    await message.delete()

@router.message(User.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(User.photo)
    await message.answer(text=LEXICON_RU['photo'], parse_mode='HTML')

@router.message(User.photo)
async def process_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.text)
    await state.set_state(User.faculty)
    await message.answer(text=LEXICON_RU['fac'], reply_markup=kb.choose_fac.as_markup(resize_keyboard=True))

@router.callback_query(User.faculty)
async def process_fac(callback: CallbackQuery, state: FSMContext):
    await state.update_data(faculty=callback.data)
    await state.set_state(User.faculty_choose)
    await callback.message.edit_text(text=LEXICON_RU['fac_choose'], reply_markup=kb.choose_fac.as_markup(resize_keyboard=True), parse_mode='HTML')

@router.callback_query(User.faculty_choose)
async def process_team(callback: CallbackQuery, state: FSMContext):
    await state.update_data(faculty_choose=callback.data)
    await state.set_state(User.teams)
    await callback.message.edit_text(text=LEXICON_RU['teams'], reply_markup=kb.teams.as_markup(resize_keyboard=True), parse_mode='HTML')

@router.callback_query(User.teams)
async def process_isu(callback: CallbackQuery, state: FSMContext):
    await state.update_data(teams=callback.data)
    await state.set_state(User.isu)
    await callback.message.edit_text(text=LEXICON_RU['isu'], parse_mode='HTML', reply_markup=None)

@router.message(User.isu)
async def process_contact(message: Message, state: FSMContext):
    await state.update_data(isu=message.text)
    await state.set_state(User.contact)
    await message.answer(text=LEXICON_RU['contact'], parse_mode='HTML')

@router.message(User.contact)
async def process_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    await message.answer(text=f'ФИО: {data["name"]}\nФото: {data["photo"]}\nТвой факультет: {data["faculty"]}\nВыбранный факультет: {data["faculty_choose"]}\nКоманда: {data["teams"]}\nИСУ: {data["isu"]}\nКонтакт: {data["contact"]}', parse_mode='HTML')
    await message.answer(text=LEXICON_RU['check'], parse_mode='HTML', reply_markup=kb.teams.as_markup(resize_keyboard=True))
    # await db.add_user(state)
    # await message.answer(text=LEXICON_RU['success'])
    # await state.clear()

@router.callback_query()
async def check_message(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Да':
        await db.add_user(state)
        await callback.message.answer(text=LEXICON_RU['success'])
        await state.clear()
    elif callback.data == 'Нет':
        await callback.message.answer(text=LEXICON_RU['cancel'])
        await state.set_state(User.name)