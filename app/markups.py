from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

#_________USER MAIN MENU MARKUPS__________ 

mainMenuMarkupUser = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📝 Подать заявку')],
                                               [KeyboardButton(text='📊 Мои заявки')],
                                               [KeyboardButton(text='ℹ️ Справка')],
                                               [KeyboardButton(text='📞 Контакты')]], 
                                               resize_keyboard=True,)
#____________________________________

#______ADMINISTRATOR MAIN MENU ______________
mainMenuMarkupAdministrator = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📊 Статистика')],
                                               [KeyboardButton(text='📝 Заявки')],
                                               [KeyboardButton(text='👥 Пользователи')],
                                               [KeyboardButton(text='⚙️ Настройки')]], 
                                               resize_keyboard=True,)
#____________________________________

#______MODERATOR MAIN MENU ______________
mainMenuMarkupModerator = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📊 Статистика')],
                                               [KeyboardButton(text='📝 Активные заявки')],
                                               [KeyboardButton(text='✅ Заявки в работе')],
                                               [KeyboardButton(text='❗️ Жалобы')]], 
                                               resize_keyboard=True,)
#____________________________________

#______EXECUTOR MAIN MENU ______________
mainMenuMarkupExecutor = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📊 Статистика')],
                                               [KeyboardButton(text='📝 Активные заявки')],
                                               [KeyboardButton(text='📅 График работ ')],
                                               [KeyboardButton(text='📸 Отправить отчет')],
                                               [KeyboardButton(text='📞 Связь с модератором ')]], 
                                               resize_keyboard=True,)
#____________________________________

#______REGISTRATION MENU ______________
RegistrationMenuYesNo = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да')],
                                               [KeyboardButton(text='Нет')]],
                                               resize_keyboard=True,)
#____________________________________