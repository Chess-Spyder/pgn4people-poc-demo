"""
Module to display a chess board alongside the variations table.
"""

import logging

import chess
import chess.svg

from pgn4people_poc_demo.error_processing import fatal_error_exit_without_traceback

from . constants import (SVG_BOARD_BASE_URL,
                         SVG_BOARD_THEME_PREFIX,
                         SVG_BOARD_SIZE_PREFIX,
                         SVG_BOARD_COORDINATES_BOOLEAN_PREFIX,
                         SVG_BOARD_ORIENTATION_PREFIX,
                         SVG_BOARD_FEN_PREFIX,
                         SVG_BOARD_LAST_MOVE_PREFIX,
                         SVG_BOARD_CHECK_PREFIX,
                         SVG_BOARD_THEME_VALUE,
                         SVG_BOARD_SIZE_VALUE,
                         SVG_BOARD_COORDINATES_BOOLEAN_VALUE,
                         SVG_BOARD_ORIENTATION_VALUE,
                         SVG_BOARD_USE_WEB_SERVICE
                        )
from . utilities import is_white_move

def compile_parameters_for_chessboard_svg(nodedict, node_id_for_board):
    """
    Compile parameters to be used for chessboard svg, whether for (a) URL from 
    web service or (b) chess.pgn svg output.

    Returns those parameters as an instance of class SVGChessBoardParameters.
    """

    parameters_for_svg_chess_board = SVGChessBoardParameters()

    node_to_display = nodedict[node_id_for_board]

    # Get fen for position
    fen_value = node_to_display.fen
    parameters_for_svg_chess_board.fen_value = fen_value

    # Find last move
    choice_id_at_originatingnode = node_to_display.choice_id_at_originatingnode

    if node_id_for_board > 0:
        # A previous node, and therefore a last move, exists
        do_highlight_last_move = True

        id_originating_node = node_to_display.originatingnode_id
        originating_node = nodedict[id_originating_node]

        last_move_edge = originating_node.edgeslist[choice_id_at_originatingnode]
        last_move_as_uci = last_move_edge.movetext_dict["uci"]

        parameters_for_svg_chess_board.last_move_as_uci = last_move_as_uci

    else:
        do_highlight_last_move = False
    
    parameters_for_svg_chess_board.do_highlight_last_move = do_highlight_last_move

    # Get square of king in check
    board = chess.Board(fen_value)
    if board.is_check():
        king_is_in_check = True

        # Finds square of player-to-move’s King
        halfmovenumber = node_to_display.halfmovenumber
        if is_white_move(halfmovenumber):
            player_to_move = chess.WHITE
        else:
            player_to_move = chess.BLACK

        checked_king_square_index = board.king(player_to_move)
        checked_king_square_name = chess.square_name(checked_king_square_index)

        parameters_for_svg_chess_board.checked_king_square_name = checked_king_square_name

    else:
        king_is_in_check = False
    
    parameters_for_svg_chess_board.king_is_in_check = king_is_in_check
    
    return parameters_for_svg_chess_board


def construct_svg_chessboard(parameters):
    """
    Construct SVG of chessboard using chess.svg.board method
    """
    board_from_fen = chess.Board(parameters.fen_value)

    def orientation_for_chess_svg_board_from_player_color_string(player_color_string):
        """
        Converts player_color_string (e.g., “wHItE” or “blaCk”) to chess.WHITE
        or chess.BLACK, respectively for use as the `orientation` argument to the
        web-boardimage HTTP service <backscattering.de/web-boardimage> to
        render chess board images.
        """
        lowercased_player_color_string = player_color_string.lower()
        if lowercased_player_color_string == 'white':
            orientation_value = chess.WHITE
        elif lowercased_player_color_string == 'black':
            orientation_value = chess.BLACK
        else: 
            fatal_error_exit_without_traceback(f"Unrecognized value for orientation: {player_color_string}")
        
        return orientation_value

    orientation_value = orientation_for_chess_svg_board_from_player_color_string(parameters.board_orientation)

    if parameters.do_highlight_last_move:
        last_move_to_highlight = chess.Move.from_uci(parameters.last_move_as_uci)
    else:
        last_move_to_highlight = None

    board_as_svg_string = chess.svg.board(board_from_fen,
                                          size = parameters.board_size,
                                          orientation = orientation_value,
                                          coordinates = parameters.use_coordinates,
                                          lastmove = last_move_to_highlight,
                                          check = parameters.checked_king_square_name
                                          )
    
    return board_as_svg_string


