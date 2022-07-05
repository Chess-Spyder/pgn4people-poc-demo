"""
Module for functions to produce the variations table.
"""
import logging

from . classes_arboreal import Edge, GameNode
from . import constants
from . constants import (BLACK_MOVE_DEFERRED,
                         VARTABLE_ALT_HALFMOVE_STYLE_NAME_PREFIX,
                         VARTABLE_VARIATION_ROW_PREFIX,
                         VARTABLE_ROW_SUFFIX,
                         VARTABLE_CELL_PREFIX_OPEN,
                         VARTABLE_CELL_PREFIX_CLOSE,
                         VARTABLE_CELL_SUFFIX,
                         VARTABLE_CELL_PREFIX_FULLMOVE_NUMBER,
                         WHITE_MOVE_ELLIPSIS,
                         VARTABLE_CSS_NAME_MAINLINE_BLACK_NONNULL,
                         VARTABLE_CSS_NAME_MAINLINE_WHITE_NONNULL,
                         VARTABLE_CSS_NAME_MAINLINE_BLACK_NULL,
                         VARTABLE_CSS_NAME_MAINLINE_WHITE_NULL,
                         VARTABLE_CSS_NAME_ALTERNATIVE_BLACK,
                         VARTABLE_CSS_NAME_ALTERNATIVE_WHITE,
                         VARTABLE_ANCHOR_PREFIX_OPEN,
                         VARTABLE_ANCHOR_PREFIX_CLOSE,
                         VARTABLE_ANCHOR_SUFFIX,
                         VARTABLE_MINIMUM_NUMBER_OF_ALTERNATIVES_TO_DISPLAY,
                         )
from . traverse_tree import compile_movetext_elements_for_output_for_single_node


def construct_list_of_rows_for_variations_table(nodedict, deviation_history):
    """
    Constructs/returns a list of strings, each of which corresponds to the HTML for one row of the variations table
    defined by deviation_history.
    """

    list_of_strings_for_rows = []

    # Start at initial node    
    node_id = constants.INITIAL_NODE_ID
    inbound_carryover_white_edge = None

    # # Output an invisible row to establish the minimum width of the table (to prevent jankiness when one main line 
    # # transitions to another.)
    # string_for_row = (VARTABLE_VARIATION_ROW_PREFIX +
    #                   VARTABLE_CELL_PREFIX_FULLMOVE_NUMBER + VARTABLE_CELL_SUFFIX +
    #                   VARTABLE_CELL_PREFIX_OPEN + )

    do_continue = True

    is_first_row = True

    while do_continue:

        if is_first_row:
            node = get_faux_node_for_invisible_first_row()
            choice_id_as_mainline = 0
            inbound_carryover_white_edge = None
            is_first_row = False
        else:
            # Determine which edge should be treated as the main line
            # Looks whether node_id is a node at which a deviation is prescribed by history
            if node_id in deviation_history.keys():
                # Node node_id has a deviation from the mainline action to deviation_history[node_id]
                choice_id_as_mainline = deviation_history[node_id]
            else:
                # Node node_id doesn't have a deviation; use the mainline action (constants.INDEX_MAINLINE)
                choice_id_as_mainline = constants.INDEX_MAINLINE
            
            node = nodedict[node_id]

        # Get the info required to create the string of HTML for a single line of the variations table
        # varitions_line is an object of class Variations_Table_Line
        variations_line = compile_movetext_elements_for_output_for_single_node(node,
                                                                               choice_id_as_mainline,
                                                                               inbound_carryover_white_edge)
        
        # Reset inbound_carryover_white_edge
        inbound_carryover_white_edge = None

        # Extracts useful elements from variations_line to determine whether to call print_single_node_to_console()
        outbound_carryover_white_edge = variations_line.outbound_carryover_white_edge
        is_terminal_node = variations_line.is_terminal_node
        mainline_edge_white = variations_line.mainline_edge_white

        do_continue = not is_terminal_node

        if outbound_carryover_white_edge:
            # Don’t produce a line of output now (because White had only a mainline move, but no alternatives) and
            # instead pass along White’s move to be combined in the next iteration with Black’s move.
            inbound_carryover_white_edge = variations_line.outbound_carryover_white_edge
        elif (not is_terminal_node) or mainline_edge_white:
            # Produce a line of output if either (a) the node is not a terminal node or (b) even if the node is a 
            # terminal node but there was a residual carryover_white_edge that needs to be flushed.
            string_for_row = string_of_HTML_for_single_row_of_variations_table(variations_line)
            list_of_strings_for_rows.append(string_for_row)

        # Finds the next node in the main line
        if do_continue:
        # if True:
            next_node_id = nodedict[node_id].edgeslist[choice_id_as_mainline].destination_node_id
            node_id = next_node_id
    # End of while not is_terminal_node loop

    return list_of_strings_for_rows

