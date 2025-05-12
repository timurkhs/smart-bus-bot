from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import programmConsts.murkupCaptionConst as markupCaption

#_________USER MAIN MENU MARKUPS__________ 

mainMenuMarkupUser = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=markupCaption.MainMenuMarkupText.SEND_REPORT.value)],
                                               [KeyboardButton(text=markupCaption.MainMenuMarkupText.MY_REPORTS.value)],
                                               [KeyboardButton(text=markupCaption.MainMenuMarkupText.HELP.value)],
                                               [KeyboardButton(text=markupCaption.MainMenuMarkupText.CONTACTS.value)]], 
                                               resize_keyboard=True,)
#____________________________________

#______ADMINISTRATOR MAIN MENU ______________
mainMenuMarkupAdministrator = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=markupCaption.AdministratorMenuMarkupText.STATISTICS.value)],
                                               [KeyboardButton(text=markupCaption.AdministratorMenuMarkupText.REPORTS.value)],
                                               [KeyboardButton(text=markupCaption.AdministratorMenuMarkupText.USERS.value)],
                                               [KeyboardButton(text=markupCaption.AdministratorMenuMarkupText.SETTINGS.value)]], 
                                               resize_keyboard=True,)
#____________________________________

#______MODERATOR MAIN MENU ______________
mainMenuMarkupModerator = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=markupCaption.ModeratorMenuMarkupsText.STATISTICS.value)],
                                               [KeyboardButton(text=markupCaption.ModeratorMenuMarkupsText.ACTIVE_REPORTS.value)],
                                               [KeyboardButton(text=markupCaption.ModeratorMenuMarkupsText.IN_PROGRESS_REPORTS.value)],
                                               [KeyboardButton(text=markupCaption.ModeratorMenuMarkupsText.COMPLAINT.value)]], 
                                               resize_keyboard=True,)
#____________________________________

#______EXECUTOR MAIN MENU ______________
mainMenuMarkupExecutor = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=markupCaption.ExecutorMenuMarkupsText.STATISTICS.value)],
                                               [KeyboardButton(text=markupCaption.ExecutorMenuMarkupsText.ACTIVE_REPORTS.value)],
                                               [KeyboardButton(text=markupCaption.ExecutorMenuMarkupsText.WORK_TIME.value)],
                                               [KeyboardButton(text=markupCaption.ExecutorMenuMarkupsText.MODERATOR_CALL.value,)]], 
                                               resize_keyboard=True,)
#____________________________________

#______REGISTRATION MENU ______________
RegistrationMenuYesNo = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=markupCaption.YesNoAnswerMarkupText.YES.value)],
                                               [KeyboardButton(text=markupCaption.YesNoAnswerMarkupText.NO.value)]],
                                               resize_keyboard=True,)
#____________________________________

RequestLocationMenu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=markupCaption.LocationMarkupText.GET_LOCATION.value, request_location=True)]],
                                               resize_keyboard=True,)

#Инлайн клавиатура на вопрос пользователя хочет ли он подать заявку
async def answer_send_report():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=markupCaption.YesNoAnswerMarkupText.YES, callback_data='set_state_send_report'),
                 InlineKeyboardButton(text=markupCaption.YesNoAnswerMarkupText.NO, callback_data='back_to_main_menu'))

    return keyboard.adjust(2).as_markup()

#Инлайн клавиатура хочет ли пользователь прикрепить локацию
async def anser_get_location():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=markupCaption.YesNoAnswerMarkupText.YES, callback_data='get_location'),
                 InlineKeyboardButton(text=markupCaption.YesNoAnswerMarkupText.NO, callback_data='next_step_report_location'))

    return keyboard.adjust(2).as_markup()

#Инлайн клавиатура хочет ли пользователь прикрепить фото к заявке
async def anser_get_photo():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=markupCaption.YesNoAnswerMarkupText.YES, callback_data='get_photo'),
                 InlineKeyboardButton(text=markupCaption.YesNoAnswerMarkupText.NO, callback_data='next_step_report_photo'))

    return keyboard.adjust(2).as_markup()