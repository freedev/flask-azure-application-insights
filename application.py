# Load libraries
import os
import psutil
import flask
import time
from flask import Flask
from opencensus.ext.azure.log_exporter import AzureLogHandler

# instantiate flask
app = Flask(__name__)

@app.route('/logging', methods=['GET'])
def get_logging():
    logger.info('handling request /logging ' + str(os.getpid()))
    return flask.jsonify({'status': 'ok', 'time': time.time()})

@app.route('/', methods=['GET'])
def get_home():
    logger.info('handling request / ' + str(os.getpid()))
    return 'ok'

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# config_integration.trace_integrations(['logging'])
connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
print(connection_string)
logger = logging.getLogger(__name__)
handler = AzureLogHandler(connection_string=connection_string)
# handler.setFormatter(logging.Formatter('%(traceId)s %(spanId)s %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.info('main process started ' + str(os.getpid()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
