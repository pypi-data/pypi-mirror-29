'''
Created on Oct 16, 2017

@author: khiem
'''
# example_publisher.py
import pika, os, logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL',
    'queue_message://caujhpxa:gOLp-uuHnVfzoXQqKtFPdx2B8yWj46HR@mustang.rmq.cloudamqp.com/caujhpxa'
    )
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
channel = connection.channel()  # start a channel
channel.queue_declare(queue='pdfprocess')  # Declare a queue
logger.info('ddd')
# send a message
channel.basic_publish(exchange='', routing_key='pdfprocess', body='User information')
print ("[x] Message sent to consumer")

if connection.is_open:
    channel.close()
# connection.close()
