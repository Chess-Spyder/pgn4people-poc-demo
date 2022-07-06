"""
Methods to traverse the game tree birectionally with output.

See generally pgn4people-poc/docs/game-tree-concepts.md
"""

from . classes_arboreal import (GameNode,
                                GameTreeReport)
from . error_processing import fatal_developer_error
# from . construct_output import print_single_node_to_console
from . import constants
from . utilities import (fullmovenumber_from_halfmove,
                             is_white_move)


def deviation_history_of_node(nodedict, target_node_id):
    """
    Returns the deviation history of node_id (with respect to the node dictionary nodedict)).
    Arguments:
        nodedict: a dictionary of (node_id, node) pairs, where node is an instance of the GameNode class.
        target_node_id : The node of nodedict whose deviation history is desired.
    
    Background:
    A deviation is a (node_id, choice_id) pair, where choice_id is assumed not equal to zero.
    According to this deviation, at node node_id, the action choice_id ≠ 0 is chosen rather than the main line
    choice_id=0.

    In other words, the default action at any node is the zero-th index, i.e., the mainline choice. A deviation exists
    only when the chosen action is different from the mainline choice.

    A deviation history is a collection of deviations.
    Specifically, a deviation history is a dictionary all of whose (key, value) items are of the form:
        key = node_id of somedeviation
        value = choice_id of somedeviation
    where some_deviation is a deviation.

    To any target node there corresponds a unique deviation history (modulo recognition that a dictionary is unordered)
    that brings the play to that node.

    """
    deviation_history = {}

    # Start at the target node and traverse the tree backward to the origin, recording the
    # (node_id, choice_id) at every immediate-predecessor node at which a non-mainline choice was made.
    # By "record," means add (node_id, choice_id) as a key/value pair to the history dictionary.

    current_node_id = target_node_id
    while current_node_id != constants.INITIAL_NODE_ID:
        # This loop stops when it reaches the original node (id=0), which has no predecessor.

        immediate_predecessor_node_id = nodedict[current_node_id].originatingnode_id
        choice_at_predecessor = nodedict[current_node_id].choice_id_at_originatingnode

        if choice_at_predecessor != constants.INDEX_MAINLINE:
            # Action other than zero implies deviation from the mainline at the predecessor.
            deviation_history[immediate_predecessor_node_id] = choice_at_predecessor
        current_node_id = immediate_predecessor_node_id

    return deviation_history


def compile_movetext_elements_for_output_for_single_node(node,
                                                         choice_id_as_mainline,
                                                         inbound_carryover_white_edge):
    """
    Compiles the movetext elements to be output for a single line of the variations table,
    where the line corresponds to a single node.

    If inbound_carryover_white_edge is not None (this should occur only when node belongs to Black),
    inbound_carryover_white_edge is used as mainline_edge_white on the same line as Black’s move.

    If node belongs to White, and there is only one edge (i.e., no non-mainline alternatives), then
    outbound_carryover_white_edge is set to White’s move and function returns without compiling any output.

    Returns variations_line, an instance of the Variations_Table_Line class:
        is_terminal_node
        has_carryover_White_edge
        carryover_white_edge
        mainline_edge_white
        mainline_edge_black
        list_of_alternative_edges_to_display
    """
    number_of_edges = node.number_of_edges

    halfmovenumber = node.halfmovenumber
    fullmovenumber = fullmovenumber_from_halfmove(halfmovenumber)
    is_player_white = is_white_move(halfmovenumber)
    # player_color_string = assign_player_color_string(is_white_move)

    # Case: Terminal node case
    if number_of_edges == 0:
        # IS a terminal node. Either there is nothing to print and we stop, or we still need to flush a residual
        # carryover_white_edge left over from last iteration.
        is_terminal_node = True

        if inbound_carryover_white_edge is not None:
            if is_player_white:
                fatal_developer_error(f"inbound_carryover_white_edge is not None but player is White.")
            else:
                # Though player is Black, Black has no moves, so we revert to player is White, playing the carry-over
                # move.
                is_player_white = True
                mainline_edge_white = inbound_carryover_white_edge
                variations_line = Variations_Table_Line(is_terminal_node,
                                                        is_player_white = is_player_white,
                                                        fullmovenumber = fullmovenumber,
                                                        mainline_edge_white = mainline_edge_white,
                                                        mainline_edge_black = None,
                                                        outbound_carryover_white_edge = None,
                                                        list_of_alternative_edges_to_display = None)
        else:
            # Terminal node with no carryover move to print. Thus we print nothing and stop.
            variations_line = Variations_Table_Line(is_terminal_node)
        return variations_line

    # Case: NOT a terminal node. Thus we proceed to print a line
    is_terminal_node = False

    # Constructs lists of indices reflecting a reordered list of edges to display
    construct_display_order_of_node_edges(node, choice_id_as_mainline)

    # The following is a list of indices
    display_order_of_edges = node.display_order_of_edges

    # Gets mainline edge for the player with non-mainline alternatives
    mainline_edge = node.edgeslist[display_order_of_edges[0]]

