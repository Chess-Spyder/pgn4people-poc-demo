"""
Constants to essentially be available globally.
"""

import logging

# Logging related
LOGGING_LEVEL=logging.DEBUG
LOG_FILE_NAME="logfile.log"
LOGGING_FORMAT='%(name)s - %(levelname)s - %(message)s'

#   CONSTANTS RELATED TO PROJECT NAMES AND FILE LOCATIONS

# NAME_OF_IMPORT_PACKAGE = "pgn4people_poc_demo"

# Name of directory of sample PGNs
DIRNAME_SAMPLE_PGNS = "static/data/"

# Computes package entity from which sample PGN can be read
# (The sample PGN(s) are in a subpackage of the import package.)
# PACKAGE_FOR_SAMPLE_PGN = NAME_OF_IMPORT_PACKAGE + "." + DIRNAME_SAMPLE_PGNS

# Names of sample PGN files
PGNFILE1 = "demo_pgn_1.pgn"

# Chosen sample PGN file to analyze; used for both (a) filesystem and (b) resource locations of the file
CHOSEN_SAMPLE_PGN_FILE = PGNFILE1

# Path of sample PGN file
PATH_OF_PGN_FILE = DIRNAME_SAMPLE_PGNS + CHOSEN_SAMPLE_PGN_FILE

# Descriptor presented when sample PGN is chosen
# PUBLIC_BASENAME_SAMPLE_PGN = f"Built-in sample PGN: {CHOSEN_SAMPLE_PGN_FILE}"
# VERSION_SAMPLE_PGN = "1.0.0"

# Constants defining the designator for each type of token in the tokenized form of a PGN game
# Each is returned as the first element of each token, informing the consumer how the remainder of
# the token should be interpreted.
MOVETEXT_INDICATOR = "<M>"
NAG_INDICATOR = "<N>"
COMMENT_INDICATOR = "<C>"
OPEN_VARIATION_INDICATOR = "<(>"
CLOSE_VARIATION_INDICATOR = "<)>"

# ARBOREAL CONSTANTS

UNDEFINED_TREEISH_VALUE = -1
NODE_IS_TERMINAL_NODE = -1

INITIAL_NODE_ID = 0

# The choice_id at a node that corresponds to the main line.
INDEX_MAINLINE = 0

# Options for formatting of variations table

# Whether to preface Black alternative halfmoves with ellipses (“…”)
# do_ellipcize_Black_alternatives = True

# Note: (a) BLACK_MOVE_PREFIX is a true ellipsis to economize on space but (b) BLACK_MOVE_DEFERRED and
# WHITE_MOVE_ELLIPSIS are more spacious because each needs to span an entire movetext element of a White/Black move,
# respectively.
WHITE_MOVE_ELLIPSIS = ". . . "
BLACK_MOVE_DEFERRED = ". . . "
BLACK_MOVE_PREFIX = "…"

# Type of movetext representation, "san", "lan"
MOVETEXT_KEY_FOR_MAINLINE = "san"
MOVETEXT_KEY_FOR_ALTERNATIVES = "san"

# Chess constants
FEN_INITIAL = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# HTML constants for Variations Table template

# Optional newline character to enhance readability of the raw HTML in the templates, though HTML doesn’t read and
# thus doesn’t care
HTML_READABILITY_HACK = '\n'
# HTML_READABILITY_HACK = ''

# The following implements having a minimum number of alternative-move slots displays, even if the currently displayed
# does not have that many alternatives. This is to prevent jankiness when transitioning from one main line to another.
# The value of 8 is hard-coded based on the statistical analysis of the sample PGN.
VARTABLE_MINIMUM_NUMBER_OF_ALTERNATIVES_TO_DISPLAY = 8

VARTABLE_VARIATION_ROW_PREFIX = '<tr class="variation">' + HTML_READABILITY_HACK
VARTABLE_VARIATION_FAUX_ROW_PREFIX = '<tr class="variation faux-row">' + HTML_READABILITY_HACK
VARTABLE_ROW_SUFFIX = '</tr>' + HTML_READABILITY_HACK

VARTABLE_CELL_PREFIX_OPEN = '<td class="'
VARTABLE_CELL_PREFIX_CLOSE = '">'
VARTABLE_CELL_SUFFIX = '</td>' + HTML_READABILITY_HACK

