import json
import random

import flask

import util

app = flask.Flask(__name__)
app.debug = True


class HexBoard(object):
    """
    Immutable game state.
    """
    size = 3

    def __init__(self, board):
        self.board = dict(board)

    def heuristic(self):
        # Higher numbers favor player `True`.
        if self.winning_row:
            # Figure out the winner by getting a value from that row.
            cd, row = self.winning_row
            coord = [0, 0, 0]
            coord[cd] = row
            coord[not cd] = -row
            return 10000 if self.board[tuple(coord)] else -10000
        return 0

    @util.cached_property
    def winning_row(self):
        """
        Tuple of (coordinate, row), where the coordinate is 0, 1, or 2
        representing x, y, or z, respectively, and the row is the value
        of that coordinate type. Eg: if all the coordinates on the board
        where z was 1 were the same color, the winning_row would be
        (2, 1).
        """
        if self.gameover:
            return self.winning_row

    @property
    def gameover(self):
        """
        Boolean value representing if the game has ended or not.

        A game is considered ended if someone has won or there are no
        more legal moves.
        """
        if len(self.board) == len(HexBoard.all_squares):
            # Stalemate
            self.winning_row = None
            return True

        for row in xrange(-HexBoard.size + 1, HexBoard.size):
            for position in xrange(3):
                row_score = abs(sum(
                    player * 2 - 1
                    for coord, player in self.board.iteritems()
                    if coord[position] == row
                ))
                if row_score == HexBoard.size * 2 - 1 - abs(row):
                    # Winner!
                    self.winning_row = (position, row)
                    return True
        return False

    def options(self, player):
        # TODO: order these better?
        options = HexBoard.all_squares - set(self.board)
        for option in options:
            yield self.move(option, player)

    def move(self, option, player):
        hb = HexBoard(self.board)
        hb.board[option] = player
        hb.latest_spot = option
        return hb


_range = xrange(-HexBoard.size + 1, HexBoard.size)
HexBoard.all_squares = frozenset(
    (x, y, -x - y)
    for x in _range
    for y in _range
    if -x - y in _range
)


def alphabeta(node, depth, player, a=-float('inf'), b=float('inf')):
    if depth == 0 or node.gameover:
        # The multiplier here is technically unnecessary, but adding it
        # makes it favor moves that let it win faster or lose slower.
        return node.heuristic() * (depth + 1), None

    choice = None
    if player:
        v = -float('inf')
        for option in node.options(player):
            alph, _ = alphabeta(option, depth - 1, not player, a, b)
            if v < alph:
                v = alph
                choice = option.latest_spot
            a = max(a, v)
            if b <= a:
                break
    else:
        v = float('inf')
        for option in node.options(player):
            alph, _ = alphabeta(option, depth - 1, not player, a, b)
            if v > alph:
                v = alph
                choice = option.latest_spot
            b = min(b, v)
            if b <= a:
                break
    return v, choice


@app.route('/', methods=['GET'])
def hello():
    with open('main.html', 'r') as f:
        return ''.join(f)


@app.route('/logic', methods=['POST'])
def logic():
    raw_board = flask.request.get_json()

    board = HexBoard({
        tuple(json.loads(key)): value
        for key, value in raw_board.iteritems()
    })

    if board.gameover:
        print "Good game."
        return 'null'
    v, choice = alphabeta(board, depth=6, player=True)
    if v:
        if (v > 0) == True:
            print "I have you now."
        else:
            print "well done!"
    return str(list(choice))


if __name__ == '__main__':
    app.run()
