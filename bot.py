import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import user_handlers
from config_data.config import Config, load_config

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(level=logging.INFO, format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
                                                   u'[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    config: Config = load_config()

    bot = Bot(config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())