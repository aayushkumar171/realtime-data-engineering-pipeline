from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_customer(data):
    producer.send('customer_topic', value=data)
    producer.flush()


def send_product(data):
    producer.send('product_topic', value=data)
    producer.flush()
    
def send_order(data):
    producer.send('order_topic', value=data)
    producer.flush()