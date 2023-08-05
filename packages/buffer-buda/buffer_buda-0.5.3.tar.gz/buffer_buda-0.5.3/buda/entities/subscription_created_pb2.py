# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: buda/entities/subscription_created.proto

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
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from buda.entities import subscription_status_pb2 as buda_dot_entities_dot_subscription__status__pb2
from buda.entities import payment_terms_pb2 as buda_dot_entities_dot_payment__terms__pb2
from buda.entities import payment_schedule_pb2 as buda_dot_entities_dot_payment__schedule__pb2
from buda.entities import payment_type_pb2 as buda_dot_entities_dot_payment__type__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='buda/entities/subscription_created.proto',
  package='buda',
  syntax='proto3',
  serialized_pb=_b('\n(buda/entities/subscription_created.proto\x12\x04\x62uda\x1a\x18\x62uda/entities/uuid.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\'buda/entities/subscription_status.proto\x1a!buda/entities/payment_terms.proto\x1a$buda/entities/payment_schedule.proto\x1a buda/entities/payment_type.proto\"\x84\x06\n\x13SubscriptionCreated\x12\x16\n\x02id\x18\x01 \x01(\x0b\x32\n.buda.Uuid\x12\x1b\n\x07user_id\x18\x02 \x01(\x0b\x32\n.buda.Uuid\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12<\n\x0csubscription\x18\x04 \x01(\x0b\x32&.buda.SubscriptionCreated.Subscription\x12\x32\n\x07payment\x18\x05 \x01(\x0b\x32!.buda.SubscriptionCreated.Payment\x1a\xaf\x03\n\x0cSubscription\x12\x16\n\x02id\x18\x01 \x01(\x0b\x32\n.buda.Uuid\x12(\n\x06status\x18\x02 \x01(\x0e\x32\x18.buda.SubscriptionStatus\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1b\n\x07plan_id\x18\x04 \x01(\x0b\x32\n.buda.Uuid\x12\x11\n\tplan_name\x18\x05 \x01(\t\x12\x1b\n\x13gateway_customer_id\x18\x06 \x01(\t\x12)\n\rpayment_terms\x18\x07 \x01(\x0e\x32\x12.buda.PaymentTerms\x12/\n\x10payment_schedule\x18\x08 \x01(\x0e\x32\x15.buda.PaymentSchedule\x12\x12\n\nterm_value\x18\t \x01(\x02\x12\x38\n\x14initial_period_start\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x36\n\x12initial_period_end\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a\x64\n\x07Payment\x12\x16\n\x02id\x18\x01 \x01(\x0b\x32\n.buda.Uuid\x12\x1f\n\x04type\x18\x02 \x01(\x0e\x32\x11.buda.PaymentType\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x02\x12\x10\n\x08\x63urrency\x18\x04 \x01(\tb\x06proto3')
  ,
  dependencies=[buda_dot_entities_dot_uuid__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,buda_dot_entities_dot_subscription__status__pb2.DESCRIPTOR,buda_dot_entities_dot_payment__terms__pb2.DESCRIPTOR,buda_dot_entities_dot_payment__schedule__pb2.DESCRIPTOR,buda_dot_entities_dot_payment__type__pb2.DESCRIPTOR,])




_SUBSCRIPTIONCREATED_SUBSCRIPTION = _descriptor.Descriptor(
  name='Subscription',
  full_name='buda.SubscriptionCreated.Subscription',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='buda.SubscriptionCreated.Subscription.id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='buda.SubscriptionCreated.Subscription.status', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='buda.SubscriptionCreated.Subscription.created_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='plan_id', full_name='buda.SubscriptionCreated.Subscription.plan_id', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='plan_name', full_name='buda.SubscriptionCreated.Subscription.plan_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gateway_customer_id', full_name='buda.SubscriptionCreated.Subscription.gateway_customer_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payment_terms', full_name='buda.SubscriptionCreated.Subscription.payment_terms', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payment_schedule', full_name='buda.SubscriptionCreated.Subscription.payment_schedule', index=7,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='term_value', full_name='buda.SubscriptionCreated.Subscription.term_value', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='initial_period_start', full_name='buda.SubscriptionCreated.Subscription.initial_period_start', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='initial_period_end', full_name='buda.SubscriptionCreated.Subscription.initial_period_end', index=10,
      number=11, type=11, cpp_type=10, label=1,
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
  serialized_start=497,
  serialized_end=928,
)

_SUBSCRIPTIONCREATED_PAYMENT = _descriptor.Descriptor(
  name='Payment',
  full_name='buda.SubscriptionCreated.Payment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='buda.SubscriptionCreated.Payment.id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='buda.SubscriptionCreated.Payment.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='buda.SubscriptionCreated.Payment.amount', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='currency', full_name='buda.SubscriptionCreated.Payment.currency', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=930,
  serialized_end=1030,
)

