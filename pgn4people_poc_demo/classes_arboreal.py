"""
Defines the GameNode and Edge classes

See generally pgn4people-poc/docs/game-tree-concepts.md
"""

import logging


from . import constants

class GameNode:
    """
    The class of which each node (position) is an instance.

    See pgn4people-poc/docs/game-tree-concepts.md
    """


   # Define/initialize class attributes to support reporting statistics on the gametree
    set_of_node_IDs = set()
    set_of_nonterminal_node_IDs = set()
    # set_of_terminal_node_IDs = set()  # Will be computed later, so doesn't need to be initialized
    # max_variation_depth = 0
    # max_halfmove_length_of_line = 0

    # Track maximum number of edges across nodes without requiring a full report to be compiled. Reason: To allow
    # the Variations Table to be a fixed width to avoid jankiness.
    maximum_number_of_edges_per_node = 0

    # Defining the set of valid instance attributes
    __slots__ = {
        "halfmovenumber":
            "The halfmove number of every edge/move that is spawned directly from this node",
        "depth":
            "number of deviations from the local main line required to reach thisn node from the initial node",
        "originatingnode_id":
            "node_id of the node that uniquely immediately precedes this node",
        "preceding_comment":
            "comment text that, in the PGN,  occurs at the beginning of a variation and precedes the corresponding movetext.",
        "comment":
            "comment text associated with the node’s position; not a preceding comment",
        "fen":
            "FEN of chess position that corresponds to this node.",
        "choice_id_at_originatingnode":
            "index of edge within the originating node’s .edgeslist that led to this node",
        "edgeslist":
            "List of edges (of class Edge) attached to this node. (Compiled incrementally as PGN is parsed.)",
        "number_of_edges":
            "Number_of_edges in .edgeslist. (Compiled incrementally as PGN is parsed.)",
        "display_order_of_edges":
            "List of indices that point to original index of edges before temporary reordering for display purposes."
    }

    
    def __init__(self, *,
                 depth=None,
                 halfmovenumber=None,
                 originating_node_id=None,
                 preceding_comment = None,
                 comment = None,
                 fen = None,
                 choice_id_at_originatingnode=None,
                 node_id=None):
        # Note that node_id is NOT an attribute of the node object; it is passed to the constructor for information so
        # that the node_id will be added to the class attribute .set_of_node_IDs at the time the node is created.
        self.depth = depth
        self.halfmovenumber = halfmovenumber
        self.originatingnode_id = originating_node_id
        self.preceding_comment = preceding_comment
        self.comment = comment
        self.fen = fen
        self.number_of_edges = 0
        self.edgeslist = []

        # self.choice_id_at_originatingnode = constants.UNDEFINED_TREEISH_VALUE
        self.choice_id_at_originatingnode = choice_id_at_originatingnode

        # Add node_id, which is NOT an attribute of this instance, to the class attribute .set_of_node_IDs
        # Checks for valid node_id. If not, skip. This allows for faux node for purposes of the initial invisible row
        # of the variations table
        if node_id != constants.UNDEFINED_TREEISH_VALUE:
            self.__class__.set_of_node_IDs.add(node_id)


    def install_new_edge_on_originating_node(self, new_edge, originating_node_id):
        """
        (a) Adds a newly discovered Edge to its originating node, (b) increments number of edges at originating node,
        and (c) add this originating node to the set of nonterminal nodes (since we know it has at least one successor).

        USAGE: method is meant to be called on gamenodes[originating_node_id]

        NOTE: originating_node_id is passed as an argument solely to allow originating_node_id to be added to
        set_of_nonterminal_nodes. (originating_node_id is not needed for the addition of the new edge, because this 
        method is called on the appropriate node.)

        Alternatively, the node could be added to the set of nonterminal nodes only the first time an edge is
        installed. It's not clear that imposing that condition would save time, because evaluating it could take as
        much time as redundantly adding the node to the set of nonterminal nodes.
        """
        self.number_of_edges += 1
        self.edgeslist.append(new_edge)

        # Updates maximum_number_of_edges_per_node
        if self.number_of_edges > self.__class__.maximum_number_of_edges_per_node:
            self.__class__.maximum_number_of_edges_per_node = self.number_of_edges


        # Determine the index this added edge is assigned at the originating node, and add this as a property to the
        # edge.
        
        new_edge.reference_index = len(self.edgeslist) - 1

        # Add this node to set of nonterminal nodes
        self.set_of_nonterminal_node_IDs.add(originating_node_id)


class Edge:
    """
    The class of which each edge is an instance.

    See pgn4people-poc/docs/game-tree-concepts.md
    """


    __slots__ = {
        "movetext_dict":
            "Dictionary with multiple textual representations of the movetext",
        "nag_list":
            "A list of integers, one for each NAG attached to the movetext.",
        "destination_node_id":
            "Description of destination_node_id",
        "reference_index":
            "Description of reference_index",
    }


    def __init__(self, movetext_dict, destination_node_id):
        self.movetext_dict = movetext_dict
        self.destination_node_id = destination_node_id
        self.nag_list = []


    def __str__(self):
        """
        String representation of instance of Edge class.
        """
        movetext_to_print = self.movetext_dict["lan"]
        return f"({movetext_to_print}, REF:{self.reference_index}, →{self.destination_node_id})"


class GameTreeReport:
    """
    Set of data characterizing a game tree in terms of number of lines, length
    of lines, and hierarchical depth.

    Object attributes:
        number_of_nodes: Total number of all nodes, both terminal and nonterminal
        number_of_lines: Number of terminal nodes
        max_halfmove_length_of_a_line : The halfmove length of the longest line (measured in halfmoves)
        max_depth_of_a_line: The maximum depth associated with a terminal node. (The number of deviations from the
            mainline on the path that is required to reach that terminal node.)
        halfmove_length_histogram: A collections.Counter dict of {halfmove_length: frequency} key:value pairs, where
            frequency is the number of terminal nodes with halfmove equal to the given halfmove_length.
        depth_histogram: A collections.Counter dict of {depth: frequency} key:value pairs, where frequency is the number
            of terminal nodes with depth equal to the given depth.
    
    Used by characterize_gametree() in compile_and_output_report.py.
    """


    # def __init__(self,
    #              number_of_nodes,
    #              number_of_lines,
    #              max_halfmove_length_of_a_line,
    #              max_depth_of_a_line,
    #              halfmove_length_histogram,
    #              depth_histogram):
    #     self.number_of_lines = constants.UNDEFINED_TREEISH_VALUE
    #     self.max_halfmove_length_of_a_line = constants.UNDEFINED_TREEISH_VALUE
    #     self.max_depth_of_a_line = constants.UNDEFINED_TREEISH_VALUE
    #     self.halfmove_length_histogram = {}
    #     self.depth_histogram = {}