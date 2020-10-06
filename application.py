# Load libraries
import os
import flask
import time
from flask import Flask
from opencensus.ext.azure.log_exporter import AzureLogHandler

threads_num = os.getenv('GU_THREADS_NUM')
work_num = os.getenv('GU_WORK_NUM')

# instantiate flask
app = Flask(__name__)

@app.route('/logging', methods=['GET'])
def get_logging():
    message = 'handling request /logging with pid %s threads %s workers %s' % (str(os.getpid()), threads_num, work_num)
    getLogger().info(message)
    return flask.jsonify({'status': 'ok', 'time': time.time(), 'pid': os.getpid(), 'threads_num': threads_num , 'work_num': work_num})

@app.route('/', methods=['GET'])
def get_home():
    message = 'handling request / with pid %s threads %s workers %s' % (str(os.getpid()), threads_num, work_num)
    getLogger().info(message)
    return 'ok'

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
logger={}

# config_integration.trace_integrations(['logging'])
connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
print(connection_string)

def getLogger():
    global logger
    try:
        if logger[str(os.getpid())] is not None:
            print("returning existing logger " + str([os.getpid()]))
            return logger[os.getpid()]
    except:
        logger[os.getpid()] = logging.getLogger(str(os.getpid()))
        print(connection_string)
        handler = AzureLogHandler(connection_string=connection_string)
        logger[os.getpid()].addHandler(handler)
        logger[os.getpid()].setLevel(logging.INFO)
        print("created logger for pid " + str([os.getpid()]))
    return logger[os.getpid()]

print(os.getpid())
getLogger().info('process started ' + str(os.getpid()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
