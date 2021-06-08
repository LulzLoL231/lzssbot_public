# -*- coding: utf-8 -*-
#
#  PcControl - Utilites.
#  Created by LulzLoL231 at 04/11/20
#
import datetime
from typing import Tuple

from aiogram import types

import security as sec
from emojis import Emojis


def getDelLogKey() -> types.InlineKeyboardMarkup:
    '''Returns inline key with deleteLogMsg data.

    Returns:
        types.InlineKeyboardMarkup: inline keyboard.
    '''
    return types.InlineKeyboardMarkup(
        resize_keyboard=True
    ).add(types.InlineKeyboardButton(
        f'{Emojis.cancel} Удалить.',
        callback_data='deleteLogMsg'
    ))


def getDateName(date: datetime.datetime) -> str:
    '''getDateName: returns date name from datetime object.

    Args:
        date (datetime): datetime object.

    Returns:
        str: date name.
    '''
    return date.strftime('%d %b %Y (%A)')


def getEmojiNumByInt(number: int) -> str:
    '''Returns emoji number by integer.

    Args:
        number (int): number.

    Returns:
        str: number emoji.
    '''
    if number == 0:
        return Emojis.zero
    elif number == 1:
        return Emojis.one
    elif number == 2:
        return Emojis.two
    elif number == 3:
        return Emojis.three
    elif number == 4:
        return Emojis.four
    elif number == 5:
        return Emojis.five
    elif number == 6:
        return Emojis.six
    elif number == 7:
        return Emojis.seven
    elif number == 8:
        return Emojis.eight
    elif number == 9:
        return Emojis.nine
    else:
        return ''


def getStatusEmojiByStatus(status: str) -> str:
    '''Returns emoji for status by provided status.

    Args:
        status (str): device status.

    Returns:
        str: emoji.
    '''
    if status == 'Online':
        return Emojis.online
    elif status == 'Offline':
        return Emojis.offline
    else:
        return Emojis.warning


def parseUsers(array: list) -> Tuple[str, types.InlineKeyboardMarkup]:
    '''Returns message content with all users from array.

    Args:
        array (list): users array.

    Returns:
        tuple: message content and types.InlineKeyboardMarkup.
    '''
    cnt = '      <code>Список пользователей:</code>\n'
    usr_temp = '{num}: <b>{level}</b> <a href="tg://user?id={id}">{username}#{id}</a>'
    sep = '\n'
    key = types.InlineKeyboardMarkup()
    for num, user in enumerate(array):
        emoji_num = getEmojiNumByInt(num)
        cnt += usr_temp.format(num=emoji_num,
                               level=user["level"].upper(),
                               id=str(user["id"]),
                               username=user["username"]) + sep
        key.add(types.InlineKeyboardButton(
            emoji_num,
            callback_data=sec.signData(f'usercontrol@{str(user["id"])}')
        ))
    return (cnt, key)


def parseUser(user: dict) -> str:
    '''Returns parsed user info for message.

    Args:
        user (dict): user info.

    Returns:
        str: message content.
    '''
    cnt = '<b>{level}:</b> <a href="tg://user?id={id}">{username}#{id}</a>\n\n'
    return cnt.format(level=user['level'].upper(), id=str(user['id']), username=user['username'])


def parseDevices(array: list) -> tuple:
    '''Returns message content with all devices from array.

    Args:
        array (list): devices array.

    Returns:
        tuple: message content with inline keyboard
    '''
    cnt = '      <code>Список устройств:</code>\n'
    dev_temp = '{}: <b>{} {}</b> - {} {}.'
    offline_dev_temp = '{}: <b>{} {}</b> - {} <code>{}</code>.'
    sep = '\n'
    key = types.InlineKeyboardMarkup(3)
    for num, device in enumerate(array):
        emoji_num = getEmojiNumByInt(num)
        key.insert(types.InlineKeyboardButton(
            emoji_num,
            callback_data=sec.signData(f'control@{device["uuid"]}')
        ))
        if device['status'].lower() == 'online':
            cnt += dev_temp.format(emoji_num, device["type"], device["alias"] if bool(
                device["alias"]) else device["hostname"], getStatusEmojiByStatus(device["status"]), device['status']) + sep
        else:
            cnt += offline_dev_temp.format(emoji_num, device["type"], device["alias"] if bool(
                device["alias"]) else device["hostname"], getStatusEmojiByStatus(device["status"]), device['status']) + sep
    return (cnt, key)


def parseDevice(device: dict, redline: bool = True) -> str:
    '''Returns message content with device info.

    Args:
        device (dict): device dict.
        redline (bool): Insert red line in begining.

    Returns:
        str: message content.
    '''
    if redline:
        cnt = '      {} <b>{}: {}</b>\n'
    else:
        cnt = '{} <b>{}: {}</b>\n'
    sep = '\n'
    device = device['device']
    cnt = cnt.format(
        getStatusEmojiByStatus(device['status']),
        device["type"],
        device['alias'] if bool(device['alias']) else device['hostname']
    )
    # [REMOVED]
    if device['code_version']:
        cnt += sep + f'<b>Версия LZSS:</b> <code>{device["code_version"]}</code>'
    return cnt


def getPlatformName(platform: str) -> str:
    '''Returns platform name by provided platform id.

    Args:
        platform (str): platform id.

    Returns:
        str: platform name.
    '''
    if platform == 'win32':
        return 'Windows'
    elif platform == 'linux':
        return 'Linux'
    elif platform == 'darwin':
        return 'macOS'
    else:
        return 'Unknown'


def parseDevicesForUser(array: list, user_access: str) -> list:
    '''Parse devices array for user.

    Args:
        array (list): devices array.
        user_access (str): user access level.

    Returns:
        list: devices array.
    '''
    devices = []
    for dev in array:
        if dev['network_access'] == user_access or user_access == 'admin':
            devices.append(dev)
    return devices


def userInDeviceGroup(user: dict, device: dict) -> bool:
    '''Checks if user have access to device by groups.

    Args:
        user (dict): user info.
        device (dict): device info.

    Returns:
        bool: Boolean.
    '''
    accessed = False
    for dev_group in device['groups']:
        if accessed:
            break
        for usr_group in user['groups']:
            if accessed:
                break
            accessed = dev_group == usr_group
    return accessed
