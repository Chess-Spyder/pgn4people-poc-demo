"""
Defines
• the class TokenizedGame, which is the data structure to hold the
tokenized form of a PGN game/repertoire.
• the custom visitor class PGNTokenizer, which traverses the PGN,
harvests each element, and inserts it appropriately into an instance of
TokenizedGame.
"""
from chess.pgn import BaseVisitor
from . constants import (
                         MOVETEXT_INDICATOR,
                         NAG_INDICATOR,
                         COMMENT_INDICATOR,
                         OPEN_VARIATION_INDICATOR,
                         CLOSE_VARIATION_INDICATOR,
                         )


class TokenizedGame():
    """
    Class for data structure to hold the tokenized form of a PGN game/repertoire.

    self.headers is a list of (tag_name, tag_value) tuples.

    self.tokenlist is a list of tokens, ordered in the same order their corresponding elements are encountered linearly
    reading the PGN file.

    Each token is represented as either a 1-tuple, 2-tuple, or a 3-tuple, based on what type of token it is.
    
    In all cases, the first element of the token’s tuple is an indicator identifying the type of token this is, in order
    to correctly interpret the remaining components. See constants.py (MOVETEXT_INDICATOR, NAG_INDICATOR,
    COMMENT_INDICATOR, OPEN_VARIATION_INDICATOR, CLOSE_VARIATION_INDICATOR,)

    There are 5 types of tokens:
        “(”: open a new variation (or subvariation)
            A 1-tuple
            #1: OPEN_VARIATION_INDICATOR
        “)”: end a variation
            A 1-tuple
            #1: CLOSE_VARIATION_INDICATOR
        Movetext: A movetext token; a 2-tuple, including a dictionary of alternative text representations of the move.
            #1: MOVETEXT_INDICATOR
            #2: A dictionary
                "san": SAN, e.g., “Nf3”
                "lan": LAN, e.g., “Ng1-f3”

        Comment: A textual annotation string (not to be confused with a PGN comment that is NOT part of the 
            PGN, i.e., lines which start with “%” or anything after a “;”)
            A 2-tuple
            #1: COMMENT_INDICATOR
            #2: Comment string (i.e., the text between the “{” and “}” in the PGN, but not including those curly 
                braces)
        NAG: A numeric annotation glyphs
            A 2-tuple
            #1: NAG_INDICATOR
            #2: An integer, e.g., 1, such that $1 corresponds to a valid NAG
    """

    def __init__(self):
        self.headers = []
        self.tokenlist = []


class PGNTokenizer(BaseVisitor):
    """
    Custom visitor to be used in conjunction with chess.pgn.read_game(), replacing the default visitor (viz., 
    chess.pgn.GameBuilder).

    Instantiates an instance of TokenizedGame to store the tokens that will be harvested from the PGN as
    chess.pgn.read_game(), in conjunction with PGNTokenizer, scans the PGN file.
    """

    def __init__(self):
        # I don’t understand the following construction (referring to both this constructor as well as the begin_game()
        # method), but I’m mimicking the constructor from chess.pgn.GameBuilder
        #   self.Game = Game
        # where I assume the r.h.s. mention of “Game” references the Game class, but then I would’ve expected
        # “Game()”, not “Game”.
        self.TokenizedGame = TokenizedGame()


    def begin_game(self):
        # This too (i.e., in conjunction with the __init__ for MyCustomVisitor) follows the model in
        # chess.pgn.GameBuilder, which I don’t understand.
        self.tokenized_game = self.TokenizedGame


    def begin_headers(self):
        self.tokenized_game.headers = []
        return

    
    def visit_header(self, tagname, tagvalue):
        """
        Receives each header from read_game() and stores it in the list `headers`.
        """

        header = (tagname, tagvalue)
        self.tokenized_game.headers.append(header)


    def begin_variation(self):
        token_to_append = (OPEN_VARIATION_INDICATOR, "")
        self.tokenized_game.tokenlist.append(token_to_append)


    def end_variation(self):
        token_to_append = (CLOSE_VARIATION_INDICATOR, "")
        self.tokenized_game.tokenlist.append(token_to_append)


    def visit_move(self, board_stack_last_item, move):
        """
        Visitor to receive board/move combinations from chess.pgn.read_game()

        I use the board_stack_last_item only for converting the move into SAN and LAN representations.
        I pass along only these two representations of the move.

        Returns a token that is a 2-tuple:
            #1: MOVETEXT_INDICATOR, e.g., “<M>”, signalling that this token is a movetext token
            #2: a dictionary of alternative text representations of the move.
                "san": SAN, e.g., “Nf3”
                "lan": LAN, e.g., “Ng1-f3”
                "uci": UCI, e.g., "g1f3"

        """
        # print(board_stack_last_item)
        move_san = board_stack_last_item.san(move)
        move_lan = board_stack_last_item.lan(move)
        move_uci = board_stack_last_item.uci(move)
        # print(f"{move_san=}, {move_lan=}")
        # This caused a circular import
        # move_san = san_from_board_and_move(board_stack_last_item, move)

        # token_to_append = (MOVETEXT_INDICATOR, move_san, move_lan)
        token_to_append = (MOVETEXT_INDICATOR, {"san": move_san, "lan": move_lan, "uci": move_uci})
        self.tokenized_game.tokenlist.append(token_to_append)
    

    def visit_nag(self, nag):
        token_to_append = (NAG_INDICATOR, nag)
        self.tokenized_game.tokenlist.append(token_to_append)


    def visit_comment(self, comment):
        token_to_append = (COMMENT_INDICATOR, comment)
        self.tokenized_game.tokenlist.append(token_to_append)


    def result(self):
        # This is the only @abc.abstractmethod in BaseVisitor
        return self.tokenized_game