# def form_url_for_chessboard_svg(nodedict, node_id_for_board):
def form_url_for_chessboard_svg(parameters):
    """
    Constructs URL to query backscattering.de to receive SVG chess board
    to display alongisde variations table.

    See https://github.com/niklasf/web-boardimage

    Returns URL
    """

    def javascript_boolean_string_from_python_boolean(python_boolean):
        return "true" if python_boolean else "false"
    
    use_coordinates_js = javascript_boolean_string_from_python_boolean(parameters.use_coordinates)

    def SVG_orientation_backscattering_de_from_player_color_string(player_color_string):
        """
        Converts player_color_string (e.g., “wHItE” or “blaCk”) to “white” or
        “black”, respectively, for use as the `orientation` argument to the
        web-boardimage HTTP service <backscattering.de/web-boardimage> to
        render chess board images.
        """
        lowercased_player_color_string = player_color_string.lower()
        return lowercased_player_color_string
    
    orientation_value = SVG_orientation_backscattering_de_from_player_color_string(parameters.board_orientation)

    board_theme = SVG_BOARD_THEME_PREFIX + parameters.board_theme
    board_orientation = SVG_BOARD_ORIENTATION_PREFIX + orientation_value
    board_size = SVG_BOARD_SIZE_PREFIX + parameters.board_size
    # use_coordinates = SVG_BOARD_COORDINATES_BOOLEAN_PREFIX + parameters.use_coordinates
    use_coordinates = SVG_BOARD_COORDINATES_BOOLEAN_PREFIX + use_coordinates_js
    
    fen_string = SVG_BOARD_FEN_PREFIX + parameters.fen_value

    # Construct URL
    url_to_fetch = (
                    SVG_BOARD_BASE_URL +
                    fen_string + "&" +
                    board_theme + "&" +
                    board_size + "&" +
                    board_orientation + "&" +
                    use_coordinates
                    )

    if parameters.do_highlight_last_move:
        last_move_string = SVG_BOARD_LAST_MOVE_PREFIX + parameters.last_move_as_uci
        url_to_fetch += "&" + last_move_string
    
    if parameters.king_is_in_check:
        checked_url_string = SVG_BOARD_CHECK_PREFIX + parameters.checked_king_square_name
        url_to_fetch += "&" + checked_url_string

    return url_to_fetch


class SVGChessBoardParameters():
    """
    Class to hold the set of parameters used for constucting an SVG chessboard
    """

    __slots__ = {
        # Immediately following attributes are supplied default values at time of instantiation"
        "board_orientation":
            "Which player color’s first rank is at the bottom of the board",
        "use_coordinates":
            "Boolean: True => use coordinates",
        "board_size":
            "Board size in pixels",
        "board_theme":
            "Name of board theme. Applies to backscattering.de but not chess.svg",
        # Remaining attributes are assigned values after instantiation
        "fen_value":
            "FEN string to represent via the SVG board",
        "do_highlight_last_move":
            "Boolean: True => Highlight the last move",
        "last_move_as_uci":
            "String of last move as UCI for highlighting the last move",
        "king_is_in_check":
            "Boolean: True => The king of player to move is in check",
        "checked_king_square_name":
            "Name of square on which the checked King resides",
    }

    def __init__(self, *,
                 board_orientation = SVG_BOARD_ORIENTATION_VALUE,
                 use_coordinates = SVG_BOARD_COORDINATES_BOOLEAN_VALUE,
                 board_size = SVG_BOARD_SIZE_VALUE,
                 board_theme = SVG_BOARD_THEME_VALUE,
                 do_highlight_last_move = False,
                 last_move_as_uci = None,
                 king_is_in_check = False ,
                 checked_king_square_name = None,
                 ):
                 self.board_orientation = board_orientation
                 self.use_coordinates = use_coordinates
                 self.board_size = board_size
                 self.board_theme = board_theme
                 self.do_highlight_last_move = do_highlight_last_move
                 self.last_move_as_uci = last_move_as_uci
                 self.king_is_in_check = king_is_in_check
                 self.checked_king_square_name = checked_king_square_name
    