# Case: White to move, but White has only a mainline move and no alternatives.
    if is_player_white and (number_of_edges == 1):
        # We defer any output in order to combine the next halfmove (of Black’s) on the same line.

        outbound_carryover_white_edge = mainline_edge
        variations_line = Variations_Table_Line(is_terminal_node,
                                                outbound_carryover_white_edge = outbound_carryover_white_edge)
        return variations_line
    
    # Case: (a) Either Black to move, regardless whether Black has alternatives, or (b) White to move and has
    # alternatives. Thus we output a line.

    # Assign mainline movetext for White and Black
    if is_player_white:
        # We’ve already established that White has alternatives, therefore Black’s halfmove is deferred until next line.
        mainline_edge_white = mainline_edge
        mainline_edge_black = None
    else:
        # Black’s move
        mainline_edge_black = mainline_edge

        # Decide how to populate mainline_edge_white depending on whether there was a carryover White edge
        if inbound_carryover_white_edge:
            # White’s last move was deferred, so we carry it over here, and present it along with Black’s move
            mainline_edge_white = inbound_carryover_white_edge
        else:
            # There’s no inbound carryover White edge because White’s earlier halfmove was printed on the previous 
            # line. Thus White gets an ellipsis (“…”)
            mainline_edge_white = None

    # Construct list of alternative (i.e., non-mainline) edges for the given player
    if number_of_edges > 1:
        list_of_alternative_edges_to_display = []
        # We’ve already assigned the index=0 mainline edge. Now we start the alternatives with index=1
        for index in display_order_of_edges[1::]:
            list_of_alternative_edges_to_display.append(node.edgeslist[index])
    else:
        list_of_alternative_edges_to_display = None
    
    variations_line = Variations_Table_Line(is_terminal_node,
                                            is_player_white=is_player_white,
                                            fullmovenumber=fullmovenumber,
                                            mainline_edge_white=mainline_edge_white,
                                            mainline_edge_black=mainline_edge_black,
                                            list_of_alternative_edges_to_display=list_of_alternative_edges_to_display)
    return variations_line


def construct_display_order_of_node_edges(node, choice_id_as_mainline):
    """
    For (a) a node (an instance of class GameNode) and (b) choice_id_as_mainline, an integer, constructs
        node.display_order_of_edges

        where node.display_order_of_edges is a list of INDICES (not edges)

        such that
            len(node.display_order_of_edges) = node.number_of_edges
            node.display_order_of_edges[0] = choice_id_as_mainline
            if choice_id_as_mainline != 0,
                node.display_order_of_edges[1] = 0
            and the remaining slots in node.display_order_of_edges are filled with remaining edges in node.edgeslist and
            in that order. I.e., the sequence: for j=2,…,len-1, node.display_order_of_edges[j] is the same as
            for k = 1,…,len-1 (k≠choice_id_as_mainline)
            In other words, (a) choice_id_as_mainline becomes the 0th element, (b) the previously mainline move
            edgeslist[0] becomes the first alternative,  and (c) the original indices of all the other elements of
            edgeslist are imported into display_order_of_edges in numerical order.
    
    This function does NOT return anything. It adds a property to an existing instance of class Edge.
    """

    node.display_order_of_edges = []

    # Assigns index of designated non-mainline edge to zero-th element of .display_order_of_edges
    node.display_order_of_edges.append(choice_id_as_mainline)

    for jindex in range(0, node.number_of_edges):
        if jindex != choice_id_as_mainline:
            node.display_order_of_edges.append(jindex)
        else:
            # When jindex == choice_id_as_mainline, that element should not be copied to display_order_of_edges
            # because it was already copied in the first step.
            pass
    # end for
    
    if len(node.display_order_of_edges) != node.number_of_edges:
        fatal_developer_error(
          f".display_order_of_edges had {len(node.display_order_of_edges)} elements rather than {node.number_of_edges}."
        )


