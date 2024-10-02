from aiogram import Bot, Dispatcher
from src import BOT_TOKEN
from src.database import sessionmanager
from src.database import TelegramRepository, TelegramProfile

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def calculate_points(message):
    async with sessionmanager.session() as session:
        if message.chat.type == "private":
            return
        telegram_repository = TelegramRepository(session)
        tg_profile = await telegram_repository.get_by_username(message.from_user.username)
        if not tg_profile:
            return
        await telegram_repository.add_points(tg_profile, int(len(message.text) * 0.1))
        await session.commit()


@dp.message()
async def send_default(message):
    await calculate_points(message)


async def main():
    await dp.start_polling(bot)