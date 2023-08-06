'''
Created on Jan 6, 2018

@author: khiem

config
<source>
  @type forward
  port 24224
</source>
<match fluentd.test.**>
  @type stdout
</match>

out
2018-01-07T21:24:24+07:00 ina.casp.start: {"to":"userB","from":"userA"}

'''
# from fluent import sender
# from fluent import event
# sender.setup('ina', host='localhost', port=24224)
# event.Event('start', {
#     'time': '2018-01-08 11:25:47',
#     'level': 'INFO',
#     'tag': 'CASP',
#     'message': 'message hello2'
# })


import logging
from fluent import handler

custom_format = {
  'host': '%(hostname)s',
  'where': '%(module)s.%(funcName)s',
  'level': '%(levelname)s',
  'stack_trace': '%(exc_text)s'
}

logging.basicConfig(level=logging.INFO)
l = logging.getLogger('fluent.testing')
h = handler.FluentHandler(
    'ina.casp', host='localhost', port=24224,
    buffer_overflow_handler='overflow_handler'
)
formatter = handler.FluentRecordFormatter(custom_format)
h.setFormatter(formatter)
l.addHandler(h)
l.info("This log entry will be logged with the additional key: message.")
