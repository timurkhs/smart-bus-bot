from aiogram import F, Router, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, PreCheckoutQuery, ReplyKeyboardRemove
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.context import FSMContext
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from models.caseModel import Case
import re

import app.markups as nav
from app.db import Database
import config as cf
import programmConsts.templateText as textCaption
import programmConsts.murkupCaptionConst as markupCaption
import programmConsts.const as configurationConsts

router = Router()
db = Database(cf.DATA_BASE_PATH)

class Registration(StatesGroup):
    user_name = State()
    notification = State()

class SendReport(StatesGroup):
    address = State()
    location = State()
    description = State()
    photo = State()


def create_case_in_db(
        code: str, #передается всегда
        description: str, #всегда
        addres: str, #всегда
        image: str | None, #передается по желанию пользователя
        location: str | None, #передается по желанию пользователя
        telegram_id: str, #передается автоматически
        ):
    """Выполняет создание заявки в базе данных"""
    initiaor_id = db.get_user_id_by_telegram_id(telegram_id=telegram_id)
    today = datetime.now().strftime("%Y%m%d")
    name =  f"Обращение-{today}-{code}"
    db.create_case(code=code,
                   description=description,
                   addres=addres,
                   coordinator_id=None,
                   owner_id=None,
                   image=image,
                   location=location,
                   initiator_id=initiaor_id,
                   name=name)

def get_location_from_datastate(location_string):
    numbers = re.findall(r"[-+]?\d+\.\d+", location_string)
    latitude, longitude = map(float, numbers)
    location = coordinates_to_address(latitude, longitude)
    return location


def generate_case_number() -> str:
    """
    Генерирует номер обращения в формате 00000
    
    :param case_id: Номер обращения (целое число)
    :return: Строка с номером в формате 00000
    """
    case_count = db.get_case_count()
    return f"{(case_count+1):05d}"

def coordinates_to_address(latitude: float, longitude: float) -> str:
    geolocator = Nominatim(user_agent="GetLoc")
    location = geolocator.reverse((latitude, longitude), language="ru")  # language="ru" для русского адреса
    
    if location:
        return location.address
    return "Адрес не найден"

def get_menu_markup(user_id):
    roles = db.get_user_role_ids(user_id)
    if (configurationConsts.SysRoleGuids.ADMINISTRATOR.value in roles):
        return nav.mainMenuMarkupAdministrator
    elif (configurationConsts.SysRoleGuids.MODERATOR.value in roles):
        return nav.mainMenuMarkupModerator
    elif (configurationConsts.SysRoleGuids.EXECUTOR.value in roles):
        return nav.mainMenuMarkupModerator
    elif (configurationConsts.SysRoleGuids.USER.value in roles):
        return nav.mainMenuMarkupUser
    
def get_main_menu_text(user_id):
    roles = db.get_user_role_ids(user_id)
    if (configurationConsts.SysRoleGuids.ADMINISTRATOR.value in roles):
        return textCaption.MainMenuText.USER_MAIN_MENU_TEXT.value
    elif (configurationConsts.SysRoleGuids.MODERATOR.value in roles):
        return textCaption.MainMenuText.USER_MAIN_MENU_TEXT.value
    elif (configurationConsts.SysRoleGuids.EXECUTOR.value in roles):
        return textCaption.MainMenuText.USER_MAIN_MENU_TEXT.value
    elif (configurationConsts.SysRoleGuids.USER.value in roles):
        return textCaption.MainMenuText.USER_MAIN_MENU_TEXT.value

#region Регистрация пользователя

#Регистрационное сообщение 
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if (not db.user_exist(message.from_user.id)):
        await state.set_state(Registration.user_name)
        await message.answer(textCaption.RegistrationText.HELLO_MESSAGE.value)


