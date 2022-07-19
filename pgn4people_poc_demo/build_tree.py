""" Exports the buildtree() function """

import logging

from . classes_arboreal import Edge
from . classes_arboreal import GameNode
from . constants import (
                              CLOSE_VARIATION_INDICATOR,
                              COMMENT_INDICATOR,
                              FEN_INITIAL,
                              INITIAL_NODE_ID,
                              MOVETEXT_INDICATOR,
                              NAG_INDICATOR,
                              OPEN_VARIATION_INDICATOR,
                              UNDEFINED_TREEISH_VALUE,
                              )
from . error_processing import fatal_pgn_error
from . python_chess_utilities import update_position_with_move_uci
# from . import pgn_tokenizer


def buildtree(tokenized_game):
    """
    Build the game tree—as a dictionary (“gamenodes”) of game nodes—from supplied tokenized_game, which is an object of
    class TokenizedGame.
    
    Return gamenodes.

    See generally pgn4people-poc/docs/game-tree-concepts.md
    """

    ###############   Initializations  ###############
    # Initialize empty dictionaries
    # gamenodes is indexed by a node_id
    gamenodes = {}
    # current_halfmovenumber is indexed by depth
    current_halfmovenumber = {}
    # current_originatingnode_id is indexed by depth
    current_originatingnode_id = {}
    # latest_mainline_destination is indexed by depth
    latest_mainline_destination = {}
    # Initializes empty movetext_dict
    movetext_dict = {}
    # Initialize string to hold a comment that occurs at the beginning of a variation, i.e., before the first move
    # of that variation
    comment_at_beginning_of_a_variation = ""
 
    # Initializations to begin the looping through tokens
    # The first movetext token is necessarily the main line and thus depth=0
    depth = 0
    # The first movetext token is White's first move, which has halfmovenumber=1, and depth=0
    current_halfmovenumber[depth] = 1

    # FEN for initial position
    fen_for_initial_node = FEN_INITIAL

    # Create the id=constants.INITIAL_NODE_ID=0 node corresponding to the initial position (and to White's first move)
    originating_node_id_of_initial_node = UNDEFINED_TREEISH_VALUE
    new_node = GameNode(depth = depth,
                       halfmovenumber = current_halfmovenumber[depth],
                       fen = fen_for_initial_node,
                       originating_node_id = originating_node_id_of_initial_node,
                       node_id = INITIAL_NODE_ID)
    # Adds this new node as the first node in the gamenodes dictionary
    gamenodes[INITIAL_NODE_ID] = new_node

    lastcreated_node_id = INITIAL_NODE_ID

    # The next node at current depth (0) will be spawned from node with id zero.
    current_originatingnode_id[depth]=INITIAL_NODE_ID
    # Node_id for the next node to be created
    current_node_id = 1

    # Initializes boolean variables that are meant to be true only if the current movetext was immediately
    # preceded by a closed/open parenthesis, respectively
    is_preceded_by_open_paren = False
    is_preceded_by_closed_paren = False

    # Initializes Boolean variation to apply constraints that apply only to the first
    are_awaiting_first_movetext_token = True

    # Most-recent previous token, to apply constraints based on what kinds of tokens can or cannot immediately follow
    # other kinds of tokens
    most_recently_found_token_type = "root"

    # When a comment is encountered BEFORE the movetext to which it applies, the variable
    # comment_at_beginning_of_a_variation is set to that comment text to await the next node created, and then that
    # comment will be attached to that node.
    # This variable must be reset to None everytime it is transferred to a node, because the way a node knows whether
    # there is a preceding comment to attach is by checking whether this variable is None.
    # There are two cases where this scenario can occur: (a) If there is a comment at the beginning of the PGN, i.e.,
    # before the first movetext or (b) if there is a comment at the beginning of a variation (i.e., immediately after
    # the “(” that begins the variation (before the first movetext of the variation).

    comment_at_beginning_of_a_variation = None

    tokenlist = tokenized_game.tokenlist
    for token in tokenlist:
        token_type = token[0]

        if are_awaiting_first_movetext_token:
            if token_type in (OPEN_VARIATION_INDICATOR, CLOSE_VARIATION_INDICATOR, NAG_INDICATOR):
                error_string = (f"Token type {token_type} encountered before first movetext token.\n",
                                f"½#: {current_halfmovenumber[depth]}, token: {token}")
                fatal_pgn_error(error_string)

            # Check for a comment before even the first movetext
            if token_type == COMMENT_INDICATOR:
                # There is a comment before the first move of a game. This comment is assigned to the root node
                comment_at_beginning_of_a_variation = token[1]
                gamenodes[INITIAL_NODE_ID].comment = comment_at_beginning_of_a_variation
                most_recently_found_token_type = COMMENT_INDICATOR

                # Resets comment_at_beginning_of_a_variation
                comment_at_beginning_of_a_variation = None
                continue # Proceeds to the next token

        if token_type == COMMENT_INDICATOR:
            if most_recently_found_token_type in (COMMENT_INDICATOR, CLOSE_VARIATION_INDICATOR):
                error_string = (f"Comment token cannot immediately follow token type {token_type}.\n",
                                f"½#: {current_halfmovenumber[depth]}, token: {token}")
                fatal_pgn_error(error_string)
        
            comment_text = token[1]

            if most_recently_found_token_type == OPEN_VARIATION_INDICATOR:
                comment_at_beginning_of_a_variation = comment_text
            else:
                # By elimination, token_type is either MOVETEXT_INDICATOR or NAG_INDICATOR (which itself immediately
                # followed a MOVETEXT_INDICATOR).
                # We attach this comment to the node just created for the recently preceding movetext.
                new_node.comment = comment_text
            
            most_recently_found_token_type = COMMENT_INDICATOR
            
            continue

        if token_type == NAG_INDICATOR:
            if most_recently_found_token_type != MOVETEXT_INDICATOR:
                error_string = (f"NAG token encountered immediately after a {token_type} token rather after movetext.",
                                f"\n½#: {current_halfmovenumber[depth]}, token: {token}")
                fatal_pgn_error(error_string)
            
            most_recently_found_token_type = NAG_INDICATOR

            nag_integer = token[1]
            new_edge.nag = nag_integer

            continue
        
        # Branches based on whether current token is (a) movetext, (b) “(”, or (c) “)”.
        if token_type == MOVETEXT_INDICATOR:

            most_recently_found_token_type = MOVETEXT_INDICATOR
            are_awaiting_first_movetext_token = False

            # Token is movetext, which defines an edge that connects (a) the node with id
            # current_originatingnode_id[depth] to a node about to be created with id current_node_id.
            # Processing now branches based on whether the immediately preceding token was (a) “(’, (b) “)”,
            # or (c) movetext.
            # This fact is communicated here from the previous iteration via the two Boolean variables
            # is_preceded_by_open_paren and is_preceded_by_closed_paren
            if is_preceded_by_open_paren:
                # A “(” begins a new variation at a depth one greater than the movetext immediately before the “(”.
                #   Thus, we increase the depth.
                #   The first move of this new variation should have the same halfmove number as the immediately
                #   preceding movetext, because both of these are alternatives of the same node.
                # The depth and halfmovenumber were already adjusted when the “(” was encountered, so no further
                #   adjustment is necessary at this point.
                #   (You may ask: So what’s the purpose of setting is_preceded_by_open_paren=True, if all we do is do
                #   nothing? That’s precisely the point. If is_preceded_by_open_paren had not been set to True, we would 
                #   have done something when we shouldn’t have.)

                # Resets flags for beginning of new variation
                is_preceded_by_open_paren = False
                is_preceded_by_closed_paren = False
            elif is_preceded_by_closed_paren:
                # A “)” ends the current variation and reverts to either (a) a previous line with depth one less or
                # (b) a new variation of the same depth that begins immediately. (This occurs when a node has two or
                # more alternatives in addition to the main line.)
                current_halfmovenumber[depth] += 1
                current_originatingnode_id[depth] = latest_mainline_destination[depth]

                # Resets flags for beginning of new variation
                is_preceded_by_open_paren = False
                is_preceded_by_closed_paren = False

            else:
                # Current movetext token was immediately preceded by another movetext token (not a parenthesis), or
                # comment or NAG, or by the initial node, 
                # The depth is unchanged.
                # The halfmovenumber for this depth is incremented.
                current_halfmovenumber[depth] += 1

                # Because the current token is reached directly via the previous movetext, that movetext's node is the 
                # originating node for the currently constructed new node.
                current_originatingnode_id[depth] = lastcreated_node_id

            # Define new edge corresponding to this token
            movetext_dict = token[1]
            destination_node_id = current_node_id
            new_edge = Edge(movetext_dict, destination_node_id)

            # Computes chess position achieved after this move is played
            pre_move_fen = gamenodes[current_originatingnode_id[depth]].fen
            post_move_fen = update_position_with_move_uci(pre_move_fen, movetext_dict["uci"])

            latest_mainline_destination[depth] = current_node_id

            # Update originating node about the existence of this node
            originating_node_id = current_originatingnode_id[depth]

            # Install new edge on originating node; add originating node to set of nonterminal nodes
            gamenodes[originating_node_id].install_new_edge_on_originating_node(new_edge, originating_node_id)

            # Computes index of new_edge at originating node that led to the current new node. This will be stored in
            # the new node corresponding to the current token.
            # NOTE: For any list, len(somelist)-1 is the index of most recently appended item
            index_of_edge_at_originating_node = len(gamenodes[originating_node_id].edgeslist) - 1

            # Create new node corresponding to the destination reached if the current token's move is chosen

            new_node = GameNode(depth = depth,
                                halfmovenumber = current_halfmovenumber[depth],
                                originating_node_id = current_originatingnode_id[depth],
                                preceding_comment = comment_at_beginning_of_a_variation,
                                fen = post_move_fen,
                                choice_id_at_originatingnode = index_of_edge_at_originating_node,
                                node_id = current_node_id)
            
            # Resets comment_at_beginning_of_a_variation to await the next time a comment immediately follows an
            # opening parenthesis.
            comment_at_beginning_of_a_variation = None

            
            # Add node to gamesnodes dictionary
            gamenodes[current_node_id] = new_node

            # Adjusts current_originatingnode_id[depth] and current_node_id for next node to be created
            lastcreated_node_id = current_node_id
            current_node_id += 1

            continue

        if token_type == OPEN_VARIATION_INDICATOR:
            if most_recently_found_token_type == OPEN_VARIATION_INDICATOR:
                error_string = (f"Two consecutive “(”s encountered.\n ",
                                f"½#: {current_halfmovenumber[depth]}, token: {token}")
                fatal_pgn_error(error_string)

            most_recently_found_token_type = OPEN_VARIATION_INDICATOR

            # A “(” begins a new variation at a depth one greater than the movetext immediately before the “(”.
            #   Thus, we increase the depth.
            depth += 1

            # The first move of this new variation should have the same halfmove number as the immediately
            # preceding movetext, because both of these are alternatives of the same node.
            # Thus we retain the halfmove number from the previous mainline move.
            current_halfmovenumber[depth] = current_halfmovenumber[depth - 1]

            # Retain same originating node as the previous mainline move
            current_originatingnode_id[depth] = current_originatingnode_id[depth - 1]

            # Sets flag to indicate that next token is immediately preceded by an open parenthesis
            is_preceded_by_open_paren = True

            continue
    
        if token_type == CLOSE_VARIATION_INDICATOR:
            # A “)” ends the current variation and reverts to either (a) a previous line with depth one less or
            # (b) a new variation of the same depth that begins immediately. (This occurs when a node has two or
            # more alternatives in addition to the main line.)

            most_recently_found_token_type == CLOSE_VARIATION_INDICATOR

            # We decrement the depth in case we’re continuing a previous line. (However, if it turns out that the “)”
            # is immediately followed by a “(”, the next time through the loop the if token == "("” branch will
            # un-do this decrementing by incrementing the depth.)
            depth -= 1

            # Sets flag to indicate that next token is immediately preceded by an open parenthesis
            is_preceded_by_closed_paren = True

            continue

        else:
            # It’s not that obvious what would trigger this branch, because currently any token not a “(” or “)” *IS*
            # by definition movetext.
            error_string = (f"Unexpected token type encountered, “{token_type}”\n",
                            f"½#: {current_halfmovenumber[depth]}, token: {token}")
            fatal_pgn_error(error_string)

    return gamenodes
