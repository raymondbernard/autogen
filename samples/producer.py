import os
import csv
import glob
import logging
import pathlib
from ai_agent_pb2 import Ai

from dotenv import load_dotenv
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic, KafkaException
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

load_dotenv()
logging.basicConfig(level=logging.INFO)

redpanda_brokers = os.getenv("REDPANDA_BROKERS")
redpanda_schema_registry = os.getenv("REDPANDA_SCHEMA_REGISTRY")
kafka_security_protocol = os.getenv("KAFKA_SECURITY_PROTOCOL")
kafka_sasl_mechanism = os.getenv("KAFKA_SASL_MECHANISM")
redpanda_username = os.getenv("REDPANDA_USERNAME")
redpanda_password = os.getenv("REDPANDA_PASSWORD")
redpanda_topic = os.getenv("REDPANDA_TOPIC")
logging.info("Connecting to: %s", redpanda_brokers)

conf = {"bootstrap.servers": redpanda_brokers}
if kafka_security_protocol and "SASL" in kafka_security_protocol:
    conf.update(
        {
            "security.protocol": kafka_security_protocol,
            "sasl_mechanism": kafka_sasl_mechanism,
            "sasl_plain_username": redpanda_username,
            "sasl_plain_password": redpanda_password,
            # "ssl_cafile": "ca.crt",
            # "ssl_certfile": "client.crt",
            # "ssl_keyfile": "client.key"
        }
    )

#
# Create topic
#
# topic_name = os.getenv("REDPANDA_TOPIC_NAME", "test-topic")
# logging.info("Creating topic: %s", topic_name)

admin = AdminClient(conf)
# try:
#     topic = NewTopic(topic=redpanda_topic, num_partitions=1, replication_factor=1)
#     admin.create_topics([topic])
# except KafkaException as e:
#     logging.error(e)

val = Ai()
val.date = '2024-01-26'
val.message = 'Your message'
val.system = 'System X'
val.open = 'Open Y'
val.score = 'Score Z'
val.high = 'High Value'
val.low = 'Low Value'


serialized_val = val.SerializeToString()


registry = SchemaRegistryClient({"url": redpanda_schema_registry})
protobuf_serializer = ProtobufSerializer(
    Ai, registry, {"use.deprecated.format": False}
)
#
# Write to topic
#
def delivery_report(err, msg):
    """Logs the success or failure of message delivery."""
    if err is not None:
        logging.error("Unable to deliver message: %s", err)
    else:
        out = f"topic: {msg.topic()}, "
        out = f"key: {msg.key()}, "
        out += f"partition: {msg.partition()}, "
        out += f"offset: {msg.offset()}, "
        out += f"value: {msg.value()}"
        logging.info(out)

logging.info("Writing to topic: %s", redpanda_topic)
p = Producer(conf)
here = pathlib.Path(__file__).parent.resolve()
logging.info("Processing message: %s", val)

logging.info("Serialized Message: %s", serialized_val)

try:
    p.produce(
        topic= redpanda_topic,
        key="123456",
        value= serialized_val,
        on_delivery=delivery_report,
    )
except KafkaException as e:
    logging.error(e)
p.flush()
