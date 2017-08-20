import os
import json
import random
import string
from datetime import datetime
from flask import Flask, make_response, jsonify, request
from livereload import Server


CONFIG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'config.json'
)


def read_config():
    with open(CONFIG_FILE_PATH, 'r') as f:
        return json.load(f)


def write_config(new_config):
    with open(CONFIG_FILE_PATH, 'w') as f:
        f.write(json.dumps(new_config, indent=4))


def generate_token(last_token):
    return ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        ) for _ in range(32)
    )


config = read_config()

app = Flask(__name__)
app.debug = config.get('debug', False)

@app.route('/status', methods=['POST'])
def status():
    try:
        last_token = request.form['token']
    except KeyError:
        return make_response(
            jsonify({
                'status': 'Token not sent'
            }),
            403
        )

    config = read_config()
    if config['last_token'] == last_token:
        config['last_token'] = generate_token(last_token)
        config['last_called_at'] = datetime.utcnow().isoformat()
        write_config(config)

        return make_response(
            jsonify({
                'status': 'OK',
                'next_token': config['last_token']
            }),
            200
        )
    else:
        return make_response(
            jsonify({
                'status': 'Token does not match'
            }),
            403
        )

if __name__ == "__main__":
    if config.get('debug', False):
        server = Server(app.wsgi_app)
        server.serve()
    else:
        app.run()
