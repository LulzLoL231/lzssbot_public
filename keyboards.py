# -*- coding: utf-8 -*-
#
#  PcControl - keyboards.
#  Created by LulzLoL231 at 29/11/20
#
from aiogram import types

import security as sec
from emojis import Emojis
from security import getLogger


class Keyboards:
    '''PCON Telegram Keyboards class.
    '''
    def __init__(self, user: dict) -> None:
        self.hubs_text = 'Хабы'
        self.devices_text = 'Устройства'
        self.netstatus_text = 'Статус сетей'
        self.help_text = 'Помощь'
        self.users_text = 'Пользователи'
        self.back_text = f'{Emojis.back_page} Назад'
        self.lock_text = Emojis.lock
        self.vc_demount_text = Emojis.key
        self.switch_text = Emojis.switch
        self.reboot_text = Emojis.reboot
        self.sleep_text = Emojis.sleep
        self.poweroff_text = Emojis.poweroff
        self.media_play_pause_text = Emojis.play_pause
        self.media_stop_text = Emojis.stop
        self.media_prev_track_text = Emojis.prev_track
        self.media_next_track_text = Emojis.next_track
        self.media_max_volume_text = 'MAX'
        self.media_50_volume_text = '50'
        self.media_min_volume_text = 'MIN'
        self.media_volume_up_text = Emojis.plus
        self.media_volume_down_text = Emojis.minus
        self.media_mute_text = Emojis.mute
        self.user_level = user['level']
        self.userctrl_delete_text = f'{Emojis.cancel} Отозвать права'
        self.userctrl_rename_text = f'{Emojis.pen} Изменить имя'
        self.userctrl_levelup_text = f'{Emojis.warning} Повысить права'
        self.userctrl_leveldown_text = f'{Emojis.warning} Понизить права'
        self.device_rename_alias_text = f'{Emojis.pen} Изменить псевдоним'

    def start(self) -> types.ReplyKeyboardMarkup:
        '''Returns telegram reply markup keyboard for "start" cmd.

        Returns:
            types.ReplyKeyboardMarkup: telegram markup keyboard.
        '''
        key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if self.user_level == 'user':
            key.row(self.devices_text)
            key.row(self.help_text)
        else:
            key.row(self.hubs_text, self.devices_text)
            key.row(self.help_text, self.netstatus_text)
            key.row(self.users_text)
        return key

    def controlDevice(self, device: dict) -> types.InlineKeyboardMarkup:
        '''Returns inline keyboard with device control buttons.

        Args:
           device (dict): device info.

        Returns:
            types.InlineKeyboardMarkup: telegram inline keyboard.
        '''
        getLogger('keyboards', 'controlDevice').debug(
            f'Called with device: {str(device)}')
        key = types.InlineKeyboardMarkup()
        lockbtn = types.InlineKeyboardButton(
            self.lock_text,
            callback_data=sec.signData(f'lock@{device["uuid"]}')
        )
        if device['type'] == 'PC' and device['platform_name'] == 'win32' and device['has_proxy'] is True:
            switchbtn = types.InlineKeyboardButton(
                self.switch_text,
                callback_data=sec.signData(f'switch_proxy@{device["uuid"]}')
            )
            if device['has_vc'] is True:
                vc_demountbtn = types.InlineKeyboardButton(
                    self.vc_demount_text,
                    callback_data=sec.signData(f'vc_demount@{device["uuid"]}')
                )
                key.row(lockbtn, switchbtn, vc_demountbtn)
            else:
                key.row(lockbtn, switchbtn)
        else:
            key.row(lockbtn)
        rebootbtn = types.InlineKeyboardButton(
            self.reboot_text,
            callback_data=sec.signData(f'reboot@{device["uuid"]}')
        )
        poweroffbtn = types.InlineKeyboardButton(
            self.poweroff_text,
            callback_data=sec.signData(f'shutdown@{device["uuid"]}')
        )
        sleepbtn = types.InlineKeyboardButton(
            self.sleep_text,
            callback_data=sec.signData(f'sleep@{device["uuid"]}')
        )
        prev_track_btn = types.InlineKeyboardButton(
            self.media_prev_track_text,
            callback_data=sec.signData(f'media_prev@{device["uuid"]}')
        )
        play_pause_btn = types.InlineKeyboardButton(
            self.media_play_pause_text,
            callback_data=sec.signData(f'media_play_pause@{device["uuid"]}')
        )
        next_track_btn = types.InlineKeyboardButton(
            self.media_next_track_text,
            callback_data=sec.signData(f'media_next@{device["uuid"]}')
        )
        vol_max_btn = types.InlineKeyboardButton(
            self.media_max_volume_text,
            callback_data=sec.signData(f'media_vol_max@{device["uuid"]}')
        )
        vol_50_btn = types.InlineKeyboardButton(
            self.media_50_volume_text,
            callback_data=sec.signData(f'media_vol_50@{device["uuid"]}')
        )
        vol_min_btn = types.InlineKeyboardButton(
            self.media_min_volume_text,
            callback_data=sec.signData(f'media_vol_min@{device["uuid"]}')
        )
        vol_up_btn = types.InlineKeyboardButton(
            self.media_volume_up_text,
            callback_data=sec.signData(f'media_vol_up@{device["uuid"]}')
        )
        mute_btn = types.InlineKeyboardButton(
            self.media_mute_text,
            callback_data=sec.signData(f'media_mute@{device["uuid"]}')
        )
        vol_down_btn = types.InlineKeyboardButton(
            self.media_volume_down_text,
            callback_data=sec.signData(f'media_vol_down@{device["uuid"]}')
        )
        rename_btn = types.InlineKeyboardButton(
            self.device_rename_alias_text,
            callback_data=sec.signData(f'rename@{device["uuid"]}')
        )
        back_btn = types.InlineKeyboardButton(
            self.back_text,
            callback_data='devices'
        )
        key.row(rebootbtn, sleepbtn, poweroffbtn)
        key.row(prev_track_btn, play_pause_btn, next_track_btn)
        key.row(vol_up_btn, mute_btn, vol_down_btn)
        key.row(vol_max_btn, vol_50_btn, vol_min_btn)
        key.row(rename_btn)
        key.row(back_btn)
        return key

    def getReturnKey(self) -> types.InlineKeyboardMarkup:
        '''Returns 'Return' button keyboard.

        Returns:
            types.InlineKeyboardMarkup: telegram inline keyboard.
        '''
        key = types.InlineKeyboardMarkup()
        key.row(types.InlineKeyboardButton(
            self.back_text,
            callback_data='devices'
        ))
        return key

    def controlUser(self, user: dict) -> types.InlineKeyboardMarkup:
        '''User control keyboard.

        Args:
            user (dict): user info.

        Returns:
            types.InlineKeyboardMarkup: telegram inline keyboard.
        '''
        getLogger('keyboards', 'controlUser').debug(f'Called with user: {str(user)}')
        rename_btn = types.InlineKeyboardButton(
            self.userctrl_rename_text,
            callback_data=sec.signData(f'renameuser@{str(user["id"])}')
        )
        if user['level'] == 'user':
            level_btn = types.InlineKeyboardButton(
                self.userctrl_levelup_text,
                callback_data=sec.signData(f'levelupuser@{str(user["id"])}')
            )
        else:
            level_btn = types.InlineKeyboardButton(
                self.userctrl_leveldown_text,
                callback_data=sec.signData(f'leveldownuser@{str(user["id"])}')
            )
        delete_btn = types.InlineKeyboardButton(
            self.userctrl_delete_text,
            callback_data=sec.signData(f'deleteuser@{str(user["id"])}')
        )
        key = types.InlineKeyboardMarkup()
        key.row(rename_btn)
        key.row(level_btn, delete_btn)
        key.row(types.InlineKeyboardButton(
            self.back_text,
            callback_data='users'
        ))
        return key