@router.message(Registration.user_name)
async def set_notification(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await state.set_state(Registration.notification)
    await message.answer(textCaption.RegistrationText.RECEIVE_NOTIFICATIONS.value, reply_markup=nav.RegistrationMenuYesNo) #да нет клавиатура 

@router.message(Registration.notification)
async def add_name(message: Message, state: FSMContext):
    if (message.text).lower() in [markupCaption.YesNoAnswerMarkupText.YES.value, markupCaption.YesNoAnswerMarkupText.NO.value]:
        await state.update_data(notification = 1 if message.text.lower() == markupCaption.YesNoAnswerMarkupText.YES else 0)
        await message.answer(textCaption.RegistrationText.SUCCESSFUL_REGISTRATION.value, reply_markup = nav.mainMenuMarkupUser) #меню клавиатура
        data = await state.get_data()
        db.add_user(message.from_user.id, data['user_name'], data['notification'])
        await state.clear()

#endregion 
 


#region Блок действий пользователя 

#region Нажатие на кнопку - Подать заявку

# вопрос пользователю хочет ли он ее подать.
@router.message(F.text == markupCaption.MainMenuMarkupText.SEND_REPORT.value)
async def send_report(message: Message):
    await message.answer(textCaption.SendReportText.ANSWER_FOR_USER.value, 
                         reply_markup=await nav.answer_send_report())

#Пользователь действительно хочет подать заявку о неисправности.
@router.callback_query(F.data == 'set_state_send_report')
async def yes_send_report(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await state.set_state(SendReport.address)
    await callback.message.delete()
    await callback.message.answer(textCaption.SendReportText.GET_BUSSTOP_NAME,
                                  reply_markup=ReplyKeyboardRemove())


#Пользователь не хочет подать заявку о неисправности.
@router.callback_query(F.data == 'back_to_main_menu')
async def no_send_report(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(get_main_menu_text(callback.from_user.id),
                             reply_markup=get_menu_markup(callback.from_user.id))
    await state.clear()

#Запрос у пользователя названия остановки
@router.message(SendReport.address)
async def get_busstop_name(message: Message, state: FSMContext):
    await state.update_data(address = message.text)
    await state.set_state(SendReport.location)
    await message.answer(textCaption.SendReportText.GET_LOCATION, 
                            reply_markup= await nav.anser_get_location())

#Пользователь не хочет прикреплять локацию остановки.
@router.callback_query(F.data == 'next_step_report_location')
async def no_send_location(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(textCaption.SendReportText.GET_DESCRIPTION)
    await state.set_state(SendReport.description)

#Пользователь хочет прикрепить локацию.
@router.callback_query(F.data == 'get_location')
async def send_location(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(textCaption.SendReportText.SEND_LOCATION, 
                                  reply_markup=nav.RequestLocationMenu)
    
#Обработка полученной локации, запрос описания проблемы
@router.message(SendReport.location, F.content_type == 'location')
async def get_location_from_user(message: Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude
    location = f'latitude: {latitude} longitude: {longitude}'
    print(location)
    await state.update_data(location=location)
    await state.set_state(SendReport.description)
    await message.answer(textCaption.SendReportText.GET_DESCRIPTION,
                         reply_markup=ReplyKeyboardRemove())

#Обработка описания проблемы, запрос фото
@router.message(SendReport.description)
async def get_description(message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    await state.set_state(SendReport.photo)
    await message.answer(textCaption.SendReportText.GET_PHOTO, 
                            reply_markup= await nav.anser_get_photo())
    
#Пользователь не хочет прикреплять фото, регистрация заявки.
@router.callback_query(F.data == 'next_step_report_photo')
async def no_send_location(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await callback.message.delete()
    data = await state.get_data()

    location = configurationConsts.ConfigurationConst.EMPTY_LOCATION.value
    if ('location' in data):
        location = get_location_from_datastate(data['location'])
    address = data['address']
    description = data['description']
    number = generate_case_number()

    await callback.message.answer(textCaption.SendReportText.RESUME_REPORT.value.format(
                                                    number=number, 
                                                    address=address,
                                                    description=description,
                                                    location=location),
                               reply_markup=get_menu_markup(callback.from_user.id))

    create_case_in_db(number, description, address, None, location, callback.from_user.id)

#Пользователь хочет прикрепить фото.
@router.callback_query(F.data == 'get_photo')
async def send_location(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(textCaption.SendReportText.SEND_PHOTO)
    await state.set_state(SendReport.photo)

#Обработка полученного фото, регистрация заявки
@router.message(SendReport.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    await state.update_data(photo=file_id)
    data = await state.get_data()
    location = configurationConsts.ConfigurationConst.EMPTY_LOCATION.value
    if ('location' in data):
        location = get_location_from_datastate(data['location'])
    address = data['address']
    description = data['description']
    number = generate_case_number()

    await message.answer_photo(file_id, caption=textCaption.SendReportText.RESUME_REPORT.value.format(
                                                    number=number, 
                                                    address=address,
                                                    description=description,
                                                    location=location),
                               parse_mode="Markdown",
                               reply_markup=get_menu_markup(message.from_user.id))
    
    create_case_in_db(number, description, address, file_id, location, message.from_user.id)
    #Отправить сообщение всем менеджерам о поступлении новой заявки.
    await state.clear()

#endregion


#region Нажатие на кнопку - Мои заявки 
@router.message(F.text == markupCaption.MainMenuMarkupText.MY_REPORTS.value)
async def show_cases(message: Message):
    # Получаем ID пользователя
    initiator_id = db.get_user_id_by_telegram_id(message.from_user.id)
    if not initiator_id:
        await message.answer("Ошибка: пользователь не найден")
        return

    # Получаем все заявки пользователя
    cases = db.get_cases_by_initiator(initiator_id=initiator_id)
    
    if not cases:
        await message.answer("📭 У вас пока нет заявок")
        return
    
    # Формируем текст с количеством заявок
    total_cases = len(cases)
    pages = (total_cases + 4) // 5  # Вычисляем общее количество страниц
    
    await message.answer(
        f"📋 Ваши заявки (всего {total_cases}, страница 1/{pages}):",
        reply_markup=await nav.user_cases_markups(cases, page=0)
    )

@router.callback_query(F.data.startswith("cases_page_"))
async def handle_pagination(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    initiator_id = db.get_user_id_by_telegram_id(callback.from_user.id)
    cases = db.get_cases_by_initiator(initiator_id=initiator_id)
    
    total_pages = (len(cases) + 4) // 5  # 5 заявок на страницу
    
    if callback.message.photo: 
        await callback.message.delete()
        # Отправляем новое сообщение с обновленными данными
        await callback.message.answer(
            f"📋 Ваши заявки (всего {len(cases)}, страница {page+1}/{total_pages}):",
            reply_markup=await nav.user_cases_markups(cases, page)
        )
    else:
        await callback.message.edit_text(
            f"📋 Ваши заявки (всего {len(cases)}, страница {page+1}/{total_pages}):",
            reply_markup=await nav.user_cases_markups(cases, page))
    
    await callback.answer()


@router.callback_query(F.data == "close_cases_list")
async def close_list(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Список закрыт")


@router.callback_query(F.data.startswith("case_detail_"))
async def show_case_detail(callback: CallbackQuery):
    # Извлекаем ID заявки
    case_id = callback.data.split("_")[-1]
    case = db.get_case_by_id(case_id)
    
    if not case:
        await callback.answer("Заявка не найдена", show_alert=True)
        return

    # Получаем номер страницы из предыдущего сообщения
    page = 0
    if "страница" in callback.message.text:
        page_match = re.search(r"страница (\d+)", callback.message.text)
        if page_match:
            page = int(page_match.group(1)) - 1

    # Формируем текст сообщения
    text = (
        f"📌 <b>{case.name}</b>\n\n"
        f"📍 <b>Адрес:</b> {case.addres}\n"
        f"🔄 <b>Статус:</b> {case.status_name}\n"
        f"📝 <b>Описание:</b>\n{case.description}\n"
    )
    
    # Добавляем локацию, если есть
    if case.location:
        text += f"\n🗺️ <b>Локация:</b> {case.location}"

    # Если есть фото
    if case.image:
        try:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=case.image,
                caption=text,
                parse_mode="HTML",
                reply_markup=await nav.inline_case_detail_markup(page=page)
            )
            
            # Отправляем локацию отдельно, если есть
            if case.location:
                lat, lon = map(float, case.location.split(','))
                await callback.message.answer_location(
                    latitude=lat,
                    longitude=lon
                )
            
            await callback.answer()
            return
        except Exception as e:
            print(f"Ошибка отправки фото: {e}")
            text += "\n⚠️ Не удалось загрузить вложение"

    # Если фото нет - отправляем текст с клавиатурой
    await callback.message.edit_text(
        text=text,
        parse_mode="HTML",
        reply_markup=await nav.inline_case_detail_markup(page=page)
    )
    await callback.answer()

#endregion

#region Нажатие на кнопку - Справка или Контакты

@router.message(F.text == markupCaption.MainMenuMarkupText.HELP.value)
async def show_cases(message: Message):
    await message.answer(textCaption.MainMenuText.HELP_TEXT.value,
                         reply_markup=get_menu_markup(message.from_user.id))


@router.message(F.text == markupCaption.MainMenuMarkupText.CONTACTS.value)
async def show_cases(message: Message):
    await message.answer(textCaption.MainMenuText.CONTACT_TEXT.value,
                         reply_markup=get_menu_markup(message.from_user.id))

#endregion

#endregion