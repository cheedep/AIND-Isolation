"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
from math import sqrt
from random import randint


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    return float(len(own_moves)/len(opp_moves))

def custom_score1(game, player):
    #Heuristic based only on own moves
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    return float(len(own_moves))

def custom_score2(game, player):
    #Heuristic trying to follow the center and the opponent
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    c = game.width//2, game.height//2
    p = game.get_player_location(player)

    if c in game.get_blank_spaces():
        dist = sqrt((c[0]-p[0])**2 + (c[1]-p[1])**2)
    else:
        p1 = game.get_player_location(game.get_opponent(player))
        dist = sqrt((p1[0] - p[0])**2 + (p1[1]-p[1])**2)
    return float(len(own_moves) - len(opp_moves) - dist)

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        if len(legal_moves) ==0:
            return -1, -1

        center = (game.width - 1)//2, (game.height - 1)//2
        best_move = center if center in legal_moves else legal_moves[randint(0, len(legal_moves) - 1)]

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            start_depth = 1 if self.iterative else self.search_depth
            end_depth = (game.height * game.width) // 2 if self.iterative else self.search_depth + 1

            if self.method == "minimax":
                for depth in range(start_depth, end_depth):
                    best_move = self.minimax(game, depth)[1]
                return best_move
            for depth in range(start_depth, end_depth):
                best_move = self.alphabeta(game, 1)[1]
                return best_move

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        legalmoves = game.get_legal_moves(self) if maximizing_player else game.get_legal_moves(game.get_opponent(self))

        #print(depth, legalmoves)

        if(len(legalmoves) == 0):
            return float("-inf") if maximizing_player else float("inf"), (-1, -1)

        scoresformoves = [(self.score(game.forecast_move(x), self) if depth == 1 else self.minimax(game.forecast_move(x), depth - 1, not maximizing_player)[0],x) for x in legalmoves]

        if(maximizing_player):
            return max(scoresformoves,key=lambda x:x[0])
        else:
            return min(scoresformoves, key=lambda x:x[0])

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        legalmoves = game.get_legal_moves(self) if maximizing_player else game.get_legal_moves(game.get_opponent(self))

        #print(depth, legalmoves)

        if (len(legalmoves) == 0):
            return float("-inf") if maximizing_player else float("inf"), (-1, -1)

        if maximizing_player:
            v = (float("-inf"), (-1, -1))
            for x in legalmoves:
                z = (self.score(game.forecast_move(x), self) if depth == 1 else self.alphabeta(game.forecast_move(x), depth - 1, alpha, beta, not maximizing_player)[0], x)
                v = max([v, z], key=lambda y: y[0])
                alpha = max(alpha, v[0])
                if beta <= alpha:
                    break
            return v
        else:
           v = (float("inf"), (-1, -1))
           for x in legalmoves:
               z = (self.score(game.forecast_move(x), self) if depth == 1 else self.alphabeta(game.forecast_move(x), depth - 1, alpha, beta, not maximizing_player)[0], x)
               v = min([v,  z], key=lambda y: y[0])
               beta = min(beta, v[0])
               if beta <= alpha:
                   break
           return v
