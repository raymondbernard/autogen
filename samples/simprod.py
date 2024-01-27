from confluent_kafka import Producer
import ai_agent_pb2  # Import the generated Protobuf class

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Configure the producer
producer_conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your broker address
}

producer = Producer(producer_conf)

# Create a new Ai message
ai_message = ai_agent_pb2.Ai()
ai_message.date = "2024-01-26"
ai_message.message = "Cosmic3 message"
ai_message.system = "System1"
ai_message.open = "Open"
ai_message.score = "100"
ai_message.high = "200"
ai_message.low = "50"

# Serialize the message
message_bytes = ai_message.SerializeToString()

# Produce the message
producer.produce('ai-topic', key="key2", value=message_bytes, callback=delivery_report)
producer.poll(0)
producer.flush()
