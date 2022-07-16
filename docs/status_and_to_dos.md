# Status and To-Dos
## 7/14/2022, v.1.1.0 Transitioned to python-chess for the parsing of the PGN file

# To Dos
## ✅ GameNode: Add `.fen` attribute to `GameNode` and populate it when nodes are created
Each node needs to store the FEN corresponding to the position when the node is reached.

## ❑ Print FEN for chosen node-to-elevate to web page
This is just as an intermediate step, to demonstrate capability.

## ❑ Enhance /node/nnn route URL to support specifying a distinguished halfmove
Change traverse.py » `@blueprint.route('/node/<int:target_node_id>')` to pull in a string, e.g., nnn-mm, where nnn is 
the node number and mm is the halfmove number.

When that URL is visited, node nnn is promoted to the main line, as current, but in addition the mm halfmove of the
main line is highlighted, and—ultimately its position shown on the board.

## ❑ Variations Table: Wrap mainline moves in `<a href="/node/nnn-mm">`
Make mainline moves clickable links. Clicking on a mainline move would not change the node that is elevated to the 
main line. It would however refresh the page with the addition that:
* The mm-th halfmove of the main line would receive a CSS style that would result in its being specially highlighted
* Ultimately, the position resulting from this distinguised mainline halfmove would be displayed on the chess board.

In this way, the user can navigate *all* moves, mainline and alternatives, by clicking on moves on the variations table.

## ❑ Variations Table: Change layout of variations_table.html to provide space on l.h.s. for chessboard
pgn4people_poc_demo/templates/traverse/variations_table.html

## ❑ Display current position on chessboard

## ❑ Display comment for current move in text field below chessboard