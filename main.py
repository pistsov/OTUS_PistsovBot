import peewee
from aiogram import Bot, Dispatcher, executor, types
import get_rates_async
from secret import TOKEN

# Подключение к базе данных
db = peewee.SqliteDatabase('bot_database.db')

# Определение модели данных
class User(peewee.Model):
    user_id = peewee.IntegerField(unique=True)
    username = peewee.CharField(null=True)
    full_name = peewee.CharField(null=True)

    class Meta:
        database = db

# Создание таблицы в базе данных
db.connect()
db.create_tables([User])

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('/eur')
    btn2 = types.KeyboardButton('/usd')
    btn3 = types.KeyboardButton('/❤️')
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    await message.reply("Привет! Я телеграм-бот для работы с перечнем пользователей.\n"
                        "Но умею и кое-что ещё - см. кнопки.\n"
                        "Команды для работы с пользователями:\n"
                        "/add_me - добавляет текущего пользователя\n"
                        "/list - выводит список всех пользователей\n"
                        "/del_me - удаляет текущего пользователя\n", reply_markup=markup)


# Обработчик команд по кнопкам
@dp.message_handler(commands=['eur', 'usd', '❤️'])
async def reply_message(message):
    print(message.from_user.username, message.text)
    match message.text:
        case '/eur':
            eur = await get_rates_async.fetch_eur()
            eur_text = '1 евро = ' + str(eur) + ' рублей по курсу ЦБ РФ на сегодня'
            await message.reply(eur_text)
        case '/usd':
            usd = await get_rates_async.fetch_usd()
            usd_text = '1 доллар = ' + str(usd) + ' рублей по курсу ЦБ РФ на сегодня'
            await message.reply(usd_text)
        case '/❤️':
            await message.reply('@' + message.from_user.username + ', ты просто прелесть!😘💋')



# Обработчик команды /add
@dp.message_handler(commands=['add_me'])
async def process_add_me_command(message: types.Message):
    print(message.from_user.username, message.text)
    # Добавление нового пользователя в базу данных
    user = User.get_or_none(user_id=message.from_user.id)
    if user:
        await message.reply("Такой пользователь уже есть в базе данных.")
    else:
        user = User.create(user_id=message.from_user.id, username=message.from_user.username, full_name=message.from_user.full_name)
        await message.reply("Пользователь добавлен в базу данных.")


# Обработчик команды /get
@dp.message_handler(commands=['list'])
async def process_get_command(message: types.Message):
    print(message.from_user.username, message.text)
    # Получение списка всех пользователей из базы данных
    users = User.select()
    response = "Список пользователей:\n"
    for user in users:
        response += f"{user.full_name} (@{user.username})\n"
    await message.reply(response)

# Обработчик команды /delete
@dp.message_handler(commands=['del_me'])
async def process_del_me_command(message: types.Message):
    print(message.from_user.username, message.text)
    # Удаление пользователя из базы данных
    user = User.get_or_none(user_id=message.from_user.id)
    if user:
        user.delete_instance()
        await message.reply("Пользователь удален из базы данных.")
    else:
        await message.reply("Пользователь не найден в базе данных.")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)