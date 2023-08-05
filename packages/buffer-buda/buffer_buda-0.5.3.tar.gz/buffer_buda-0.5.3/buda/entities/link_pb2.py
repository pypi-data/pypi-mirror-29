# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: buda/entities/link.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buda.entities import uuid_pb2 as buda_dot_entities_dot_uuid__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='buda/entities/link.proto',
  package='buda',
  syntax='proto3',
  serialized_pb=_b('\n\x18\x62uda/entities/link.proto\x12\x04\x62uda\x1a\x18\x62uda/entities/uuid.proto\"5\n\x04Link\x12\x0e\n\x06target\x18\x01 \x01(\t\x12\x1d\n\ttarget_id\x18\x02 \x01(\x0b\x32\n.buda.Uuidb\x06proto3')
  ,
  dependencies=[buda_dot_entities_dot_uuid__pb2.DESCRIPTOR,])




_LINK = _descriptor.Descriptor(
  name='Link',
  full_name='buda.Link',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='target', full_name='buda.Link.target', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target_id', full_name='buda.Link.target_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=113,
)

_LINK.fields_by_name['target_id'].message_type = buda_dot_entities_dot_uuid__pb2._UUID
DESCRIPTOR.message_types_by_name['Link'] = _LINK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Link = _reflection.GeneratedProtocolMessageType('Link', (_message.Message,), dict(
  DESCRIPTOR = _LINK,
  __module__ = 'buda.entities.link_pb2'
  # @@protoc_insertion_point(class_scope:buda.Link)
  ))
_sym_db.RegisterMessage(Link)


# @@protoc_insertion_point(module_scope)
