# -*- coding: utf-8 -*-
#
#  PcControl - Security funcs.
#  Created by LulzLoL231 at 04/11/20
#
from typing import Optional, Union
from zlib import crc32

from aiogram import types

import config
from log import getLogger
from runtime import brain
from emojis import Emojis


async def getUser(msg: types.Message) -> Optional[Union[dict, None]]:
    '''getUser: returns user, if registered.

    Args:
        msg (types.Message): Telegram message.

    Returns:
        Optional[Union[dict, None]]: user dict or None.
    '''
    log = getLogger('PCON Security', 'getUser')
    user = await brain.getUser(msg.chat.id)
    if user:
        log.info(f'Access granted for {msg.chat.mention} ({str(msg.chat.id)})')
        return user
    else:
        log.warn(f'Access denied for {msg.chat.mention} ({str(msg.chat.id)})')
        await msg.answer(f'{Emojis.access_denied} <code>В доступе отказано!</code>')
        return None


def signData(data: str) -> str:
    '''[REMOVED]
    '''
    return '[REMOVED]'


def verifySign(signed_data: str) -> bool:
    '''[REMOVED]
    '''
    return False


def check_cmd(msg: types.Message, cmd: str) -> bool:
    '''Check if text is cmd alias.

    Args:
        msg (types.Message): telegram message.
        cmd (str): command name.

    Returns:
        bool: True or False.
    '''
    log = getLogger('PCON Security', 'check_cmd')
    log.info(f'Called with args: ("{msg.text}", {cmd})')
    cmds = {
        'help': ('помощь', 'хелп', 'хэлп'),
        'hubs': ('хабы'),
        'netstatus': ('статус сети', 'сеть'),
        'devices': ('устройства'),
        'version': ('ver', 'version', 'вер', 'версия'),
        'users': ('usr', 'users', 'пользователи', 'юзеры')
    }
    res = msg.text.lower() in cmds[cmd]
    if res:
        log.info(f'"{msg.text}" is "{cmd}" command alias.')
        return res
    else:
        log.warning(f'"{msg.text}" is not a "{cmd}" command alias.')
        return res
