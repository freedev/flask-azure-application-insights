# Load libraries
import os
import flask
import time
from flask import Flask
from opencensus.ext.azure.log_exporter import AzureLogHandler

# instantiate flask
app = Flask(__name__)

@app.route('/logging', methods=['GET'])
def get_logging():
    getLogger().info('handling request /logging ' + str(os.getpid()))
    return flask.jsonify({'status': 'ok', 'time': time.time(), 'pid': os.getpid()})


@app.route('/', methods=['GET'])
def get_home():
    getLogger().info('handling request / ' + str(os.getpid()))
    return 'ok'

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# config_integration.trace_integrations(['logging'])
connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
print(connection_string)
def getLogger():
    global logger
    try:
        if logger[os.getpid()] is not None:
            print("returning existing logger " + str([os.getpid()]))
            return logger[os.getpid()]
    except:
        try:
            if logger is not None:
                print('logger not empty')
        except:
            logger = {}
            # root_logger = logging.getLogger()
            # handler = AzureLogHandler(connection_string=connection_string)
            # root_logger.addHandler(handler)
            # handler.setLevel(logging.INFO)
            # print("added AzureLogHandler handler for pid " + str([os.getpid()]))
        try:
            if logger[os.getpid()] is not None:
                print('logger for pid found')
        except:
            logger[os.getpid()] = logging.getLogger(str(os.getpid()))
            print(connection_string)
            handler = AzureLogHandler(connection_string=connection_string)
            logger[os.getpid()].addHandler(handler)
            handler.setLevel(logging.INFO)
            print("created logger for pid " + str([os.getpid()]))
        # handler.setFormatter(logging.Formatter('%(traceId)s %(spanId)s %(message)s'))
    return logger[os.getpid()]

getLogger().info('process started ' + str(os.getpid()) + ' home 2')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
