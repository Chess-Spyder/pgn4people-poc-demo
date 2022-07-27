# Preparing for acknowledging transpositions
When the game tree represents an actual game, plus conterfactual variations that could have been played, each node has a
unique predecessor node.

This uniqueness is manifested in version 1.2.x in at least two ways:

* the definition of the `GameNode` class, which has an instance attribute of `originatingnode_id`, which is the node_id of the node that uniquely immediately precedes this node.
* that every path in the tree can be defined by a single node (which is the last node in that path which represents a departure from the local
main line). This is used in the construction of the deviation history that leads to a user-chosen alternative halfmove. The history is constructed by working backward from the chosen node, to the node’s unique immediate predecessor, to that node’s unique immediate predecessor, etc.

In contrast, for use as an opening repertoire manager it is important and desirable to acknowledge transpositions, i.e., that the same 
position (specifically the specification of the arrangement of pieces, player to move, and castling rights, but ignoring the halfmove number and halfmove clock) can be reached by multiple chains of moves.

For example, consider these two paths: (A) 1.e4 e6 2.d4 and (B) 1.d4 e6 2.e4. Both of these paths result in the same position. In particular,
the node corresponding to this position has *two* possible immediate predecessor nodes: (a) the one reached by 1.e4 e6 and (b) the one reached by 1.d4 e6.

Thus, when transpositions are acknowledged, we can no longer assume that every node has a unique immediate predecessor node.

At this point in the development of pgn4people, viz., July 25, 2022 and version 1.2.2, this document discusses steps that will need to be taken
in order to make pgn4people transposition-aware. It lays out a sequence of refactorings and modifications that can be taken as bite-sized steps, after each of which, the current functionality is intact.

# Allow for a node to have multiple immedidate predecessor nodes
## Step 1: Refactor the instance attributes of class `GameNode` to group into a named tuple the two attributes associated with the immediately preceding node

Currently, the `GameNode` class has two instance attributes that collectively track how play arrived at a given node from an immediately preceding node:
* `originatingnode_id`: the node_id of the immediately preceding node
* `choice_id_at_originatingnode`: index of the edge within the originating node’s `.edgeslist` that led to this node

As a first step in the refactoring, it will be worthwhile to join these two attributes more closely together by creating an `Origin` named-tuple class, with two attributes:
* `origin.node_id`: The node_id of the immediately preceding node.
* `origin.choice_id`: index of the edge within the immediately preceding node’s `.edgeslist` that led to this node.

Thus we can replace both of the original instance attributes `originatingnode_id` and `choice_id_at_originatingnode`, with a single
`origin` instance.

## Step 2: Create a new instance attribute of class `GameNode` to be a *list* of these named tuples
Now add a new instance attribute to class `GameNode`: `.list_of_origins`, which is a list of the `origin` instances, each of which represents an immediately preceding node and an edge at that node.

## Step 3: Add a new instance attribute to the `GameNode` class: `index_of_mru_origin`
In order to backtrack to the initial node from any given node, we can no longer count on the uniqueness of immediate predecessors, so we need to maintain the history actually chosen when that path was most recently traversed (because that path can include a node at which there are two or more choices of predecessor node).

Thus, every time a path is forward-traversed, as each node is reached we record at that node the immediately preceding node and the edge chosen at that node. Such a tuple (id of immediately preceding node, id of chosen edge at immediately preceding node) is already an instance of the named-tuple class `Origin` and indeed is already an element of `.list_of_origins`. (The `.list_of_origins` attribute of the `GameNode` instance was compiled when the game tree was first built.)

Thus, all we need record at the newly reached node is the index within the newly reached node’s `.list_of_origins` that corresponds to the `Origin` named tuple that represents the immediately preceding node and the edge chosen there.

We store this index in the new attribute of the `GameNode` class: `index_of_mru_origin`, where “mru” stands for “most recently used.”

## Step 4: Modify the `__init__()` method for class `GameNode` to conform with the new definitions.
The `__init__()` constructor method for class `GameNode` needs to be modifed in the following ways:
* Replace the separate `originatingnode_id` and `choice_id_at_originatingnode` attributes with a single `.list_of_origins` attribute.
    * The default value for `.list_of_origins` should be the empty list, `[]`.
