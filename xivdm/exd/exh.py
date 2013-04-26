import logging
from collections import namedtuple
from struct import Struct

HEADER_STRUCT = Struct(">4sHHHHH")
MEMBER_STRUCT = Struct(">HH")
START_ID_STRUCT = Struct(">II")
LANGUAGE_STRUCT = Struct("<H")

MEMBER_NT = namedtuple('member', ['type', 'offset'])
HEADER_NT = namedtuple('exh', ['field_count', 'start_id', 'languages', 'members', 'data_offset'])

def extract_header(file_handle):
    (_, _, data_offset, field_count, _, language_count) = HEADER_STRUCT.unpack(file_handle.read(HEADER_STRUCT.size))

    file_handle.seek(0x20) # skip header

    members = list()
    for index in range(field_count):
        members.append(MEMBER_NT._make(MEMBER_STRUCT.unpack(file_handle.read(MEMBER_STRUCT.size))))

    (start_id, _) = START_ID_STRUCT.unpack(file_handle.read(START_ID_STRUCT.size))

    languages = list()
    for index in range(language_count):
        languages.append(LANGUAGE_STRUCT.unpack(file_handle.read(LANGUAGE_STRUCT.size))[0])

    return HEADER_NT._make((field_count, start_id, languages, members, data_offset))
