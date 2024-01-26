from confluent_kafka import Consumer, KafkaException

c = Consumer({
    'bootstrap.servers': '<your_redpanda_server>',
    'group.id': '<group_id>',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['<your_topic_name>'])

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            print('Received message: {}'.format(msg.value().decode('utf-8')))

except KeyboardInterrupt:
    pass

finally:
    c.close()