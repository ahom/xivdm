import logging
import struct

class BufferObject:
    def __init__(self, file_handle):
        self._first_mesh_index = None
        self._mesh_nb = None
        self._vertex_buffer = None
        self._index_buffer = None

        self._read(file_handle)

    def _read(self, file_handle):
        (self._first_mesh_index, self._mesh_nb) = struct.unpack("<HH", file_handle.read(4))

        file_handle.seek(0x28, 1) # skipping unimportant stuff

        (vertex_buffer_size, index_buffer_size, vertex_buffer_offset, index_buffer_offset) = struct.unpack("<IIII", file_handle.read(16))

        pos = file_handle.tell()

        file_handle.seek(vertex_buffer_offset)
        self._vertex_buffer = file_handle.read(vertex_buffer_size)
        file_handle.seek(index_buffer_offset)
        self._index_buffer = file_handle.read(index_buffer_size)

        file_handle.seek(pos)

    def __repr__(self):
        return "<first_mesh_index: %d - mesh_nb: %d>" % (self._first_mesh_index, self._mesh_nb)

class Mesh:
    def __init__(self, file_handle):
        self._buffer_object_id = None

        self._vertex_buffer_offset = None
        self._vertex_count = None
        self._vertex_size = None

        self._index_buffer_offset = None
        self._index_count = None

        self._read(file_handle)

    def set_buffer_object_id(self, buffer_object_id):
        self._buffer_object_id = buffer_object_id

    def _read(self, file_handle):
        (self._vertex_count, self._index_count) = struct.unpack("<II", file_handle.read(8))

        file_handle.seek(0x8, 1)

        (self._index_buffer_offset, self._vertex_buffer_offset) = struct.unpack("<II", file_handle.read(8))

        file_handle.seek(0x8, 1)

        (self._vertex_size,) = struct.unpack("<B", file_handle.read(1))

        file_handle.seek(0x3, 1)

    def __repr__(self):
        return "<vertex_buffer_offset: %d - vertex_count: %d - vertex_size: %d - index_buffer_offet: %d - index_count: %d>" % (self._vertex_buffer_offset, self._vertex_count, self._vertex_size, self._index_buffer_offset, self._index_count)

class Model:
    def __init__(self, path, file_handle):
        self._path = path
        self._buffer_objects = []
        self._meshes = []
        self._read(file_handle)

    def get_path(self):
        return self._path

    def _read(self, file_handle):
        logging.info('Reading file: %s' % self._path)

        file_handle.seek(0x40)

        (mesh_nb, material_nb) = struct.unpack("<HH", file_handle.read(4))

        file_handle.seek(0x88 * mesh_nb, 1) # Skipping mesh headers

        file_handle.seek(0x4, 1) # Skipping number of strings

        (string_block_size, ) = struct.unpack("<I", file_handle.read(4))

        file_handle.seek(string_block_size, 1) # Skipping string block

        file_handle.seek(0x38, 1) # Skipping header

        for i in range(3):
            self._buffer_objects.append(BufferObject(file_handle))

        for j in range(mesh_nb):
            self._meshes.append(Mesh(file_handle))

        for index, buffer_object in enumerate(self._buffer_objects):
            for mesh_nb in range(buffer_object._first_mesh_index, buffer_object._first_mesh_index + buffer_object._mesh_nb):
                self._meshes[mesh_nb].set_buffer_object_id(index)

        logging.info(self._buffer_objects)
        logging.info(self._meshes)
