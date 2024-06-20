import pika
from database.config import settings


def queue_producer():
    credentials = pika.PlainCredentials(settings.rabbitmq_creds['user_name'], settings.rabbitmq_creds['password'])
    parameters = pika.ConnectionParameters('127.0.0.1',
                                           5672,
                                           '/',
                                           credentials, heartbeat=0,
                                           blocked_connection_timeout=3000)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='logs_exchange', exchange_type='topic')

    channel.queue_declare(queue='error_queue')
    channel.queue_declare(queue='warning_queue')
    channel.queue_declare(queue='info_queue')

    channel.queue_bind(exchange='logs_exchange', queue='error_queue', routing_key='error')
    channel.queue_bind(exchange='logs_exchange', queue='warning_queue', routing_key='warning')
    channel.queue_bind(exchange='logs_exchange', queue='info_queue', routing_key='info')

    log_messages = [
        {'severity': 'error', 'message': 'Critical error occurred!'},
        {'severity': 'warning', 'message': 'Possible issue detected.'},
        {'severity': 'info', 'message': 'System status: OK'},
    ]

    for log in log_messages:
        channel.basic_publish(exchange='logs_exchange', routing_key=log['severity'], body=log['message'])
        print(f"Sent '{log['severity']}' log message: {log['message']}")
    channel.close()


queue_producer()
