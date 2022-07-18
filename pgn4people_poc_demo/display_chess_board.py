"""
Module to display a chess board alongside the variations table.
"""

import logging

import chess

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
                         SVG_BOARD_ORIENTATION_VALUE
                        )
from . utilities import is_white_move

def form_url_for_chessboard_svg(nodedict, node_id_for_board):
    """
    Constructs URL to query backscattering.de to receive SVG chess board
    to display alongisde variations table.

    See https://github.com/niklasf/web-boardimage

    Returns url and the FEN string as a 2-tuple
    """

    board_theme = SVG_BOARD_THEME_PREFIX + SVG_BOARD_THEME_VALUE
    board_size = SVG_BOARD_SIZE_PREFIX + SVG_BOARD_SIZE_VALUE
    use_coordinates = SVG_BOARD_COORDINATES_BOOLEAN_PREFIX + SVG_BOARD_COORDINATES_BOOLEAN_VALUE
    board_orientation = SVG_BOARD_ORIENTATION_PREFIX + SVG_BOARD_ORIENTATION_VALUE

    node_to_display = nodedict[node_id_for_board]

    # Get fen for position
    fen_value = node_to_display.fen
    fen_string = SVG_BOARD_FEN_PREFIX + fen_value

    # Find last move
    choice_id_at_originatingnode = node_to_display.choice_id_at_originatingnode

    if node_id_for_board > 0:
        # A previous node, and therefore a last move, exists
        add_last_move_to_url = True
        id_originating_node = node_to_display.originatingnode_id
        originating_node = nodedict[id_originating_node]

        last_move_edge = originating_node.edgeslist[choice_id_at_originatingnode]
        last_move_as_uci = last_move_edge.movetext_dict["uci"]
        last_move_string = SVG_BOARD_LAST_MOVE_PREFIX + last_move_as_uci
    else:
        add_last_move_to_url = False

    # Get square of king in check
    board = chess.Board(fen_value)
    if board.is_check():
        add_checked_king_to_url = True
        halfmovenumber = node_to_display.halfmovenumber
        if is_white_move(halfmovenumber):
            player = chess.WHITE
        else:
            player = chess.BLACK

        checked_king_square_index = board.king(player)
        checked_king_square_name = chess.square_name(checked_king_square_index)

        checked_url_string = SVG_BOARD_CHECK_PREFIX + checked_king_square_name
    else:
        add_checked_king_to_url = False
        
# Construct URL
    url_to_fetch = (
                    SVG_BOARD_BASE_URL +
                    fen_string + "&" +
                    board_theme + "&" +
                    board_size + "&" +
                    board_orientation + "&" +
                    use_coordinates
                    )

    if add_last_move_to_url:
        url_to_fetch += "&" + last_move_string
    
    if add_checked_king_to_url:
        url_to_fetch += "&" + checked_url_string

    # logging.debug(f"Here’s the URL I computed: {url_to_fetch}")

    return (url_to_fetch, fen_value)
