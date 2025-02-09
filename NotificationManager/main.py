import argparse
import threading
import pika
import psycopg2
import redis
from notificationmanager.models import RtmqParams, RedisParams
from notificationmanager.rabbitmq import rabbitmq_consume, setup_rabbitmq


def parse_arguments():
    parser = argparse.ArgumentParser(description="Configure RabbitMQ, Redis, and Postgres parameters.")

    # RabbitMQ arguments
    parser.add_argument('--rabbitmq-host', default='rabbitmq', help='RabbitMQ host')
    parser.add_argument('--rabbitmq-log-queue', default='log_queue', help='RabbitMQ log queue')
    parser.add_argument('--rabbitmq-log-exchange', default='log_exchange', help='RabbitMQ log exchange')
    parser.add_argument('--rabbitmq-log-key', default='log_routing_key', help='RabbitMQ log routing key')
    parser.add_argument('--rabbitmq-user', default='ing3', help='RabbitMQ user')
    parser.add_argument('--rabbitmq-pass', default='paas', help='RabbitMQ password')

    # Redis arguments
    parser.add_argument('--redis-host', default='redis', help='Redis host')
    parser.add_argument('--redis-port', type=int, default=6379, help='Redis port')
    parser.add_argument('--redis-pass', default='', help='Redis password')

    # Postgres arguments (if needed in future)
    parser.add_argument('--postgres-host', default='postgres', help='Postgres host')
    parser.add_argument('--postgres-db', default='house_config', help='Postgres database')
    parser.add_argument('--postgres-user', default='postgres', help='Postgres user')
    parser.add_argument('--postgres-pass', default='admin', help='Postgres password')
    parser.add_argument('--postgres-port', type=int, default=5432, help='Postgres port')

    return parser.parse_args()


def rabbitmq_consumer(rabbitmq_host, rabbitmq_log_exchange, rabbitmq_log_queue, rabbitmq_log_key, rabbitmq_user,
                      rabbitmq_pass, redis_host, redis_port):
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    connection = setup_rabbitmq(host=rabbitmq_host, credentials=credentials)
    cons_channel = connection.channel()
    postgres_connection = psycopg2.connect(dbname=args.postgres_db, user=args.postgres_user,
                                           password=args.postgres_pass, host=args.postgres_host,
                                           port=args.postgres_port)

    redis_params = RedisParams(host=redis_host, port=redis_port)
    rtmq_cons_params = RtmqParams(channel=cons_channel, exchange=rabbitmq_log_exchange, queue=rabbitmq_log_queue,
                                  key=rabbitmq_log_key)
    rabbitmq_consume(params=rtmq_cons_params, redis=redis_params, postgres=postgres_connection)


if __name__ == "__main__":
    args = parse_arguments()

    threading.Thread(target=rabbitmq_consumer, args=(
        args.rabbitmq_host, args.rabbitmq_log_exchange, args.rabbitmq_log_queue,
        args.rabbitmq_log_key, args.rabbitmq_user, args.rabbitmq_pass,
        args.redis_host, args.redis_port
    )).start()
