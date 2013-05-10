import logging
from collections import namedtuple
from struct import Struct
from io import BytesIO
import zlib

FILE_HEADER_STRUCT = Struct("<IIIIII")
BLOCK_HEADER_STRUCT = Struct("<IIII")

BLOCK_INFOS_TYPE2 = Struct("<IHH")
BLOCK_INFOS_TYPE4 = Struct("<IIIII")

BLOCK_EFFECTIVE_SIZE = Struct("<H")

def extract_file(file_handle, offset):
    output = BytesIO()

    file_handle.seek(offset)
    (header_size, entry_type, total_uncompressed_size, _, _, block_count) = FILE_HEADER_STRUCT.unpack(file_handle.read(FILE_HEADER_STRUCT.size))

    if entry_type == 0x02:
        pos = file_handle.tell()
        blocks_infos = list()
        for block_index in range(block_count):
            file_handle.seek(pos)
            (relative_block_offset, _, _) = BLOCK_INFOS_TYPE2.unpack(file_handle.read(BLOCK_INFOS_TYPE2.size))
            pos = file_handle.tell()
            read_block(file_handle, offset + header_size + relative_block_offset, output)

    elif entry_type == 0x04:
        from_part = 0
        num_part = 0

        block_infos = list()
        for block_index in range(block_count):
            block_infos.append(BLOCK_INFOS_TYPE4.unpack(file_handle.read(BLOCK_INFOS_TYPE4.size)))
        
        real_block_count = block_infos[-1][3] + block_infos[-1][4]
        
        blocks_effective_size = list()
        for block_effective_size_index in range(real_block_count):
            blocks_effective_size.append(BLOCK_EFFECTIVE_SIZE.unpack(file_handle.read(BLOCK_EFFECTIVE_SIZE.size))[0])
        
        pos = offset + header_size + block_infos[0][0]
        for block_effective_size in blocks_effective_size:
            read_block(file_handle, pos, output)
            pos += block_effective_size

    elif entry_type == 0x03:
        # skipping bytes
        file_handle.seek(134, 1)
        
        read_size = 134 + FILE_HEADER_STRUCT.size
        blocks_effective_size = list()
        while read_size < header_size:
            block_effective_size = BLOCK_EFFECTIVE_SIZE.unpack(file_handle.read(BLOCK_EFFECTIVE_SIZE.size))[0]
            if block_effective_size == 0x00:
                break
            blocks_effective_size.append(block_effective_size)
        
        pos = offset + header_size
        for block_effective_size in blocks_effective_size:
            read_block(file_handle, pos, output)
            pos += block_effective_size
    else:
        raise Exception("Unknown entry type: %d" % entry_type)

    return output


def read_block(file_handle, offset, output):
    file_handle.seek(offset)
    (header_size, _, block_compressed_size, block_uncompressed_size) = BLOCK_HEADER_STRUCT.unpack(file_handle.read(BLOCK_HEADER_STRUCT.size))

    if block_compressed_size >= block_uncompressed_size:
        output.write(file_handle.read(block_uncompressed_size))
    else:
        output.write(zlib.decompress(file_handle.read(block_compressed_size), -15))