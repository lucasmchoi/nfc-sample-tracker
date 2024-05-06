# -*- coding: utf-8 -*-
"""
Created on Thursday, 2024-05-02 23:39

@author: Luca Sung-Min Choi (gitcontact@email.lucachoi.de)
"""
from typing import Type, Union
from pirc522 import RFID
import ndef


NTAG_NON_USER_PAGES = 9
NTAG_PRE_MEMORY = 4
NTAG_TRAILING_MEMORY = 5
NTAG_STRUCTURE_PAGES = {'serial number': [0, 2], 'static lock bytes': [2, 3], 'capability container': [3, 4], 'user memory': [4, -5], 'configuration pages': [-5, None]}
NTAG_STRUCTURE_BYTES = {'serial number': [0, 8], 'static lock bytes': [8, 12], 'capability container': [12, 16], 'user memory': [16, -20], 'configuration pages': [-20, None]}
TLV_NULL = 0x00
TLV_NDEF_MESSAGE = 0x03
TLV_PROPRIETARY = 0xFD
TLV_TERMINATOR = 0xFE


def begin_tag(reader: Type[RFID]) -> tuple[bool, str]:
    """run anticollision and tag selection before reading or writing

    Args:
        reader (Type[RFID]): RFID class from pirc522

    Returns:
        tuple[bool, str]: bool to indicate error, uid of tag
    """
    (error, _) = reader.request()
    if not error:
        (error, uid) = reader.anticoll()
        if not error:
            error = reader.select_tag(uid)
            if not error:
                reader.read(0)
                return error, uid
            else:
                return error, uid
        else:
            return error, None
    else:
        return error, None


def stop_tag(reader: Type[RFID]) -> bool:
    """run cleanup after finished with reading and writing of tag

    Args:
        reader (Type[RFID]): RFID class from pirc522

    Returns:
        bool: bool to indicate error
    """
    reader.stop_crypto()
    reader.cleanup()
    return False


def get_ntag_memory(reader: Type[RFID]) -> tuple[bool, Union[None, int]]:
    """get the number of pages for NTAG21X

    Args:
        reader (Type[RFID]): RFID class from pirc522

    Returns:
        tuple[bool, Union[None, int]]: bool to indicate error, int returning number of pages
    """
    memory_pages = None
    error, data = read_ntag_page(reader, NTAG_STRUCTURE_PAGES['capability container'][0])

    if not error:
        match data[2]:
            case 0x12:
                # NTAG213 memory
                memory_pages = 45
            case 0x3E:
                # NTAG215 memory
                memory_pages = 135
            case 0x6D:
                # NTAG216 memory
                memory_pages = 231

    return error, memory_pages


def read_ntag_page(reader: Type[RFID], page: int) -> tuple[bool, list[int]]:
    """read specific page of NTAG21X

    Args:
        reader (Type[RFID]): RFID class from pirc522
        page (int): page of NTAG21X to be read

    Returns:
        tuple[bool, list[int]]: bool to indicate error, list with bytes of page
    """
    error, block = reader.read(page)
    return error, block[0:4]


def read_ntag_complete(reader: Type[RFID], printt: bool = False) -> tuple[bool, Union[None, tuple[list[int]]]]:
    """read complete NTAG21X

    Args:
        reader (Type[RFID]): RFID class from pirc522
        printt (bool, optional): bool to print data to terminal. Defaults to False.

    Returns:
        tuple[bool, Union[None, tuple[list[int]]]]: bool to indicate error, list with bytes of complete NTAG21X
    """
    error = []
    read_error, memory_pages = get_ntag_memory(reader)
    error.append(read_error)
    data_dump = None

    if not read_error:
        data = []

        for page in range(memory_pages):
            page_error, page_data = read_ntag_page(reader, page)
            error.append(page_error)
            data.extend(page_data)

        if printt:
            for page in range(0, memory_pages, 4):
                hex_string = ''
                chr_string = ''
                line = data[4 * page:4 * page + 4 * 4]
                for value in line:
                    hex_string += '{:02X} '.format(value)
                    if value > 20 and value < 127:
                        chr_string += chr(value)
                    else:
                        chr_string += '.'
                print('Page {: >4}:   {: <48}   {: <16}'.format(
                    page, hex_string, chr_string))
                
        data_dump = (data[NTAG_STRUCTURE_BYTES['serial number'][0]:NTAG_STRUCTURE_BYTES['serial number'][1]],
                     data[NTAG_STRUCTURE_BYTES['static lock bytes'][0]:NTAG_STRUCTURE_BYTES['static lock bytes'][1]],
                     data[NTAG_STRUCTURE_BYTES['capability container'][0]:NTAG_STRUCTURE_BYTES['capability container'][1]],
                     data[NTAG_STRUCTURE_BYTES['user memory'][0]:NTAG_STRUCTURE_BYTES['user memory'][1]],
                     data[NTAG_STRUCTURE_BYTES['configuration pages'][0]:NTAG_STRUCTURE_BYTES['configuration pages'][1]])
        
    return any(error), data_dump


def read_ntag_container(reader: Type[RFID], container: str = 'user memory') -> tuple[bool, list[int]]:
    """read specific container of NTAG21X

    Args:
        reader (Type[RFID]): RFID class from pirc522
        container (str, optional): NTAG21X container to be read. Defaults to 'user memory'.

    Returns:
        tuple[bool, list[int]]: bool to indicate error, list with bytes of complete NTAG21X
    """
    if container not in NTAG_STRUCTURE_PAGES.keys():
        return True, []
    
    error = []
    data = []

    read_error, memory_pages = get_ntag_memory(reader)
    error.append(read_error)

    rangeind = []

    for index in NTAG_STRUCTURE_PAGES[container]:
        if index == None:
            rangeind.append(memory_pages)
        elif index < 0:
            rangeind.append(memory_pages + index)
        else:
            rangeind.append(index)

    for page in range(*rangeind):
        page_error, page_data = read_ntag_page(reader, page)
        error.append(page_error)
        data.extend(page_data)

    return any(error), data


