from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

#_________MAIN MENU MARKUPS__________ 

mainMenuMarkup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                               [KeyboardButton(text='Корзина')]], 
                                               resize_keyboard=True,)
#____________________________________

#______ADMIN MAIN MENU ______________
mainMenuMarkupAdmin = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Добавить товар')],
                                               [KeyboardButton(text='Каталог')],
                                               [KeyboardButton(text='Заказы')]], 
                                               resize_keyboard=True,)


#______BACK TO CATALOG _____

async def inline_fresh_fish_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_to_catalog'))

    return keyboard.adjust(1).as_markup()

#___________________________

#______SHOPCART OR CATALOG _____
async def inline_after_add():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='В корзину', callback_data='to_shopcart_from_message'),
                 InlineKeyboardButton(text='В каталог', callback_data='back_to_catalog_from_message'))

    return keyboard.adjust(2).as_markup()



#______ADD TO SHOP CAR _____ подумать что сделать с кнопкой 
async def inline_add_to_shop():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Добавить в корзину', callback_data='add_to_shop_car'),
                 InlineKeyboardButton(text='Назад', callback_data='back_to_catalog'))

    return keyboard.adjust(2).as_markup()

#__________________________

async def inline_fresh_fish(data):
    keyboard = InlineKeyboardBuilder()
    for dicts in data:
        keyboard.add(InlineKeyboardButton(text=f'{dicts["name"]} - {dicts["price"]}р/кг',
                                          callback_data='fresh_'+str(dicts['id'])))

    return keyboard.adjust(1).as_markup()

#______УДАЛИТЬ ТОВАР ИЗ КОРЗИНЫ 
async def inline_shopcart(data):
    keyboard = InlineKeyboardBuilder()
    args = ()
    for dicts in data:
        keyboard.add(InlineKeyboardButton(text=f'{dicts["name"]} {dicts["kilograms"]}кг - удалить',
                                          callback_data='shopcartf_'+str(dicts['id'])))
        args = args + (1,)
    keyboard.add(InlineKeyboardButton(text=f'Оплата онлайн',
                                          callback_data='pay_online'))
    keyboard.add(InlineKeyboardButton(text=f'Оплата в магазине',
                                          callback_data='pay_shop'))
    
    return keyboard.adjust(*args, 2).as_markup()

#____ВЫБОР ЗАКАЗОВ ДЛЯ АДМИНКИ 
async def inline_orders_admin():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Активные заказы', callback_data='active_orders'),
                 InlineKeyboardButton(text='Заказы в сборке', callback_data='raise_orders'),
                 InlineKeyboardButton(text='Готовы к выдаче', callback_data='ready_orders'))

    return keyboard.adjust(1).as_markup()


###____АКТИВНЫЕ ЗАКАЗЫ ДЛЯ АДМИНКИ 
async def inline_active_orders_admin(data):
    keyboard = InlineKeyboardBuilder()

    for dicts in data:
        keyboard.add(InlineKeyboardButton(text=f'Заказ №{str(dicts["id"])}',
                                          callback_data='activeorder_'+str(dicts['id'])))
    
    keyboard.add(InlineKeyboardButton(text=f'Назад',
                                          callback_data="back_admin"))

    return keyboard.adjust(1).as_markup()

###____В СБОРКЕ ЗАКАЗЫ ДЛЯ АДМИНКИ 
async def inline_raise_orders_admin(data):
    keyboard = InlineKeyboardBuilder()

    for dicts in data:
        keyboard.add(InlineKeyboardButton(text=f'Заказ №{str(dicts["id"])}',
                                          callback_data='raiseorder_'+str(dicts['id'])))
    
    keyboard.add(InlineKeyboardButton(text=f'Назад',
                                          callback_data="back_admin"))

    return keyboard.adjust(1).as_markup()

###____ГОТОВЫЕ К ВЫДАЧЕ ЗАКАЗЫ ДЛЯ АДМИНКИ 
async def inline_ready_orders_admin(data):
    keyboard = InlineKeyboardBuilder()

    for dicts in data:
        keyboard.add(InlineKeyboardButton(text=f'Заказ №{str(dicts["id"])}',
                                          callback_data='readyorder_'+str(dicts['id'])))
    
    keyboard.add(InlineKeyboardButton(text=f'Назад',
                                          callback_data="back_admin"))

    return keyboard.adjust(1).as_markup()

#____ЗАКРЫТЬ ЧАТ ____ 
async def inline_close_chat():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Завершить чат', callback_data='close_chat'))

    return keyboard.adjust(1).as_markup()


#____UPDATE_OREDER_STATUS___
async def update_status():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Передать в сборку', callback_data='to_raise'),
                 InlineKeyboardButton(text='Закрыть заказ', callback_data='close_order'))

    return keyboard.adjust(2).as_markup()

async def update_status_raise():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Заказ собран', callback_data='to_ready'),
                 )

    return keyboard.adjust(1).as_markup()


async def update_status_ready():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Заказ вручен', callback_data='to_done'),
                 InlineKeyboardButton(text='Заказ не забрали', callback_data='close_order')
                 )

    return keyboard.adjust(1).as_markup()

async def edit_catalog_admin():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Название', callback_data='edit_name'),
                 InlineKeyboardButton(text='Цена', callback_data='edit_price'),
                 InlineKeyboardButton(text='Изображение', callback_data='edit_image'),
                 InlineKeyboardButton(text='Удалить товар', callback_data='delete_order'),
                 InlineKeyboardButton(text='Назад', callback_data='back_to_catalog')
                 )

    return keyboard.adjust(1).as_markup()