_SUBSCRIPTIONCREATED = _descriptor.Descriptor(
  name='SubscriptionCreated',
  full_name='buda.SubscriptionCreated',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='buda.SubscriptionCreated.id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='buda.SubscriptionCreated.user_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='buda.SubscriptionCreated.created_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subscription', full_name='buda.SubscriptionCreated.subscription', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payment', full_name='buda.SubscriptionCreated.payment', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_SUBSCRIPTIONCREATED_SUBSCRIPTION, _SUBSCRIPTIONCREATED_PAYMENT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=258,
  serialized_end=1030,
)

_SUBSCRIPTIONCREATED_SUBSCRIPTION.fields_by_name['id'].message_type = buda_dot_entities_dot_uuid__pb2._UUID
_SUBSCRIPTIONCREATED_SUBSCRIPTION.fields_by_name['status'].enum_type = buda_dot_entities_dot_subscription__status__pb2._SUBSCRIPTIONSTATUS
_SUBSCRIPTIONCREATED_SUBSCRIPTION.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_SUBSCRIPTIONCREATED_SUBSCRIPTION.fields_by_name['plan_id'].message_type = buda_dot_entities_dot_uuid__pb2._UUID
_SUBSCRIPTIONCREATED_SUBSCRIPTION.fields_by_name['payment_terms'].enum_type = buda_dot_entities_dot_payment__terms__pb2._PAYMENTTERMS
_SUBSCRIPTIONCREATED_SUBSCRIPTION.fields_by_name['payment_schedule'].enum_type = buda_dot_entities_dot_payment__schedule__pb2._PAYMENTSCHEDULE
_SUBSCRIPTIONCREATED_SUBSCRIPTION.fields_by_name['initial_period_start'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_SUBSCRIPTIONCREATED_SUBSCRIPTION.fields_by_name['initial_period_end'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_SUBSCRIPTIONCREATED_SUBSCRIPTION.containing_type = _SUBSCRIPTIONCREATED
_SUBSCRIPTIONCREATED_PAYMENT.fields_by_name['id'].message_type = buda_dot_entities_dot_uuid__pb2._UUID
_SUBSCRIPTIONCREATED_PAYMENT.fields_by_name['type'].enum_type = buda_dot_entities_dot_payment__type__pb2._PAYMENTTYPE
_SUBSCRIPTIONCREATED_PAYMENT.containing_type = _SUBSCRIPTIONCREATED
_SUBSCRIPTIONCREATED.fields_by_name['id'].message_type = buda_dot_entities_dot_uuid__pb2._UUID
_SUBSCRIPTIONCREATED.fields_by_name['user_id'].message_type = buda_dot_entities_dot_uuid__pb2._UUID
_SUBSCRIPTIONCREATED.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_SUBSCRIPTIONCREATED.fields_by_name['subscription'].message_type = _SUBSCRIPTIONCREATED_SUBSCRIPTION
_SUBSCRIPTIONCREATED.fields_by_name['payment'].message_type = _SUBSCRIPTIONCREATED_PAYMENT
DESCRIPTOR.message_types_by_name['SubscriptionCreated'] = _SUBSCRIPTIONCREATED
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SubscriptionCreated = _reflection.GeneratedProtocolMessageType('SubscriptionCreated', (_message.Message,), dict(

  Subscription = _reflection.GeneratedProtocolMessageType('Subscription', (_message.Message,), dict(
    DESCRIPTOR = _SUBSCRIPTIONCREATED_SUBSCRIPTION,
    __module__ = 'buda.entities.subscription_created_pb2'
    # @@protoc_insertion_point(class_scope:buda.SubscriptionCreated.Subscription)
    ))
  ,

  Payment = _reflection.GeneratedProtocolMessageType('Payment', (_message.Message,), dict(
    DESCRIPTOR = _SUBSCRIPTIONCREATED_PAYMENT,
    __module__ = 'buda.entities.subscription_created_pb2'
    # @@protoc_insertion_point(class_scope:buda.SubscriptionCreated.Payment)
    ))
  ,
  DESCRIPTOR = _SUBSCRIPTIONCREATED,
  __module__ = 'buda.entities.subscription_created_pb2'
  # @@protoc_insertion_point(class_scope:buda.SubscriptionCreated)
  ))
_sym_db.RegisterMessage(SubscriptionCreated)
_sym_db.RegisterMessage(SubscriptionCreated.Subscription)
_sym_db.RegisterMessage(SubscriptionCreated.Payment)


# @@protoc_insertion_point(module_scope)