def write_ntag_page(reader: Type[RFID], message: list = [0, 0, 0, 0], page: int = NTAG_STRUCTURE_PAGES['user memory'][0]) -> bool:
    """write specific NTAG21X page

    Args:
        reader (Type[RFID]): RFID class from pirc522
        message (list, optional): page bytes to be written. Defaults to [0, 0, 0, 0].
        page (int, optional): page to be written. Defaults to 4.

    Returns:
       bool: bool to indicate error
    """
    error = []

    if page < NTAG_STRUCTURE_PAGES['user memory'][0]:
        return True
    if len(message) != 4:
        return True
    error.append(reader.write(page, message+[0]*12))

    return any(error)


def write_ntag_message(reader: Type[RFID], message: list = [0, 0, 0, 0], page: int = NTAG_STRUCTURE_PAGES['user memory'][0]) -> bool:
    """write message to NTAG21X beginning with specific page

    Args:
        reader (Type[RFID]): RFID class from pirc522
        message (list, optional): message bytes to be written. Defaults to [0, 0, 0, 0].
        page (int, optional): page to start writing. Defaults to 4.

    Returns:
        bool: bool to indicate error
    """
    error = []
    read_error, memory_pages = get_ntag_memory(reader)
    error.append(read_error)

    if not read_error:
        if page < NTAG_STRUCTURE_PAGES['user memory'][0]:
            return True
        if len(message) > (memory_pages - NTAG_NON_USER_PAGES - page + NTAG_STRUCTURE_PAGES['user memory'][0]) * 4:
            return True
        while len(message) % 4 != 0:
            message.append(0)
        
        for i in range(len(message) // 4):
            error.append(write_ntag_page(reader, message[4*i:4*i+4], page + i))

    return any(error)


def clear_ntag_usermemory(reader: Type[RFID]) -> bool:
    """clear complete user memory of NTAG21X

    Args:
        reader (Type[RFID]): RFID class from pirc522

    Returns:
        list[bool]: bool to indicate error
    """
    error = []
    read_error, memory_pages = get_ntag_memory(reader)
    error.append(read_error)

    if not read_error:
        for page in range(NTAG_PRE_MEMORY, memory_pages - NTAG_TRAILING_MEMORY):
            error.append(reader.write(page, [0]*16))

    return any(error)


def check_ntag_usermemeory_beginning(reader: Type[RFID]) -> tuple[bool, bool]:
    """_summary_

    Args:
        reader (Type[RFID]): RFID class from pirc522

    Returns:
        tuple[bool, bool]: bool to indicate error, bool to indicate empty
    """
    empty = True
    expected_empty = [[0x01, 0x03, 0x0], [0x3, 0x0], [0xA0, 0xFE, 0x0], [0x0C, 0x0]]
    error, data = read_ntag_page(reader, NTAG_STRUCTURE_PAGES['user memory'][0])
    if not error:
        for i in range(4):
            if data[i] not in expected_empty[i]:
                empty = False
    
    return error, empty


def create_ndef_tlv_wrap(ndef_message: list[int]) -> list[int]:
    """wrap ndef message in tvl block

    Args:
        ndef_message (list): list of message to be written

    Returns:
        list[int]: list of message bytes
    """
    message = []

    message.append(TLV_NDEF_MESSAGE)
    message.append(len(ndef_message))
    message.extend(ndef_message)
    message.append(TLV_TERMINATOR)
    
    return message


def create_ndef_message(records: list[Union[ndef.uri.UriRecord, ndef.text.TextRecord]]) -> list[int]:
    """create TLV wrapped ndef message from supplied ndef records
    
    Args:
        records (list[Union[ndef.uri.UriRecord, ndef.text.TextRecord]]): ndef records to be joined and wrapped

    Returns:
        list[int]: list of message bytes
    """
    
    msg = b''.join((ndef.message_encoder(records)))
    wrapped_message = create_ndef_tlv_wrap(list(msg))

    return wrapped_message


def find_and_parse_ndef_message(userdata: list[int]) -> tuple[bool, list[list], list[list[Union[None, str]]]]:
    """find ndef messages in provided userdata

    Args:
        userdata (list[int]): userdata list returned from read_ntag_container()

    Returns:
        tuple[bool, list[list], list[list[Union[None, str]]]]: bool to indicate error, list of lists of ndef message bytes, list of parsed ndef message strings or None
    """
    ndef_bytes_messages = []
    ndef_messages = []
    starts = []
    stops = []
    errors = [False]
    
    for index, value in enumerate(userdata):
        if value == TLV_NDEF_MESSAGE:
            starts.append(index)
            minpos = index + 4
        elif value == TLV_TERMINATOR and index > minpos:
            stops.append(index)

    npairs = min(len(starts), len(stops))

    if npairs == 0:
        return True, ndef_bytes_messages
    
    for i in range(npairs):
        ndef_bytes_messages.append(userdata[starts[i]+2:stops[i]])
    
    for message in ndef_bytes_messages:
        try:
            rpayloads = []
            for record in ndef.message_decoder(bytes(message)):
                match record.type:
                    case 'urn:nfc:wkt:U':
                        rpayloads.append(record.iri)
                    case 'urn:nfc:wkt:T':
                        rpayloads.append(record.text)
                    case _:
                        rpayloads.append(False)

            ndef_messages.append(rpayloads)
        except:
            errors.append(True)

    return any(errors), ndef_bytes_messages, ndef_messages
