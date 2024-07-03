# -*- coding: utf-8 -*-
"""
Created on Tuesday, 2024-07-02 23:59

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright © 2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""
from os import getenv

def getenvbool(key, default=False):
    """check a environmental variable if it is set to true

    Args:
        key (str): environmental variable to return the bool representation
        default (bool, optional): default bool. Defaults to False.

    Returns:
        bool: converted bool of the environment variable
    """
    return getenv(key, str(default)).upper() == 'TRUE'
