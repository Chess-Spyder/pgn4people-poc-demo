"""
Module for displaying text comments on variations-table page
"""

from . constants import MOVETEXT_KEY_FOR_TEXT_COMMENTS_BOX


def extract_text_comments_for_current_node(nodedict, node_id_for_board):
    """
    Gets movetext (string) and pre- and post-comment text for node_id_for_board.

    Returns tuple (movetext, precomment, postcomment)
    """

    # Use of this crickets string is only for development, until there are actual comments in the
    # sample PGN
    # crickets = " 🦗 🦗 🦗 … "
    crickets = ""

    node_to_harvest_comments = nodedict[node_id_for_board]

    id_of_node_leading_to_node_to_harvest_comments = node_to_harvest_comments.originatingnode_id

    if id_of_node_leading_to_node_to_harvest_comments >= 0:

        choice_id_at_originatingnode = node_to_harvest_comments.choice_id_at_originatingnode

        node_leading_to_node_to_harvest_comments = nodedict[id_of_node_leading_to_node_to_harvest_comments]

        edge_for_movetext = node_leading_to_node_to_harvest_comments.edgeslist[choice_id_at_originatingnode]

        movetext_string = edge_for_movetext.movetext_dict[MOVETEXT_KEY_FOR_TEXT_COMMENTS_BOX]

        # Consider a comment at the very beginning of the PGN. It will be interpreted as a comment that belongs to the 
        # game or, alternatively, to all of the possible first moves for White.
        # The function buildtree() stores this comment in the initial node’s comment attribute.
        # Thus, when id_of_node_leading_to_node_to_harvest_comments==0, we take nodedict[0].comment and use it as the pre-comment for whichever
        # first move by White was chosen.
        if id_of_node_leading_to_node_to_harvest_comments == 0:
            precomment = nodedict[0].comment
        else:
            precomment = node_to_harvest_comments.preceding_comment

        postcomment = node_to_harvest_comments.comment
    else:
        movetext_string = ""
        precomment = None
        postcomment = None   

    if not precomment:
        precomment = crickets
    
    if not postcomment:
        postcomment = crickets

    return (movetext_string, precomment, postcomment)
