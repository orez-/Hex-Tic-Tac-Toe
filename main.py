import json
import random

import flask

app = flask.Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def hello():
    with open('main.html', 'r') as f:
        return ''.join(f)


@app.route('/logic', methods=['POST'])
def logic():
    raw_board = flask.request.get_json()

    board = {
        tuple(json.loads(key)): value
        for key, value in raw_board.iteritems()
    }

    CUTOFF = 30
    for _ in xrange(CUTOFF):
        x = random.randint(-2, 2)
        y = random.randint(-2, 2)
        z = -(x + y)
        if abs(z) <= 2 and (x, y, z) not in board:
            break

    return str([x, y, z])


if __name__ == '__main__':
    app.run()
