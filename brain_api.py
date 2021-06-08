# -*- coding: utf-8 -*-
#
#  PcControl - Brain Server API.
#  Created by LulzLoL231 at 04/11/20
#
import logging
import json
from logging import Logger
from base64 import b64encode
from datetime import datetime
from typing import Any, Dict, Optional, Union

import aiohttp

import config
from log import getLogger


def getLog(func: str) -> Logger:
    '''Returns specific logger with module and func name.

        Args:
            func (str): function name logger for.

        Returns:
            Logger: logging logger.
        '''
    return getLogger('PCON Brain API', func)


class Brain:
    '''PCON Brain Server API.
    '''
    def __init__(self, endpoint: str = 'https://example.com:8080'):
        self.SECRET = '[REMOVED]'
        self.tempdb: Dict[int, Dict[str, Any]] = {}
        if config.DEV:
            self.endpoint = 'http://localhost:5000'
        else:
            self.endpoint = endpoint

    async def _makeRequest(self, method: str, url: str, data: bytes = b'') -> dict:
        '''Make request to BRAIN server.

        Args:
            method (str): HTTP method.
            url (str): url method.
            data (bytes): body.

        Returns:
            dict: dict or empty dict.
        '''
        log = getLog('_makeRequest')
        log.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
        log.info(f'Called with args: ({method}, {url}) and data: ({str(data)})')
        full_url = self.endpoint + url
        try:
            async with aiohttp.request(method,
                                       full_url,
                                       headers={'[REMOVED]': self.SECRET},
                                       data=data) as resp:
                if resp.status != 500:
                    try:
                        result = await resp.json()
                    except Exception as e:
                        log.error(f'JSON Error: {str(e)}')
                        return {}
                    else:
                        if 'error' in result.keys():
                            log.error(
                                f'API Error {str(resp.status)} {result["error_type"]}: {result["error"]}')
                            return {}
                        else:
                            log.debug(f'API result: {str(result)}')
                            return result
                else:
                    log.error(
                        'Brain internal server error. Request can\'t be processed.')
                    return {}
        except Exception as e:
            log.error(f'Request Error: {str(e)}')
            return {}

    async def getDevicesForUser(self, id: int) -> Optional[Union[list, None]]:
        '''Returns registered devices for specified user.

        Returns:
            Optional[Union[list, None]]: Devices list or None if not found or unsuccessfull request.
        '''
        log = getLog('getDevicesForUser')
        log.info('Called.')
        url = '[REMOVED]'
        body = b64encode(json.dumps({'id': id}).encode())
        result = await self._makeRequest('GET', url, body)
        if result.get('ok', False):
            return result['devices']
        log.warning('Request unsuccessfull.')
        return None

    async def getDevice(self, device_uuid: str) -> Optional[Union[dict, None]]:
        '''Returns device dict or None if not found.

        Args:
            device_uuid (str): Device UUID.

        Returns:
            Optional[Union[dict, None]]: device dict or None.
        '''
        log = getLog('getDevice')
        log.info(f'Called with args: ({device_uuid})')
        url = '[REMOVED]'
        body = b64encode(json.dumps({
            'device_uuid': device_uuid
        }).encode())
        device = await self._makeRequest('GET', url, body)
        if device.get('ok', False):
            return device
        if 'ok' in device:
            log.error(
                f'Request error: {device["error_type"]}: {device["error"]}')
        else:
            log.warning('Request unsuccessfull.')
        return None

    async def addTask(self, type: str, device_uuid: str) -> Optional[Union[int, None]]:
        '''Returns task ID or None if unsuccessfull request.

        Args:
            type (str): Task Type (See README)
            device_uuid (str): Device UUID.

        Returns:
            Optional[Union[int, None]]: Task ID or None.
        '''
        log = getLog('addTask')
        log.info(f'Called with args: ({type}, {device_uuid})')
        url = '[REMOVED]'
        body = b64encode(json.dumps({
            'device_uuid': device_uuid,
            'type': type
        }).encode())
        task = await self._makeRequest('POST', url, body)
        if task.get('ok', False):
            log.info(f'Added new task "{type}" with #{task["id"]}@{device_uuid}')
            return task['id']
        if 'ok' in task:
            log.error(f'Task create error: {task.get("error_type")}: {task.get("error")}')
        else:
            log.error(f'Unknown error when try to create a new task "{type}" for device #{device_uuid}')
        return None

    async def getServerVersion(self) -> dict:
        '''Returns PCON Brain Server Version.

        Returns:
            dict: Server version dict.
        '''
        log = getLog('getServerVersion')
        log.info('Called.')
        url = '[REMOVED]'
        result = await self._makeRequest('GET', url)
        if result.get('ok', False):
            return result
        if 'ok' in result:
            log.error(f'Request error: {result["error_type"]}: {result["error"]}')
        else:
            log.warning('Request unsuccessfull.')
        return {}

    async def getClientVersion(self) -> dict:
        '''Returnc PCON Client latest version.

        Returns:
            dict: Client version dict.
        '''
        log = getLog('getClientVersion')
        log.info('Called.')
        url = '[REMOVED]'
        result = await self._makeRequest('GET', url)
        if result.get('ok', False):
            return result
        if 'ok' in result:
            log.error(f'Request error: {result["error_type"]}: {result["error"]}')
        else:
            log.warning('Request unsuccessfull.')
        return {}

    async def flushTasks(self, device_uuid: str, admin_code: str) -> bool:
        '''Flushes tasks for specific device.

        Args:
            device_uuid (str): Device UUID.
            admin_code (str): Admin code for executing.

        Returns:
            bool: True or False.
        '''
        log = getLog('flushTasks')
        log.info(f'Called with args: ({device_uuid}, {admin_code})')
        url = '[REMOVED]'
        body = b64encode(json.dumps({
            'device_uuid': device_uuid,
            'admin_code': admin_code
        }).encode())
        result = await self._makeRequest('DELETE', url, body)
        if result.get('ok', False):
            return True
        if 'ok' in result:
            log.error(f'Request error: {result["error_type"]}: {result["error"]}')
        else:
            log.warning('Request unsuccessfull.')
        return False

    async def getTasksForDevice(self, device_uuid: str) -> Optional[Union[list, None]]:
        '''Returns all current tasks for specific device.

        Args:
            device_uuid (str): Device UUID.

        Returns:
            Optional[Union[list, None]]: tasks array or None.
        '''
        log = getLog('getTasksForDevice')
        log.info(f'Called with args: ({device_uuid})')
        url = '[REMOVED]'
        body = b64encode(json.dumps({
            'device_uuid': device_uuid
        }).encode())
        result = await self._makeRequest('GET', url, body)
        if result.get('ok', False):
            return result['tasks']
        if 'ok' in result:
            log.error(f'Request error: {result["error_type"]}: {result["error"]}')
        else:
            log.warning('Request unsuccessfull.')
        return None

    async def getUser(self, id: int) -> Optional[Union[dict, None]]:
        '''Return user info by telegram id.

        Args:
            id (int): telegram id.

        Returns:
            Optional[Union[dict, None]]: dict, None.
        '''
        log = getLog('getUser')
        log.info(f'Called with args: ({str(id)})')
        log.info('Checking tempDB...')
        if id in self.tempdb.keys():
            td = (datetime.now() - self.tempdb[id]['fetched']).total_seconds()
            if td <= 300:
                log.info('User have unexpired access in tempDB.')
                return self.tempdb[id]
            else:
                log.info('User expired access in tempDB.')
                del(self.tempdb[id])
        url = '[REMOVED]'
        body = b64encode(json.dumps({
            'id': id
        }).encode())
        result = await self._makeRequest('GET', url, body)
        if result.get('ok', False):
            log.debug(f'Fetched user: {str(result["user"])}')
            result['user'].update({'fetched': datetime.now()})
            self.tempdb.update({id: result['user']})
            log.info(f'User #{str(id)} added to tempDB.')
            return result['user']
        if 'ok' in result:
            log.error(f'Request error: {result["error_type"]}: {result["error"]}')
        else:
            log.warning('Request unsuccessfull.')
        return None

    async def addUser(self,
                      id: int,
                      username: str,
                      admin_code: str,
                      level: str = 'user') -> bool:
        '''Created new user in BRAIN.

        Args:
            id (int): telegram id.
            username (str): user name.
            admin_code (str): 2FA code.
            level (str, optional): user access level. Defaults to 'user'.

        Returns:
            bool: True or False
        '''
        log = getLog('addUser')
        log.info(f'Called with args: ({str(id), username, level})')
        url = '[REMOVED]'
        body = b64encode(json.dumps({
            'id': id,
            'username': username,
            'level': level,
            'admin_code': admin_code
        }).encode())
        result = await self._makeRequest('POST', url, body)
        if result.get('ok', False):
            return True
        if 'ok' in result:
            log.error(f'Request error: {result["error_type"]}: {result["error"]}')
        else:
            log.warning('Request unsuccessfull.')
        return False

    async def deleteUser(self,
                         id: int,
                         admin_code: str) -> bool:
        '''Deletes user from BRAIN.

        Args:
            id (int): telegram id.
            admin_code (str): 2FA code.

        Returns:
            bool: True or False
        '''
        log = getLog('deleteUser')
        log.info(f'Called with args: ({str(id)})')
        url = '[REMOVED]'
        body = b64encode(json.dumps({
            'id': id,
            'admin_code': admin_code
        }).encode())
        result = await self._makeRequest('DELETE', url, body)
        if result.get('ok', False):
            return True
        if 'ok' in result:
            log.error(f'Request error: {result["error_type"]}: {result["error"]}')
        else:
            log.warning('Request unsuccessfull.')
        return False

    async def getUsers(self) -> Optional[Union[list, None]]:
        '''Returns all registered users.

        Returns:
            Optional[Union[list, None]]: tasks array or None.
        '''
        log = getLog('getUsers')
        log.info('Called!')
        url = '[REMOVED]'
        result = await self._makeRequest('GET', url)
        if result.get('ok', False):
            return result['users']
        if 'ok' in result:
            log.error(f'Request error: {result["error_type"]}: {result["error"]}')
        else:
            log.warning('Request unsuccessfull.')
        return None

    async def updateDeviceInfo(self, device_uuid: str,
                               key: str, value: str,
                               admin_code: str) -> bool:
        '''Обновляет данные устройства.

        Args:
            device_uuid (str): device uuid.
            key (str): info key.
            value (str): info value.
            admin_code (str): admin verify code.

        Returns:
            bool: Boolean.
        '''
        log = getLog('updateDeviceInfo')
        log.info(f'Called with args: ({str(id)})')
        url = '[REMOVED]'
        body = b64encode(json.dumps({
            'device_uuid': device_uuid,
            'admin_code': admin_code,
            'updates': {
                key: value
            }
        }).encode())
        result = await self._makeRequest('PATCH', url, body)
        if result.get('ok', False):
            return True
        if 'ok' in result:
            log.error(
                f'Request error: {result["error_type"]}: {result["error"]}')
        else:
            log.warning('Request unsuccessfull.')
        return False
