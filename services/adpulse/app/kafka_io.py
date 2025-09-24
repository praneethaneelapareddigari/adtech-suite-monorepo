import os, json, asyncio
from aiokafka import AIOKafkaProducer

KAFKA_BROKER = os.getenv("KAFKA_BROKER","kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC","ad_events")

_producer = None

async def get_producer():
    global _producer
    if _producer is None:
        _producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER,
                                     value_serializer=lambda v: json.dumps(v).encode())
        await _producer.start()
    return _producer

async def publish(event: dict):
    producer = await get_producer()
    await producer.send_and_wait(KAFKA_TOPIC, event)

async def close():
    if _producer:
        await _producer.stop()