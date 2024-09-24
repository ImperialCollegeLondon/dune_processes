"""Example client that consumes messages from Kafka and sends them to the web app."""

import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from druncschema.broadcast_pb2 import BroadcastMessage
from kafka import KafkaConsumer

KAFKA_URL = os.getenv("KAFKA_URL", "127.0.0.1:30092")
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")


def main() -> None:
    """Listen for Kafka messages and process them indefinitely."""
    consumer = KafkaConsumer(bootstrap_servers=[KAFKA_URL])
    consumer.subscribe(pattern="control.*.process_manager")

    print("Listening for messages from Kafka.")
    while True:
        for messages in consumer.poll(timeout_ms=500).values():
            for message in messages:
                print(f"Message received: {message}")
                bm = BroadcastMessage()
                bm.ParseFromString(message.value)

                data = urlencode(dict(message=bm.data.value))
                request = Request(f"{SERVER_URL}/message/", data=data.encode())
                urlopen(request)


if __name__ == "__main__":
    main()
