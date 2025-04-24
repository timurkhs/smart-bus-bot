from aiogram import F, Router, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, PreCheckoutQuery
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.context import FSMContext

import app.markups as nav
from app.db import Database
import config as cf
from programmConsts.templateText import YesNoAnswer, RegistrationText

router = Router()
db = Database(cf.DATA_BASE_PATH)

class Registration(StatesGroup):
    user_name = State()
    notification = State()

#Регистрационное сообщение 
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if (not db.user_exist(message.from_user.id)):
        await state.set_state(Registration.user_name)
        await message.answer(RegistrationText.HELLO_MESSAGE.value)


@router.message(Registration.user_name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.notification)
    await message.answer(RegistrationText.RECEIVE_NOTIFICATIONS.value) #да нет клавиатура 

@router.message(Registration.notification)
async def add_name(message: Message, state: FSMContext):
    if (message.text).lower() in [YesNoAnswer.YES.value, YesNoAnswer.NO.value]:
        await state.update_data(notification = 1 if message.text.lower() == YesNoAnswer.YES else 2)
        await message.answer(RegistrationText.SUCCESSFUL_REGISTRATION.value) #меню клавиатура
        data = await state.get_data()
        db.add_user(message.from_user.id, data['user_name'], data['notification'])
        await state.clear()
        

