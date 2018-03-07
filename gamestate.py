# This is just one possible solution, there are many
# other options that will work just as well or better
from copy import deepcopy

xlim, ylim = 3, 2  # board dimensions


class GameState:
    """ Attributes
    ----------
    _board: list(list)
        Represent the board with a 2d array _board[x][y]
        where open spaces are 0 and closed spaces are 1
        and a coordinate system where [0][0] is the top-
        left corner, and x increases to the right while
        y increases going down (this is an arbitrary
        convention choice -- there are many other options
        that are just as good)

    _parity: bool
        Keep track of active player initiative (which
        player has control to move) where 0 indicates that
        player one has initiative and 1 indicates player two

    _player_locations: list(tuple)
        Keep track of the current location of each player
        on the board where position is encoded by the
        board indices of their last move, e.g., [(0, 0), (1, 0)]
        means player one is at (0, 0) and player two is at (1, 0)
    """

    def __init__(self):
        """ single-underscore prefix on attribute names means
         that the attribute is "private" (Python doesn't truly
         support public/private members, so this is only a
         convention)"""
        self._board = [[0] * ylim for _ in range(xlim)]
        self._board[-1][-1] = 1  # block lower-right corner
        self.active_player = 0
        self._player_locations = [None, None]

    def get_legal_moves(self):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """

        # get the location of the current player
        current_location = self._player_locations[self.active_player]

        # Current location will be None if it's the first move of the game,
        # and if it is the first move of the game, then we can return an
        # empty board provided by _get_blank_space
        if not current_location:
            return self._get_blank_spaces()

        # We've Determined it's not the first move, so we need to compile the
        # available moves into a list, we'll call it Moves
        moves = []

        # Here ar ethe possible relative moves from any squares, think
        # of these as dx, and dy
        rays = [(1,  0), (1, -1), (0, -1),
                (-1, -1), (-1,  0), (-1,  1),
                (0,  1), (1,  1)]

        # we have all the possible potential moves, but some of them may not be
        # valid. for example, we can't move one to the right, if we're already
        # on the space on the right side edge...we need to be smart about what
        # availble moves we can add to our `moves` list.
        for dx, dy in rays:
            x, y = current_location
            # as long as adding the relative moves gives  alegit move,i.e. not
            # (-1, 2)
            while 0 <= x + dx < xlim and 0 <= y + dy < ylim:
                # What would the X and Y be of that new move
                x += dx
                y += dy
                if self._board[x][y]:
                    # If that move is already in the board then break the while
                    # Loop and then try another move
                    break
                else:
                    # if it's legit move that hasn't been made, then we can add
                    # it to the list
                    moves.append((x, y))
        return moves

    def forecast_move(self, move):
        """ Return a new board object with the specified move
        applied to the current game state.

        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
            (e.g., (0, 0) if the active player will move to the
            top-left corner of the board)
        """

        # We shouldnt' forecast the game tree of a move we can't make...
        if move not in self.get_legal_moves():
            raise RuntimeError("Attempted forecast of illegal move")
        # If the move is a legal one, then we'll copy the current board
        newBoard = deepcopy(self)
        # We'll populate our move's square on the new board
        newBoard._board[move[0]][move[1]] = 1
        # Then we'll update the players current position
        newBoard._player_locations[self.active_player] = move
        # Then we'll 'end the players turn' by changing the parity to give the
        # turn to the next player
        newBoard.active_player ^= 1
        # return the new _board
        return newBoard

    def _get_blank_spaces(self):
        """ Return a list of blank spaces on the board."""
        return [(x, y) for y in range(ylim) for x in range(xlim)
                if self._board[x][y] == 0]


def terminal_test(gameState):
    """ Return True if the game is over for the active player
    and False otherwise.
    """
    # Using implicit boolean on the list. If there were no legal Moves
    # for the player then the list would be [] and be implicitly "False"
    # Therefore we can just force the boolean and return true (not) if
    # the list is zero, and thus the game is zero
    return not bool(gameState.get_legal_moves())


def min_value(gameState, depth):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    # We check to see if we're at the end of the game
    # by checking if the player has any remaining moves
    if terminal_test(gameState):
        return 1

    # now we're adding a depth limit!
    if depth <= 0:
        return 0
    # Since we're currently on a min level, we're starting our value out as
    # postive infinity. Any score smaller than that ( a loss ) is preferred
    v = float("inf")
    # Run through all the available nodes from this level
    for move in gameState.get_legal_moves():
        # Then forecast each move to get the score and replace
        # our current score with any smaller one that comes about.
        v = min(v, max_value(gameState.forecast_move(move), depth - 1))
    return v


def max_value(gameState, depth):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    # We check to see if we're at the end of the game
    # by checking if the player has any remaining moves
    if terminal_test(gameState):
        return -1
    # now we're adding a depth limit!
    if depth <= 0:
        return 0
    # Since we're currently on a max level, we're starting our value out as
    # negative infinity. Any score smaller than that ( a loss ) is preferred
    v = float("-inf")
    # Run through all the available nodes from this level
    for move in gameState.get_legal_moves():
        # Then forecast each move to get the score and replace
        # our current score with any larger one that comes about.
        v = max(v, min_value(gameState.forecast_move(move), depth - 1))
    return v


def minimax_decision(gameState, depth):
    """ Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.

    You can ignore the special case of calling this function
    from a terminal state.
    """
    # TODO: Finish this function!
    # This is a max node, so we want to assume the worst we can do is lost (-inf)
    # So we start out with that score and a best_move of none
    best_score = float("-inf")
    best_move = None
    # Let's grab our potential moves and loop through them
    for m in gameState.get_legal_moves():
        # For each possible move, we want to generate it's children nodes'
        # scores and take the minimum value (the mins turn is next)
        v = min_value(gameState.forecast_move(m), depth - 1)
        # If that move's forecasted score is better than our current score
        # expection then we take that for our best score and best move before
        # moving on to the next move or if we're done looping we return that
        # best move
        if v > best_score:
            best_score = v
            best_move = m
    return best_move
