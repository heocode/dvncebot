from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Билеты', callback_data='tickets'),
     InlineKeyboardButton(text='Тех.поддержка', callback_data='support')],
     [InlineKeyboardButton(text='Сотрудничество', callback_data='collaboration'),
      InlineKeyboardButton(text='О нас', callback_data='aboutUs')]
], resize_keyboard=True,
   input_field_placeholder='Выберите пункт')

tickets = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Где купить билет?', callback_data='wherePay'),
     InlineKeyboardButton(text='Как пользоваться билетом?', callback_data='howUse')],
    [InlineKeyboardButton(text='Информация о билетах', callback_data='infoTickets'),
     InlineKeyboardButton(text='Как вернуть билет?', callback_data='return')],
    [InlineKeyboardButton(text='Главное меню', callback_data='home')]
])

returnProccess = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='tickets'),
     InlineKeyboardButton(text='Главное меню', callback_data='home')]
])

techSupport = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Задать вопрос', callback_data='tech')],
    [InlineKeyboardButton(text='Главное меню', callback_data='home')]
])

askSupportment = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='support'),
     InlineKeyboardButton(text='Главное меню', callback_data='home')]
])

collaboration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Есть своя идея!', callback_data='idea'),
     InlineKeyboardButton(text='Хочу работать с вами!', callback_data='work')],
    [InlineKeyboardButton(text='Главное меню', callback_data='home')]
])

ticketsBack = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='tickets'),
     InlineKeyboardButton(text='Главное меню', callback_data='home')]
])

supportBack = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='support'),
     InlineKeyboardButton(text='Главное меню', callback_data='home')]
])

collaborationBack = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='collaboration'),
     InlineKeyboardButton(text='Главное меню', callback_data='home')]
])

menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Вернуться на главную', callback_data='home')]])