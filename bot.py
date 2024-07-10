import datetime
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InputFile, Message
from aiogram.utils import executor
from aiogram.utils.executor import start_polling
from aiogram.dispatcher.filters import Text
import datetime

API_TOKEN="api_token here"

logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

photo = InputFile("images/img1.jpg")


credentials_file = 'token.json'
# Определяем область доступа
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# # Загружаем учетные данные
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

# key=AIzaSyAqcbSPkS0NwEDsn0YIukAdooWHS8ucANI
# # Авторизуемся и создаем клиент
client = gspread.authorize(credentials)

# # Создаем новую таблицу
spreadsheet = client.create('tgBot_sheets')

spreadsheet.share('sonochiwaxd@gmail.com', perm_type='user', role='writer')

# Открываем таблицу по названию
spreadsheet = client.open('tgBot_sheets')

print('https://docs.google.com/spreadsheets/d/' + spreadsheet.id)

# Открываем первый лист
worksheet = spreadsheet.get_worksheet(0)

# Добавляем новый лист
spreadsheet.add_worksheet(title='first sheet', rows=100, cols=20)

worksheet.update_acell('A2', 'helloworld123')

value = worksheet.acell('A2').value

class Form(StatesGroup):
    date = State()

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Кнопка 1", "Кнопка 2", "Кнопка 3", "Кнопка 4"]
    keyboard.add(*buttons)
    await message.answer("Выбери кнопку или введи дату в формате 'дд.мм.гггг'", reply_markup=keyboard)


@dp.message_handler(Text(equals="Кнопка 1"))
async def with_puree(message: types.Message):
    await message.answer(
        "Ленина 1, https://yandex.ru/maps/66/omsk/house/ulitsa_lenina_1/Y0oYdQFpS0UHQFtufXV5eHpnYg==/?indoorLevel=1&ll=73.369200%2C54.989647&z=17.15")


@dp.message_handler(Text(equals="Кнопка 2"))
async def with_puree(message: types.Message):
    await message.answer(
        "Ссылка на оплату: https://yoomoney.ru/fundraise/13RTK3HFUOO.240708")
    


@dp.message_handler(Text(equals="Кнопка 3"))
async def with_puree(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption="Картинка")
    


@dp.message_handler(Text(equals="Кнопка 4"))
async def with_puree(message: types.Message):
    await message.answer(value)
    
    
@dp.message_handler()
async def process_date(message: types.Message):
    try:
        date_str = message.text
        date_format = '%d.%m.%y'
        datetime.datetime.strptime(date_str, date_format)
        spreadsheet = client.open('tgBot_sheets')
        #next_row = len(spreadsheet.col_values(2)) + 1
        worksheet.update_acell('B1', date_str)
        await message.answer("Дата верна")
    except ValueError:
        await message.answer("Дата неверна")
    

# Запуск бота
if __name__ == '__main__':
    start_polling(dp, skip_updates=True)
