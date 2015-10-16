import json
import random

import flask

import ai
import game

app = flask.Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def hello():
    with open('main.html', 'r') as f:
        return ''.join(f)


@app.route('/logic', methods=['POST'])
def logic():
    raw = flask.request.get_json()
    raw_board = raw['board']
    player = raw['player']

    board = game.HexBoard({
        tuple(json.loads(key)): value
        for key, value in raw_board.iteritems()
    })

    choice = ai.smart_ai(board, player)
    if not choice:
        return 'null'
    return str(list(choice))


if __name__ == '__main__':
    app.run()
