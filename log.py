# -*- coding: utf-8 -*-
#
#  PcControl - logging funcs.
#  Created by LulzLoL231 at 04/11/20
#
import logging

import config


def getLogger(module: str, name: str) -> logging.Logger:
    '''getLogger: returns named logger ready for work.

    Args:
        module (str): module name.
        name (str): logger name.

    Returns:
        logging.Logger: Logger instance.
    '''
    log = logging.getLogger(f'{module}::{name}')
    log.setLevel(logging.DEBUG if config.DEV else logging.INFO)
    return log
