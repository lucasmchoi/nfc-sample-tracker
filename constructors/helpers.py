# -*- coding: utf-8 -*-
"""
Created on Tuesday, 2024-06-18 20:01

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
@copyright: Copyright ©  2024 Luca Sung-Min Choi
@license: AGPL v3
@links: https://github.com/lucasmchoi
"""


def check_menu_selection(fpath, mode, elen=0):
    defpath = fpath.split("/")
    length = len(defpath)

    if length == elen + 1:
        match length:
            case 1:
                if mode == defpath[0]:
                    return True
                else:
                    return False
            case 2:
                if defpath[1] == mode:
                    return True
                else:
                    return False
            case 3:
                if defpath[1] == mode:
                    return True
                else:
                    return False
            case _:
                return False
    else:
        return False
