import telebot
from typing import Optional, List
import logging
import time
from src import BOT_TOKEN


class T_bot(telebot.TeleBot):
    def infinity_polling(self, timeout: Optional[int] = 20, skip_pending: Optional[bool] = False,
                         long_polling_timeout: Optional[int] = 20,
                         logger_level: Optional[int] = logging.ERROR, allowed_updates: Optional[List[str]] = None,
                         *args, **kwargs):

        while True:
            try:
                self.polling(non_stop=True, timeout=timeout, long_polling_timeout=long_polling_timeout,
                             logger_level=logger_level, allowed_updates=allowed_updates, *args, **kwargs)
            except Exception as e:
                logging.exception("Infinity polling exception: %s", e)
                time.sleep(3)
                continue


bot = T_bot(BOT_TOKEN)
