# -*- coding: utf-8 -*-

def _alphabeta(node, depth, player, a=-float('inf'), b=float('inf')):
    if depth == 0 or node.gameover:
        # The multiplier here is technically unnecessary, but adding it
        # makes it favor moves that let it win faster or lose slower.
        return node.heuristic() * (depth + 1), None

    choice = None
    if player:
        v = -float('inf')
        for option in node.options(player):
            alph, _ = _alphabeta(option, depth - 1, not player, a, b)
            if v < alph:
                v = alph
                choice = option.latest_spot
            a = max(a, v)
            if b <= a:
                break
    else:
        v = float('inf')
        for option in node.options(player):
            alph, _ = _alphabeta(option, depth - 1, not player, a, b)
            if v > alph:
                v = alph
                choice = option.latest_spot
            b = min(b, v)
            if b <= a:
                break
    return v, choice


def smart_ai(board, player):
    if board.gameover:
        print "Good game."
        return None

    # Hardcoded response to a strong early opening.
    if len(board.board) == 1:
        x, y, z = next(iter(board.board))
        if {x, y, z} == {-2, 0, 2}:  # Corner
            # Pick a corner 120˚ away, arbitrarily counterclockwise.
            return (z, x, y)

    v, choice = _alphabeta(board, depth=6, player=player)
    if v:
        if (v > 0) == player:
            print "I have you now."
        else:
            print "well done!"
    return choice
