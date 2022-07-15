"""
Utilities specific to python-chess
"""

import logging

# import chess
import chess.pgn

# from . process_pgn_file import pgn_file_not_found_fatal_error
# from . pgn_tokenizer import PGNTokenizer
from . constants import (
                              MOVETEXT_INDICATOR,
                              NAG_INDICATOR,
                              COMMENT_INDICATOR,
                              OPEN_VARIATION_INDICATOR,
                              CLOSE_VARIATION_INDICATOR,
                              )



def san_from_board_and_move(board, move):
    move_san = board.san(move)
    return move_san


def debug_output_of_tokenized_game(tokenized_game):
    tokenlist = tokenized_game.tokenlist
    length_of_tokenlist = len(tokenlist)
    output_list = []
    string_to_append = ("\nREPORT OF TOKENIZED GAME\n",
                        f"Length of tokenlist: {length_of_tokenlist}\n")
    logging.debug(string_to_append)
    output_list.append(string_to_append)

    if tokenlist:
        for token in tokenlist:
            if token[0] == MOVETEXT_INDICATOR:
                movetext_dict = token[1]
                movetext_san = movetext_dict["san"]
                movetext_lan = movetext_dict["lan"]
                movetext_uci = movetext_dict["uci"]
                string_to_append = f"» {MOVETEXT_INDICATOR} » {movetext_san}, {movetext_lan}, {movetext_uci}\n"
                logging.debug(string_to_append)
                output_list.append(string_to_append)
            elif token[0] in {OPEN_VARIATION_INDICATOR, CLOSE_VARIATION_INDICATOR}:
                string_to_append = f"» VARIATION DELIMITER: {token[0]}\n"
                logging.debug(string_to_append)
                output_list.append(string_to_append)
            else:
                string_to_append = f"» {token[0]} » “{token[1]}”\n"
                logging.debug(string_to_append)
                output_list.append(string_to_append)
        
        string_to_log = "".join(output_list)
        logging.debug(string_to_log)

        
# def print_report_of_repertoire_game(repertoire_game):
#     type_of_repertoire_game = type(repertoire_game)
#     print(f"{type_of_repertoire_game=}")
#     summarize_headers(repertoire_game)
#     print_tokenlist(repertoire_game)


# def summarize_headers(repertoire_game):
#     print("\nHere’s a summary of the headers:")

#     headers = repertoire_game.headers
#     for header in headers:
#         tagname, tagvalue = header
#         print(f"[{tagname}]: {tagvalue}")
#     print(" ")

# def print_tokenlist(repertoire_game):
#     tokenlist = repertoire_game.tokenlist
#     length_of_tokenlist = len(tokenlist)
#     print(f"Length of tokenlist: {length_of_tokenlist}")
#     if tokenlist:
#         for token in tokenlist:
#             # indicator, value_1, *optional_value_2 = token
#             # value_2 = optional_value_2[0] if optional_value_2 else None
#             # print(f"» “{indicator}” » “{value_1}” » “{value_2}”")
        
#             if token[0] == MOVETEXT_INDICATOR:
#                 movetext_san = token[1]
#                 movetext_lan = token[2]
#                 print(f"» {MOVETEXT_INDICATOR} » ({movetext_san}, {movetext_lan})")
#             elif token[0] in {OPEN_VARIATION_INDICATOR, CLOSE_VARIATION_INDICATOR}:
#                 print(f"» VARIATION DELIMITER: {token[0]}")
#             else:
#                 print(f"» {token[0]} » “{token[1]}”")




# def print_report_on_game(some_game):
#     type_of_game = type(some_game)
#     print(f"Type of game: {type_of_game}")
#     print_game_headers(some_game)
#     list_of_names = dir(some_game)
#     for name in list_of_names:
#         print(name)


# def run_board_report_on_list(list_of_fens):
#     divider = chalk.green(20*" *")

#     print(f"\n\n{divider} \n\nNow I will explore a list of positions and analyze them.\n")

#     for fen_position in list_of_fens:
#         board = chess.Board(fen_position)
#         # print_report_of_castling_rights(board)
#         print_board_report(board)

#     print("\nTesting set_fen()…")
#     a_fen = '6k1/2Q5/8/8/8/2B5/5R2/1K6 b - - 0 1'
#     board = chess.Board()
#     board.set_fen(a_fen)
#     print(board)
#     return





# def get_next_parsed_game_from_PGN_file(pgn_filepath):
#     """
    
#     """
#     try:
#         with pgn_filepath.open('r') as pgn_file:
#             parsed_pgn_text_stream = chess.pgn.read_game(pgn_file)
#             return parsed_pgn_text_stream
#     except FileNotFoundError as err:
#         pgn_file_not_found_fatal_error(pgn_filepath, err)


# def print_game_headers(game):
#     """
#     Prints the headers of a game.

#     To be clear, the argument `game` is the parsed game as returned by chess.pgn.read_game()

#     as in:
#         with pgn_filepath.open('r') as pgn_file:
#         parsed_pgn_text_stream = chess.pgn.read_game(pgn_file)
#         return parsed_pgn_text_stream

#         print_game_headers(parsed_pgn_text_stream)
#     """

#     headers = game.headers
#     number_of_headers = len(headers)

