import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

API_TOKEN = '6904735054:AAFQLWaQmB4kUozz2dT7_yW1QAsY-nugG0k'  # Замените на ваш токен бота

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Хранилище имен игроков
players = []

# Команда /start — приветствие и инструкция
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот для генерации футбольных команд.\n\n"
        "Просто отправьте имена игроков в чат, и они будут добавлены автоматически.\n"
        "Когда все игроки будут добавлены, введите команду /generate для создания команд.\n"
        "Используйте команду /clear, чтобы очистить список игроков."
    )

# Добавление игрока при любом текстовом сообщении, кроме команд
@dp.message(lambda message: not message.text.startswith('/'))
async def add_player_auto(message: Message):
    global players
    name = message.text.strip()
    
    if len(players) >= 20:
        await message.answer("Максимум 20 игроков. Сначала сгенерируйте команды, чтобы начать заново.")
    else:
        players.append(name)
        await message.answer(f"Игрок {name} добавлен! Всего игроков: {len(players)}.")

# Команда /generate — генерация случайных команд
@dp.message(Command("generate"))
async def generate_teams(message: Message):
    global players
    if len(players) < 2:
        await message.answer("Недостаточно игроков для создания команд. Добавьте хотя бы 2 игрока.")
    else:
        # Перемешиваем список игроков и делим его пополам
        random.shuffle(players)
        mid = len(players) // 2
        team1 = players[:mid]
        team2 = players[mid:]
        
        # Формируем ответ с командами
        response = "Команды сгенерированы!\n\n"
        response += "⚽ *Команда 1:* \n" + "\n".join(team1) + "\n\n"
        response += "⚽ *Команда 2:* \n" + "\n".join(team2)

        await message.answer(response, parse_mode="Markdown")
        
        # Очистка списка игроков для новой игры
        players = []

# Команда /clear — очистка списка игроков
@dp.message(Command("clear"))
async def clear_players(message: Message):
    global players
    players = []
    await message.answer("Список игроков очищен. Начните добавлять игроков, отправляя их имена в чат.")

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
