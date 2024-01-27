import os
import logging
import ai_agent_pb2

from dotenv import load_dotenv
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic, KafkaException
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()])

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
    conf.update({
        "security.protocol": kafka_security_protocol,
        "sasl_mechanism": kafka_sasl_mechanism,
        "sasl_plain_username": redpanda_username,
        "sasl_plain_password": redpanda_password,
    })

# Create the Schema Registry Client
try:
    registry = SchemaRegistryClient({"url": redpanda_schema_registry})
    logging.info("Connected to Schema Registry at %s", redpanda_schema_registry)
except Exception as e:
    logging.error("Failed to connect to Schema Registry: %s", str(e))
    raise

# Create the Protobuf Serializer
try:
    protobuf_serializer = ProtobufSerializer(ai_agent_pb2.Ai, registry, {"use.deprecated.format": False})
    logging.info("Protobuf Serializer created")
except Exception as e:
    logging.error("Failed to create Protobuf Serializer: %s", str(e))
    raise

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        logging.error("Unable to deliver message: %s", err)
    else:
        out = f"topic: {msg.topic()}, key: {msg.key()}, partition: {msg.partition()}, offset: {msg.offset()}, value: {msg.value()}"
        logging.info(out)

# Create and populate the Protobuf message
val = ai_agent_pb2.Ai()
val.date = '2024-01-26'
val.message = 'Your message'
val.system = 'System X'
val.open = 'Open Y'
val.score = 'Score Z'
val.high = 'High Value'
val.low = 'Low Value'

# Serialize using ProtobufSerializer
serialized_val = protobuf_serializer(val, SerializationContext(redpanda_topic, MessageField.VALUE))

# Produce the message to Kafka
logging.info("Writing to topic: %s", redpanda_topic)
try:
    producer.produce(topic=redpanda_topic, key="123456", value=serialized_val, on_delivery=delivery_report)
except KafkaException as e:
    logging.error(e)

producer.flush()