def string_of_HTML_for_single_row_of_variations_table(variations_line):
    """
    Constructs a string of HTML corresponding to a single row of the variations table, as described by the argument
    variations_line, which is an instance of the Variations_Table_Line class.

    If reached, you can assume that either:
        • A terminal node has been reached but there was a “carryover” White move that still needs to be displayed.
        OR
        • The node to be elevated to the main line is NOT a terminal node and is either:
            • A White move with alternatives
            OR
            • A Black move with or without alternatives
    """


    string_for_row = VARTABLE_VARIATION_ROW_PREFIX
    is_player_white = variations_line.is_player_white
    mainline_edge_white = variations_line.mainline_edge_white

    # Add fullmove number
    if mainline_edge_white:
        fullmovenumber = str(variations_line.fullmovenumber) + "."
    else:
        fullmovenumber = ""
    string_for_cell = VARTABLE_CELL_PREFIX_FULLMOVE_NUMBER + fullmovenumber + VARTABLE_CELL_SUFFIX
    string_for_row += string_for_cell

    # Add White mainline halfmove
    # mainline_edge_white = variations_line.mainline_edge_white
    movetext, css_class_names_string = format_mainline_edge(mainline_edge_white, is_white = True)
    string_for_cell = HTML_string_for_variations_table_cell(movetext, css_class_names_string)
    string_for_row += string_for_cell

    # Add Black mainline halfmove
    mainline_edge_black = variations_line.mainline_edge_black
    movetext, css_class_names_string = format_mainline_edge(mainline_edge_black, is_white = False)
    string_for_cell = HTML_string_for_variations_table_cell(movetext, css_class_names_string)
    string_for_row += string_for_cell

    # Loop through alternatives halfmoves
    list_of_alternative_edges_to_display = variations_line.list_of_alternative_edges_to_display
    # is_player_white = variations_line.is_player_white

    if list_of_alternative_edges_to_display:
        for edge in list_of_alternative_edges_to_display:
            movetext, css_class_names_string = format_anchor_alternative_edge(edge, is_white = is_player_white)
            string_for_cell = HTML_string_for_variations_table_cell(movetext, css_class_names_string)
            string_for_row += string_for_cell

    # Close the row with “</tr>”
    string_for_row += VARTABLE_ROW_SUFFIX

    return string_for_row

def HTML_string_for_variations_table_cell(movetext, list_of_class_names):
    """
    Returns string of HTML: <tr class="…">movetext</tr>
    corresponding to a sincle cell of the variations table, whether that be a mainline move or an
    altnerative move.

    Takes as arguments the movetext and list of CSS class names.
    """
    string_for_cell = (VARTABLE_CELL_PREFIX_OPEN +
                       list_of_class_names +
                       VARTABLE_CELL_PREFIX_CLOSE +
                       movetext +
                       VARTABLE_CELL_SUFFIX)
    return string_for_cell


