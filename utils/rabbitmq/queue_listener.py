import pika
from database.config import settings


def queue_listener():
    credentials = pika.PlainCredentials(settings.rabbitmq_creds['user_name'], settings.rabbitmq_creds['password'])
    parameters = pika.ConnectionParameters('127.0.0.1',
                                           5672,
                                           '/',
                                           credentials, heartbeat=0,
                                           blocked_connection_timeout=3000)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='error_queue')
    channel.queue_declare(queue='warning_queue')
    channel.queue_declare(queue='info_queue')

    def callback(ch, method, properties, body):
        # ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Received message: {body.decode()}")

    channel.basic_consume(queue='error_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for error messages...')

    channel.basic_consume(queue='warning_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for warning messages...')

    channel.basic_consume(queue='info_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for info messages...')

    channel.start_consuming()


queue_listener()
