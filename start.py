# -*- coding: utf-8 -*-
#
#  PcControl - startup script.
#  Created by LulzLoL231 at 04/11/20
#
from aiogram.utils.executor import start_polling

from runtime import bot
import cmds


if __name__ == '__main__':
    start_polling(bot)
