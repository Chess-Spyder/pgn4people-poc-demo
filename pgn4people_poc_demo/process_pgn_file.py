"""
Functions to help parse PGN file of a chess game.
"""

from importlib.resources import files
import logging
import os
import re

from . import constants
from . error_processing import (fatal_error_exit_without_traceback,
                                fatal_pgn_error)
from . jdr_utilities import id_text_between_first_two_blankish_lines
from . strip_balanced_braces import strip_balanced_braces_from_string


def clean_and_parse_string_read_from_file(string_read_from_file):
    """
    Grab the movetext from game #1 by stripping headers and stripping textual annotations; then tokenize that string.
    """

    pgnstring = extract_game_1_movetext(string_read_from_file)

    pgnstring = strip_balanced_braces_from_string(pgnstring)

    if not pgnstring:
        # fatal_pgn_error("No valid movetext found", pgn_source)
        fatal_pgn_error("No valid movetext found")
   
    # Parse string into a list of tokens, either (a) a movetext entry (e.g., "e4"), (b) “(”, or (c) “)”.
    tokenlist = tokenize_pgnstring(pgnstring)

    return tokenlist


def extract_game_1_movetext(string_read_from_file):
    """
    Extracts the movetext from the first game in the string read from the PGN file.
    This text begins immediately following the first blank-ish line (which occurs immediately after
    the headers) and continues until the next blank-ish line (which separates the first game from
    the second) or end of string.
    """
    (start_index, end_index) = id_text_between_first_two_blankish_lines(string_read_from_file)

    if start_index is None:
        pgn_error_no_blank_line_after_headers()
    
    if end_index is None:
        movetext_string = string_read_from_file[start_index::]
    else:
        movetext_string = string_read_from_file[start_index: end_index:]
    
    # Remove any remaining leading white space
    movetext_string = movetext_string.lstrip()

    return movetext_string



def tokenize_pgnstring(pgnstring):
    """
    Parse string into a list of tokens, either a movetext entry (e.g., "Nf3"), “(”, or “)”. Return the list.
    """
    # Bursts the string at each space
    tokenlist = pgnstring.split()

    # Strips any move-number indication (e.g., “2.” or “6...”) from a movetext token that precedes the movetext itself.
    # This skips over tokens that are either “(” or “)”, which are not movetext tokens.
    # for token in tokenlist:
    #    token = strip_leading_movenumber_indication(token)

    # See https://www.geeksforgeeks.org/python-change-list-item/

    tokenlist = [strip_leading_movenumber_indication(token) for token in tokenlist]

    # Removes any empty token
    # See, e.g., https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
    #
    # An empty token can occur, e.g., with the “*” at the end or if a move-number indication is in a separate component
    # of the burst string from its movetext).
    # Note: If the PGN is in “export format,” there will be no space between the move-number indication and the
    # move. In this case, each burst component will have the movenumber and movetext together. 
    # Otherwise, a component may have ONLY the move-text indicator, and this string will be converted to the
    # empty string by strip_leading_movenumber_indication(). This is OK, as empty strings are stripped out.
    #
    # NOTE: An empty string is considered False.
    tokenlist = [token for token in tokenlist if token]

    return tokenlist

def strip_leading_movenumber_indication(string_to_strip):
    """
    Strips leading move-number indication (e.g., “2.” or “4...”) from supplied movetext token. Returns stripped string. 
    """
    # Requirements
    # import re  # Requires re package to be imported by the module.

    # Use regular expression to strip all non-alpha leading characters, except for “(” and “)”, from string.
    # Adapted the answer from https://stackoverflow.com/a/31034061/8401379, which strips non-alphanumeric characters.

    # Compiles pattern
    regex_pattern = re.compile(r"^[^A-Za-z()]+")

    # Finds characters matching pattern and replaces them with null character
    #   See, e.g., https://medium.com/@zohaibshahzadTO/regular-expressions-sub-method-and-verbose-mode-1902cbc0ceef

    stripped_string = regex_pattern.sub("",string_to_strip)

    return stripped_string


def pgn_file_not_found_fatal_error(user_pgn_filepath, original_error_message):
    """
    Called when user-specified file could not be found at path specified in CLI argument. This is a fatal error.
    Program exits with no traceback information.
    """
    basename = user_pgn_filepath.name
    path_fo_file = str(user_pgn_filepath.parent)
    errmsg_list = []
    errmsg_list.append("FileNotFoundError")
    errmsg_list.append("PGN file specified on command line could not be found:\n")
    errmsg_list.append(f"Could not find a file “{basename}” at the user-specified path:\n")
    errmsg_list.append(f"{path_fo_file}\n")
    errmsg_list.append(f"Please try again by calling “{constants.entry_point_name}” with either ")
    errmsg_list.append("(a) a different file path or (b) no argument at all to use a default PGN file.")
    errmsg_list.append(f"\nOriginal error message = “str({original_error_message})”")
    error_message = "".join(errmsg_list)
    fatal_error_exit_without_traceback(error_message)


def pgn_error_no_blank_line_after_headers():
    errmsg_list = []
    errmsg_list.append("No blank line found after headers.\n")
    error_message = "".join(errmsg_list)
    fatal_pgn_error(error_message)