VARTABLE_CELL_PREFIX_FULLMOVE_NUMBER = '<td class="fullmovenumber">'

# This does NOT close the initial <td> tag so that an additional class can be specified
VARTABLE_ROW_PREFIX_WHITE_MAINLINE_MOVE = '<td class="mainline-white '

VARTABLE_ALT_HALFMOVE_STYLE_NAME_PREFIX = "alt-"

# CSS style names for mainline moves
VARTABLE_CSS_NAME_MAINLINE_BASE = "mainline"
VARTABLE_CSS_NAME_MAINLINE_WHITE = f'{VARTABLE_CSS_NAME_MAINLINE_BASE} {VARTABLE_CSS_NAME_MAINLINE_BASE}-white'
VARTABLE_CSS_NAME_MAINLINE_BLACK = f'{VARTABLE_CSS_NAME_MAINLINE_BASE} {VARTABLE_CSS_NAME_MAINLINE_BASE}-black'
VARTABLE_CSS_NAME_MAINLINE_WHITE_NULL = f'{VARTABLE_CSS_NAME_MAINLINE_WHITE} {VARTABLE_CSS_NAME_MAINLINE_WHITE}-null '
VARTABLE_CSS_NAME_MAINLINE_WHITE_NONNULL = f'{VARTABLE_CSS_NAME_MAINLINE_WHITE} {VARTABLE_CSS_NAME_MAINLINE_WHITE}-nonnull '
VARTABLE_CSS_NAME_MAINLINE_BLACK_NULL = f'{VARTABLE_CSS_NAME_MAINLINE_BLACK} {VARTABLE_CSS_NAME_MAINLINE_BLACK}-null '
VARTABLE_CSS_NAME_MAINLINE_BLACK_NONNULL = f'{VARTABLE_CSS_NAME_MAINLINE_BLACK} {VARTABLE_CSS_NAME_MAINLINE_BLACK}-nonnull '

# Additional style name for mainline move that receives focus
VARTABLE_CSS_NAME_MAINLINE_FOCUS = f'{VARTABLE_CSS_NAME_MAINLINE_BASE}-focus '

# CSS style names for alternative moves
VARTABLE_CSS_NAME_ALTERNATIVE_BASE = "alt"
VARTABLE_CSS_NAME_ALTERNATIVE_WHITE = f'{VARTABLE_CSS_NAME_ALTERNATIVE_BASE} {VARTABLE_CSS_NAME_ALTERNATIVE_BASE}-white '
VARTABLE_CSS_NAME_ALTERNATIVE_BLACK = f'{VARTABLE_CSS_NAME_ALTERNATIVE_BASE} {VARTABLE_CSS_NAME_ALTERNATIVE_BASE}-black '

VARTABLE_BASE_URL = "/node/"
VARTABLE_ANCHOR_CLASS = f"{VARTABLE_CSS_NAME_ALTERNATIVE_BASE}-anchor"
VARTABLE_ANCHOR_PREFIX_OPEN = f'<a class="{VARTABLE_ANCHOR_CLASS}" href="{VARTABLE_BASE_URL}'
VARTABLE_ANCHOR_PREFIX_CLOSE = '">'
VARTABLE_ANCHOR_SUFFIX = '</a>'

# Parameters for display of SVG chess board
SVG_BOARD_BASE_URL = "https://backscattering.de/web-boardimage/board.svg?"
SVG_BOARD_THEME_PREFIX = "colors="
SVG_BOARD_SIZE_PREFIX = "size="
SVG_BOARD_COORDINATES_BOOLEAN_PREFIX = "coordinates="
SVG_BOARD_ORIENTATION_PREFIX = "orientation="
SVG_BOARD_FEN_PREFIX = "fen="
SVG_BOARD_LAST_MOVE_PREFIX = "lastMove="
SVG_BOARD_CHECK_PREFIX = "check="

# SVG_BOARD_THEME = "wikipedia"
# SVG_BOARD_THEME = "lichess-brown"
SVG_BOARD_THEME_VALUE = "lichess-blue"

SVG_BOARD_SIZE_VALUE = "500"
SVG_BOARD_COORDINATES_BOOLEAN_VALUE = "true"
SVG_BOARD_ORIENTATION_VALUE = "white"



