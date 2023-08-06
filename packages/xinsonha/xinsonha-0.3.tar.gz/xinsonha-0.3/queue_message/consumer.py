'''
Created on Oct 16, 2017

@author: khiem
'''
# example_consumer.py
import pika, os, time

def pdf_process_function(msg):
    print(" PDF processing")
    print(" Received %r" % msg)

    time.sleep(5)  # delays for 5 seconds
    print(" PDF processing finished")

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL',
    'queue_message://cfpzarme:MqsdI8OBcuTy_C1C1JP1B2a8APAWQzf1@mustang.rmq.cloudamqp.com/cfpzarme'
    )

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel
channel.queue_declare(queue='pdfprocess')  # Declare a queue

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    pdf_process_function(body)

# set up subscription on the queue
# channel.basic_consume(callback, queue='pdfprocess', no_ack=True)
print channel.basic_get(queue='ina_casp_service_listen1', no_ack=False)

# start consuming (blocks)
channel.start_consuming()
connection.close()
