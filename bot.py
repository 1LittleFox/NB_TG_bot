import asyncio
from aiogram import Bot, Dispatcher
from hendlers import base_commands, buttons
from token_nbb import BOT_TOKEN


async def main():

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(base_commands.router),
    dp.include_router(buttons.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

