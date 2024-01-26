import os
import csv
import glob
import logging
import pathlib

from dotenv import load_dotenv
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic, KafkaException

load_dotenv()
logging.basicConfig(level=logging.INFO)

redpanda_brokers = os.getenv("REDPANDA_BROKERS")
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

mess = 'cosmic test'

#
# Write to topic
#
def delivery_report(err, msg):
    """Logs the success or failure of message delivery."""
    if err is not None:
        logging.error("Unable to deliver message: %s", err)
    else:
        out = f"topic: {msg.topic()}, "
        out += f"partition: {msg.partition()}, "
        out += f"offset: {msg.offset()}, "
        out += f"value: {msg.value()}"
        logging.info(out)

logging.info("Writing to topic: %s", 'ai')
p = Producer(conf)
here = pathlib.Path(__file__).parent.resolve()
logging.info("Processing message: %s", mess)

val = mess
try:
    p.produce(
        topic='ai',
        key="123",
        value=val.encode("utf-8"),
        on_delivery=delivery_report,
    )
except KafkaException as e:
    logging.error(e)
p.flush()
