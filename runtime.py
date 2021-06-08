# -*- coding: utf-8 -*-
#
#  PcControl - runtime funcs.
#  Created by LulzLoL231 at 04/11/20
#
from asyncio import get_event_loop

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from brain_api import Brain


cmds = [
    BotCommand('start', 'Authorization'),
    BotCommand('help', 'Help page'),
    BotCommand('version', 'Show version')
]
loop = get_event_loop()
bot = Dispatcher(Bot(config.TOKEN, loop, parse_mode='HTML'), loop, storage=MemoryStorage())
brain = Brain()
loop.run_until_complete(bot.bot.set_my_commands(cmds))
__version__ = '2.2.0'
