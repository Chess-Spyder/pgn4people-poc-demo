"""
Construct and output report characterizing the current game tree in terms of
number of lines, length of lines, and hierarchical depth.
"""

# from yachalk import chalk

from .error_processing import fatal_developer_error

from . classes_arboreal import (GameNode,
                                GameTreeReport)
from . import constants
# from . utilities import (conditionally_clear_console,
#                          wait_for_any_user_input)


def characterize_gametree(nodedict):
    """
    Takes nodedict as representation of the tree as {node_id: node} key:value pairs, where node is an instance of the
    GameNode class.

    Records the results in class attributes of the GameTreeReport class;
        number_of_nodes: Number of positions
        number_of_lines: Number of terminal nodes
        max_halfmove_length_of_a_line : The halfmove length of the longest line (measured in halfmoves)
            The length of a line is the halfmove number associated with the line’s terminal node MINUS 1, because the
            halfmove associated with the terminal node corresponds to a move never made (since it’s a terminal mode).
        max_depth_of_a_line: The maximum depth associated with a terminal node. (The number of deviations from the
            mainline required to reach that terminal node.)
        halfmove_length_histogram: A collections.Counter dict of {halfmove_length: frequency} key:value pairs, where
            frequency is the number of terminal nodes with halfmove equal to the given halfmove_length.
        depth_histogram: A collections.Counter dict of {depth: frequency} key:value pairs, where frequency is the number
            of terminal nodes with depth equal to the given depth.

    There is a one-to-one relationship between (a) a “line” and (b) a terminal node.

    The set of terminal nodes (set_of_terminal_nodes) is a class attribute of the GameNode class and can be accessed
    (read) via any node: node.set_of_terminal_nodes.
        However, .set_of_terminal_nodes shouldn't be changed when referenced as node.set_of_terminal_nodes, because
        then .set_of_terminal_nodes would become an instance attribute. (That said, I apparently was getting away with
        it. But since I didn't understand why, I changed it to self.__class__.set_of_terminal_nodes,)

    However, while set_of_nodes and set_of_nonterminal_nodes are both compiled during the buildtree() process, 
    set_of_terminal_nodes is not and must be derived from set_of_nodes and set_of_nonterminal_nodes.
    """

    #Derive set_of_terminal_nodes

    # Compute number of nodes (i.e., number of positions)
    GameTreeReport.number_of_nodes = len(nodedict)

    # Calculates set of terminal nodes from previously calculated set of all nodes and set of all nonterminal nodes
    GameNode.set_of_terminal_node_IDs = GameNode.set_of_node_IDs.difference(GameNode.set_of_nonterminal_node_IDs)
    GameTreeReport.number_of_lines = len(GameNode.set_of_terminal_node_IDs)

    # Initialized counters and histograms
    GameTreeReport.max_halfmove_length_of_a_line = 0
    GameTreeReport.max_depth_of_a_line = 0
    GameTreeReport.depth_histogram = {}
    GameTreeReport.halfmove_length_histogram = {}
    
    # Loops througn terminal nodes
    for terminal_node_ID in GameNode.set_of_terminal_node_IDs:

        terminal_node = nodedict[terminal_node_ID]

        # Process depth
        depth = terminal_node.depth

        if depth > GameTreeReport.max_depth_of_a_line:
            GameTreeReport.max_depth_of_a_line = depth
        
        if depth in GameTreeReport.depth_histogram.keys():
            GameTreeReport.depth_histogram[depth] += 1
        else:
            GameTreeReport.depth_histogram[depth] = 1
    
        # Process halfmove_length
        # The length of a line is the halfmove number associated with the line’s terminal node MINUS 1, because the
        # halfmove number associated with the terminal node corresponds to a move never made (since it’s a terminal
        # mode).
        halfmove_length = terminal_node.halfmovenumber - 1

        if halfmove_length > GameTreeReport.max_halfmove_length_of_a_line:
            GameTreeReport.max_halfmove_length_of_a_line = halfmove_length
        
        if halfmove_length in GameTreeReport.halfmove_length_histogram.keys():
            GameTreeReport.halfmove_length_histogram[halfmove_length] += 1
        else:
            GameTreeReport.halfmove_length_histogram[halfmove_length] = 1
