import logging
from collections import namedtuple
from struct import Struct
from io import BytesIO
import zlib

FILE_HEADER_STRUCT = Struct("<III")
BLOCK_HEADER_STRUCT = Struct("<IIII")

def extract_file(file_handle):
    (header_size, _, total_uncompressed_size) = FILE_HEADER_STRUCT.unpack(file_handle.read(FILE_HEADER_STRUCT.size))

    file_handle.seek(header_size - FILE_HEADER_STRUCT.size, 1)

    output = BytesIO()
    read_size = 0
    
    while True:
        (_, _, block_compressed_size, block_uncompressed_size) = BLOCK_HEADER_STRUCT.unpack(file_handle.read(BLOCK_HEADER_STRUCT.size))

        block_read_size = BLOCK_HEADER_STRUCT.size
        if block_compressed_size >= block_uncompressed_size:
            output.write(file_handle.read(block_uncompressed_size))
            block_read_size += block_uncompressed_size
        else:
            output.write(zlib.decompress(file_handle.read(block_compressed_size), -15))
            block_read_size += block_compressed_size

        read_size += block_uncompressed_size
        
        if read_size < total_uncompressed_size:
            real_block_size = ((block_read_size // 0x80) + (1 if block_read_size % 0x80 > 0x00 else 0)) * 0x80

            if real_block_size - block_read_size > 0:
                file_handle.seek(real_block_size - block_read_size, 1)
        else:
            break

    output.flush()
    output.seek(0x00)
    return output