# -*- coding: utf-8 -*-
#
#  PcControl - config file.
#  Created by LulzLoL231 at 04/11/20
#
import logging
from os import environ

DEV = False
DEBUG = False
ADMIN_ID = 0
SECRET = '[REMOVED]'
if 'pcon_DEV' in environ:
    TOKEN = '[REMOVED]'
    DEV = True
    DEBUG = True
elif 'pcon_DEBUG' in environ:
    TOKEN = '[REMOVED]'
    DEBUG = True
else:
    TOKEN = '[REMOVED]'
logging.basicConfig(
    format='[%(levelname)s] %(name)s (%(lineno)d) >> %(message)s',
    level=logging.DEBUG if DEBUG else logging.INFO)
logging.getLogger('aiogram').setLevel(logging.DEBUG if DEV else logging.INFO)
