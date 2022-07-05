"""
Routes associated with the PGN file and raversing the tree: '/node/nnn',
'/report', and 'dump_pgn'
"""

# import logging
import os

from flask import Blueprint
from flask import flash
from flask import render_template

from . build_tree import buildtree
from . classes_arboreal import GameTreeReport
from . compile_game_tree_report import characterize_gametree
from . import constants
from . process_pgn_file import clean_and_parse_string_read_from_file
from . traverse_tree import deviation_history_of_node
from . variations_table import construct_list_of_rows_for_variations_table


# NOTE: As of 7/1/2022
# Ultimately I want to perform the tree-creation only once and cache it.
# At this point, to abstract away from those questions, I will do it EVERY TIME a request is made.

# Re Blueprints, see https://flask.palletsprojects.com/en/2.1.x/tutorial/views/
blueprint = Blueprint('traverse', __name__)

@blueprint.route('/node/<int:target_node_id>')
def promote_node_to_main_line(target_node_id=0):
    """
    When user requests to elevate a particular node (viz., target_node_id) to the main line, displays new
    variations-table web page reflecting the specified node elevated to the main line.
    """

    # Gets nodedict embodying the game tree defined by the built-in PGN file
    nodedict = prepare_nodedict_for_tranversal()

    # Computes the deviation history required to achieve the specified target_node_id
    deviation_history = deviation_history_of_node(nodedict, target_node_id)

    # Gets a list of HTML table rows for the new variations table
    list_of_rows_for_variations_table = construct_list_of_rows_for_variations_table(nodedict, deviation_history)

    if target_node_id == 0:
        flash_message = f"The game tree has been reset to the original main line."
    else:
        flash_message = f"Node {target_node_id} has been elevated to the main line."

    flash(flash_message)

    # Renders the new variations table, incorporating the new rows
    return render_template("traverse/variations_table.html", 
                           target_node_id = target_node_id,
                           list_of_rows_for_variations_table = list_of_rows_for_variations_table)
    # return render_template("traverse/variations_table.html", target_node_id = target_node_id)


@blueprint.route('/report')
def render_report_of_game_tree_statistics():
    """
    Renders a web page with a report of statistics about the game tree
    """

    # Gets nodedict embodying the game tree defined by the built-in PGN file
    nodedict = prepare_nodedict_for_tranversal()

    # Populates the class attributes of class GameTreeReport
    characterize_gametree(nodedict)

    depth_histogram = GameTreeReport.depth_histogram
    length_histogram = GameTreeReport.halfmove_length_histogram

    # Computes supplemental statistics not included in the class attributes of class GameTreeReport
    sum_of_depth_histogram_frequencies = sum(depth_histogram.values())
    sum_of_length_histogram_frequencies = sum(length_histogram.values())

    return render_template("traverse/report.html",
                           game_tree_report=GameTreeReport,
                           sum_of_depth_histogram_frequencies = sum_of_depth_histogram_frequencies,
                           sum_of_length_histogram_frequencies = sum_of_length_histogram_frequencies,
                           )


@blueprint.route('/dump_pgn')
def dump_pgn():
    """
    Renders a web page that displays the raw PGN from the built-in PGN file
    """
    string_read_from_file = read_static_pgn_file()

    # Replaces all newline characters with HTML <br> tags
    string_read_from_file = string_read_from_file.replace("\n", "<br>")

    return render_template("traverse/dump_pgn.html", raw_pgn_string = string_read_from_file)


def prepare_nodedict_for_tranversal():
    """
    Constructs from scratch the nodedict that represents the game tree,
    starting from reading the built-in PGN file.

    This function should ultimately be cached, because this step should be
    performed only once; nodedict should never change, because the built-in
    PGN file which determines it never changes.
    """

    # Get string of PGN from built-in PGN file
    string_read_from_file = read_static_pgn_file()

    # Grab the movetext from game #1 by stripping headers and stripping textual annotations; then tokenize that string.
    tokenlist = clean_and_parse_string_read_from_file(string_read_from_file)

    # Builds tree from pgn file
    nodedict = buildtree(tokenlist)
    return nodedict


def read_static_pgn_file():
    """
    Reads the built-in PGN file and returns a string
    """

    # Note: in Python 3.9+, I believe that __file__ necessarily returns an absolute path and thus the os.path.abspath
    # part of the next line of code would be unnecessary. See https://www.youtube.com/watch?v=LVhxqOznPg0
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Constructs path to built-in PGN file
    pgn_file = os.path.join(basedir, constants.PATH_OF_PGN_FILE)

    with open(pgn_file, "r") as file:
        string_read_from_file = file.read()

    return string_read_from_file


