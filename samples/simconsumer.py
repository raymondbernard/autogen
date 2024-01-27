from confluent_kafka import Consumer, KafkaError
import ai_agent_pb2  # Import the generated Protobuf class

# Configure the consumer
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your broker address
    'group.id': '123',  # Replace with your group ID
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe(['ai-topic'])

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Deserialize the message
        ai_message = ai_agent_pb2.Ai()
        ai_message.ParseFromString(msg.value())

        print(f"Received message: {ai_message}")

finally:
    consumer.close()
