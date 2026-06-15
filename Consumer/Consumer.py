from kafka import KafkaConsumer
import json
import os
from datetime import datetime

consumer = KafkaConsumer(
    'customer_topic',
    'product_topic',
    'order_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

os.makedirs('../data/customer', exist_ok=True)
os.makedirs('../data/product', exist_ok=True)
os.makedirs('../data/order', exist_ok=True)

print("Listening to all topics...")

for message in consumer:

    topic = message.topic
    data = message.value

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    if topic == "customer_topic":

        file_path = f"../data/customer/customer_{timestamp}.json"

    elif topic == "product_topic":

        file_path = f"../data/product/product_{timestamp}.json"

    elif topic == "order_topic":

        file_path = f"../data/order/order_{timestamp}.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved {topic} -> {file_path}")