#     print(f"The number of header keys is {number_of_headers}.")
#     for header_key in headers:
#         header_value = headers[header_key]
#         print(f"{header_key}: “{header_value}”")
#     print("- - -")


# def print_board_report(board):
#     print(f"\nReport on this board:\n")
#     print(f"The FEN of this board is: {board.fen()}\n")
#     print(f"The 8×8 configuration of this board: \n {board}\n")
#     value_of_board_turn = board.turn
#     player_to_move = "WHITE" if board.turn else "BLACK"
#     print(f"It is {player_to_move}’s move in this position.")
#     report_whether_check_mate_or_stale(board, player_to_move)
#     print_report_of_castling_rights(board)


# def synthesize_castling_rights(board):
#     """
#     Summarize castling rights in the supplied position.
#     """
#     WHITE = chess.WHITE
#     BLACK = chess.BLACK
#     castling_bitboard = board.castling_rights
#     castling_rights_dict = {}
#     for player in [WHITE, BLACK]:
#         can_kingside_castle = board.has_kingside_castling_rights(player)
#         can_queenside_castle = board.has_queenside_castling_rights(player)
#         has_castling_rights = board.has_castling_rights(player)
#         castling_rights_dict[player] = [can_kingside_castle, can_queenside_castle, has_castling_rights]
#     return castling_rights_dict


# def print_report_of_castling_rights(board):
#     WHITE = chess.WHITE
#     BLACK = chess.BLACK
#     castling_rights_dict = synthesize_castling_rights(board)
#     print("\nCastling Rights Report \n")
#     print("Player    K       Q      Has rights")
#     for player in [WHITE, BLACK]:
#         can_kingside_castle = castling_rights_dict[player][0]
#         can_queenside_castle = castling_rights_dict[player][1]
#         has_castling_rights = castling_rights_dict[player][2]
#         print(f" {player}   {can_kingside_castle}  {can_queenside_castle}  {has_castling_rights}")


# def report_whether_check_mate_or_stale(board, player_to_move):
#     def verbal_phrase(logical_flag):
#         verbal_phrase = "IS" if logical_flag else "is NOT"
#         return verbal_phrase

#     # Checks for checkmate
#     is_mate = board.is_checkmate()
#     print(f"{player_to_move} {verbal_phrase(is_mate)} in checkmate.")
#     if is_mate:
#         return

#     # Check for stalemate
#     is_stalemate = board.is_stalemate()
#     print(f"The position {verbal_phrase(is_stalemate)} stalemate.")
#     if is_stalemate:
#         return

#     #Check whether player is in check
#     is_in_check = True if board.is_check() else False
#     print(f"{player_to_move} {verbal_phrase(is_in_check)} in check.")


# def iterate_over_game_tree(node):
#     print("Entering iterate_over_game_tree.")
#     print(f"{node.move=}")
#     if node.is_end():
#         return
#     for child_node in node.variations:
#         iterate_over_game_tree(child_node)


# def progress_through_main_line_of_game(some_game):
#     print("Inside progress_through_main_line_of_game.")
#     mainline_variation = []
#     board = chess.Board()
#     for node in some_game.mainline():
#         move = node.move
#         board.push(move)
#         mainline_variation.append(move)
#         print(f"Adding move {move} at node {node}.")
#         report_on_a_node(board, node)
#     print(f"All done. The mainline variation is: {mainline_variation}")



# def report_on_a_node(board, node):
#     type_of_the_node = type(node)
#     comment = node.comment if node.comment != '' else "❌"
#     starting_comment = node.starting_comment if node.comment != '' else "❌"
#     parent = node.parent if node.parent is not None else "This node has no parent."
#     player_to_move_as_Boolean = board.turn
#     player_to_move_by_name = player_to_move_as_string(player_to_move_as_Boolean)
#     halfmove_number = node.ply()
#     fullmove_number = board.fullmove_number
#     is_terminal_node =  node.is_end()
#     is_start_of_variation = node.starts_variation()
#     is_on_main_line_of_game = node.is_mainline()
#     is_locally_mainline = node.is_main_variation()
#     number_of_variations = len(node.variations)
#     print(f"#: {fullmove_number}; ½#: {halfmove_number}")
#     print("Comments:")
#     print(f"    {comment=}")
#     print(f"    {starting_comment=}")
#     print("")
#     print(board.unicode(), "\n")
#     # print(board)
#     print(f"{type_of_the_node=}")
#     print(f"{player_to_move_by_name=}")
#     print(f"{parent=}")
#     print(f"{is_terminal_node=}")
#     print(f"{is_start_of_variation=}")
#     print(f"{is_on_main_line_of_game=}")
#     print(f"{is_locally_mainline=}")
#     print(f"{number_of_variations=}")
#     if number_of_variations > 0:
#         for count, variation in enumerate(node.variations):
#             print(f"Variation #{count + 1}: {variation}")
    
#     move_stack = board.move_stack
#     type_of_move_stack = type(move_stack)
#     length_of_move_stack = len(move_stack)
#     for count, move in enumerate(move_stack):
#         print(f"Move #{count}: {move}")

#     print(8*"- ", "End of node", 8*"- ", "\n")


# def player_to_move_as_string(player_to_move_as_Boolean):
#     player_to_move_as_string = "WHITE" if player_to_move_as_Boolean else "BLACK"
#     return player_to_move_as_string