def format_mainline_edge(edge, is_white):
    """
    Provides the corresponding movetext for the supplied mainline edge and corresponding CSS class names for its cell
    Returns as a 2-ple
        • movetext_string: A string of movetext, e.g., "Bg5"
        • css_class_names_string: A string of space-separated CSS class names
            E.g.: 'mainline mainline-black mainline-black-nonnull alt-0'
    The color of the player who owns the edge determines both (a) the class names and (b) the choice of ellipsis
    """

    if edge:
        # edge corresponds to an actual move, not a “null” ellipsis
        movetext_string = edge.movetext
        cell_CSS_name_based_on_origin = cell_CSS_name_based_on_reference_index(edge)
        if is_white:
            css_class_names_string = VARTABLE_CSS_NAME_MAINLINE_WHITE_NONNULL + cell_CSS_name_based_on_origin
        else:
            css_class_names_string = VARTABLE_CSS_NAME_MAINLINE_BLACK_NONNULL + cell_CSS_name_based_on_origin
    else:
        # edge is None means that the movetext should be replaced with some kind of ellipsis
        if is_white:
            movetext_string = WHITE_MOVE_ELLIPSIS
            css_class_names_string = VARTABLE_CSS_NAME_MAINLINE_WHITE_NULL
        else:
            movetext_string = BLACK_MOVE_DEFERRED
            css_class_names_string = VARTABLE_CSS_NAME_MAINLINE_BLACK_NULL

    return movetext_string, css_class_names_string


def format_anchor_alternative_edge(edge, is_white):
    """
    Provides the corresponding movetext for the supplied alternative edge and corresponding CSS class names for its cell
    Returns as a 2-ple
        • movetext_string: A string of movetext, e.g., "Bg5"
        • css_class_names_string: A string of space-separated CSS class names
            E.g.: 'alt alt-black alt-0'
    """
    movetext_string = edge.movetext
    destination_node_id = edge.destination_node_id
    movetext_anchor_string = (VARTABLE_ANCHOR_PREFIX_OPEN +
                              str(destination_node_id) +
                              VARTABLE_ANCHOR_PREFIX_CLOSE +
                              movetext_string +
                              VARTABLE_ANCHOR_SUFFIX)
    cell_CSS_name_based_on_origin = cell_CSS_name_based_on_reference_index(edge)
    if is_white:
        css_class_names_string = VARTABLE_CSS_NAME_ALTERNATIVE_WHITE + cell_CSS_name_based_on_origin
    else:
        css_class_names_string = VARTABLE_CSS_NAME_ALTERNATIVE_BLACK + cell_CSS_name_based_on_origin

    return movetext_anchor_string, css_class_names_string


def cell_CSS_name_based_on_reference_index(edge):
    """
    Returns CSS class name incorporating the supplied edge’s original reference index, e.g., “alt-0” if it started
    life as a mainline move; “alt-1” if it started life as the first alternative, etc.
    """
    reference_index = edge.reference_index
    cell_CSS_name_based_on_origin = VARTABLE_ALT_HALFMOVE_STYLE_NAME_PREFIX + str(reference_index)
    return cell_CSS_name_based_on_origin


def get_faux_node_for_invisible_first_row():
    """
    Returns faux node for output of initial invisible row of variations table.

    This node is not assigned a node_id and is not added to the nodedict dictionary, so it will not distort the node
    report.
    """

    node = GameNode(depth = 0,
                    halfmovenumber = 1,
                    originating_node_id = 0,
                    node_id = constants.UNDEFINED_TREEISH_VALUE)
    number_of_edges = constants.VARTABLE_MINIMUM_NUMBER_OF_ALTERNATIVES_TO_DISPLAY + 1
    node.number_of_edges = number_of_edges
    sole_edge_defined = Edge(movetext="", destination_node_id=0)

    # Creates an edges list of multiple copies of this defined edge
    edges_list = []
    for index in range(0, number_of_edges):
        sole_edge_defined.reference_index = index
        edges_list.append(sole_edge_defined)

    node.edgeslist = edges_list
    return node