* Add a `index_of_mru_origin` (str) attribute.
    * The default value for `index_of_mru_origin` should be zero. With this assignment, by default, in those cases where there is a unique immediate predecessor, that unique immediate predecessor will be used.

## Step 5: Make necessary changes downstream from `GameNode`’s definition
Now the remaining code needs to be conformed with the new definitions of class `GameNode`.

* Every time the `.originatingnode_id` attribute of a node is referenced, that reference should be replaced with:
```
node.list_of_origins[index_of_mru_origin].node_id
```
* Every time the `.choice_id_at_originatingnode` attribute of a node is referenced, that reference should be replaced with:
```
node.list_of_origins[index_of_mru_origin].choice_id
```

As stated, these steps do not change program behavior but rather just pave the way for later refactorings.

# Allow for the node-creation step to first check whether the resulting position is already represented by an existing node
## Define a global variable `ONLY_ONE_NODE_PER_POSITION`
To allow the same code to work both (a) with actual games and (b) with opening repertoires, we allow for either of two behaviors: (a) at most one node per position or (b) possibly multiple nodes correspond to the same position. 

Define a global variable `constants.ONLY_ONE_NODE_PER_POSITION` such that, if `True`, any distinct chess position will be represented by at most one node. If `False`, the existing behavior is maintained; i.e., every time a new move is processed, a new node is created, even if the position that results from the new move is already represented by an preexisting node.

## Define function to create and use a subset of a FEN string
Define a function `base_fen(fen_string)` that returns a truncated FEN string that includes only
* the arrangement of pieces on the board
* the player to move
* the set of castling rights

## Create a new dictionary with base-FEN string as the lookup key
We create a dictionary that takes a base-FEN string as its key.

The name and form of this dictionary depends on `constants.ONLY_ONE_NODE_PER_POSITION`. If `constants.ONLY_ONE_NODE_PER_POSITION` is:
* `True`: create a dictionary `node_id_by_base_fen`, and initialize it to the empty dictionary `{}`.
    * The value of every item in this dictionary is a single integer `node_id`.
* `False`: create a dictionary `list_of_node_ids_by_base_fen`, and initialize it to the empty dictionary `{}`.
    * The value of every item in this dictionary is a list, each element of which is a single integer `node_id`.

## When encountering a new move, compute an `Origin` object and a base-FEN for the new resultant chess position
When a new move is encountered (whether during the parsing of movetext from the PGN file or from later editing that adds a new variation),
* create `origin = Origin(originatingnode_id, choice_id_at_originatingnode)`.
* retrieve the FEN string for the position corresponding to `originatingnode_id`
* compute the FEN string for the *next* position, `new_position`, reached via the application of the new move (`uci_move`) to the previous position

Regardless whether you’re acknowledging transpositions, `origin` and `new_position` will be used to populate the node corresponding to this new move.

## Create a new function `node_id_for_new_move(origin, fen_new_position)`
Create a new function `node_id_for_new_move(origin, fen_new_position)` that:
* Determines whether a new node should be created for the new move
* If a new node should be created, it creates that node.
* If an existing node should be created, it appends `origin` to the `.list_of_origins`.
* Returns the id of the appropriate node

```
base_fen = base_fen(fen_new_position)
if not constants.ONLY_ONE_NODE_PER_POSITION:
    do_create_new_node = True
else:
    if base_fen in node_id_by_base_fen:
        do_create_new_node = False
        node_id_to_return = node_id_by_base_fen[base_fen]
        nodedict[node_id].list_of_origins.append(origin)
    else:
        do_create_new_node = True

if do_create_new_node:
    node_id_to_return = get_next_available_node_id()
    new_node = GameNode(node_id=node_id_to_return, origin_of_node=origin)

return node_id_to_return
```

<div style='padding:0.1em; margin: 1em; background-color:yellow; color:green'>
<div style="margin: 1em;">
<p style='text-align:center'><b>WARNING: Look into this</b></p>
<p>A possible issue with a node having multiple immediate predecessors is that a node’s depth may no longer be uniquely defined.</p>
<p>This may not actually be a problem: The `.depth` attribute of GameNode seems to play no role other than keeping track of the depth for the purpose of running reports.</p>
<p>I could consider: Every time a new immediate successor is added to a node, new max-depth and min-depth attributes can be updated.</p>
</div>
</div>