class Variations_Table_Line():
    def __init__(self,
                 is_terminal_node,
                 fullmovenumber = None,
                 is_player_white = None,
                 mainline_edge_white = None,
                 mainline_edge_black = None,
                 outbound_carryover_white_edge = None,
                 list_of_alternative_edges_to_display = None):
        self.is_terminal_node = is_terminal_node
        self.fullmovenumber = fullmovenumber
        self.is_player_white = is_player_white
        self.mainline_edge_white = mainline_edge_white
        self.mainline_edge_black = mainline_edge_black
        self.outbound_carryover_white_edge = outbound_carryover_white_edge
        self.list_of_alternative_edges_to_display = list_of_alternative_edges_to_display


    def __str__(self):
        """
        String representation of instance of Variations_Table_Line class.
        """
        player_char = "W" if self.is_player_white else "B"
        # white_edge = f"({self.mainline_edge_white.movetext} , {self.mainline_edge_white.reference_index})"
        # black_edge = f"({self.mainline_edge_black.movetext} , {self.mainline_edge_black.reference_index})"
        white_edge = str(self.mainline_edge_white)
        black_edge = str(self.mainline_edge_black)
        if white_edge == None:
            white_edge = "(…)"
        if black_edge == None:
            black_edge = "(…)"
        black_edge = str(self.mainline_edge_black)
        if self.list_of_alternative_edges_to_display:
            number_of_alternatives = len(self.list_of_alternative_edges_to_display)
        else:
            number_of_alternatives = 0
        string_representation = f"#{self.fullmovenumber} {player_char} {white_edge} {black_edge} #alts: {number_of_alternatives}\n"
        if self.is_terminal_node:
            string_representation += "\nTERMINAL NODE\n"
        if self.outbound_carryover_white_edge:
            # string_representation += f"Carryover: ({self.outbound_carryover_white_edge.movetext}, {self.outbound_carryover_white_edge.reference.index})\n"
            string_representation += f"Carryover: {str(self.outbound_carryover_white_edge)}\n"
        if number_of_alternatives > 0:
            string_representation += "Alt edges: "
            for index, edge in enumerate(self.list_of_alternative_edges_to_display):
                string_representation += f"{index}: {str(edge)}; "
            string_representation += "\n"
        return string_representation


def characterize_gametree(nodedict):
    """
    Takes nodedict as representation of the tree as {node_id: node} key:value pairs, where node is an instance of the
    GameNode class.

    Statistically analyzes the game tree and returns the result  in class attributes of the GameTreeReport class.

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

    # Loops through ALL nodes
    GameTreeReport.number_of_edges_histogram = {}
    max_number_of_edges_on_a_node = 0

    for node_id in GameNode.set_of_node_IDs:
        node = nodedict[node_id]
        number_of_edges = node.number_of_edges
        if number_of_edges > max_number_of_edges_on_a_node:
            max_number_of_edges_on_a_node = number_of_edges
        
        if number_of_edges in GameTreeReport.number_of_edges_histogram.keys():
            GameTreeReport.number_of_edges_histogram[number_of_edges] += 1
        else:
            GameTreeReport.number_of_edges_histogram[number_of_edges] = 1
