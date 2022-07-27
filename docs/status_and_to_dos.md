# Status and To-Dos

* 7/26/2022, v.1.2.3
    * Replaced chess.svg.board() to render the chess board on the variations-table page with [cm-chessboard](https://github.com/shaack/cm-chessboard)
        

* 7/24/2022, v.1.2.2
    * Create new route `/experimental` as a test bed for the incorporation of [cm-chessboard](https://github.com/shaack/cm-chessboard)
    * Begin incorporation of [cm-chessboard](https://github.com/shaack/cm-chessboard), implementing the simplest example [Simple chessboards, view only](https://shaack.com/projekte/cm-chessboard/examples/simple-boards.html), which has clearly exposed FEN strings. Should be a simple matter to replace chess.svg.board with this.
* 7/24/2022, v.1.2.1 Dropped use of the web-boardimage HTTP service at backscattering.de for creating the SVG image of the chess board
and instead now use chess.svg.board() directly instead.
* 7/19/2022, v.1.2.0 Added graphical board, text-annotation area, FEN-string area, navigation of main line (in 
addition to previous navigation of alternative variations)

* 7/14/2022, v.1.1.0 Transitioned to python-chess for the parsing of the PGN file

# To Dos
* ❑ Replace SVG image of chess board (created by chess.svg.board()) with my own CSS-driven board, coupled with JavaScript
front end that will allow the in-browser animation of incremental moves along a mainline path without a round trip to the
server.
* ❑ Add a concept of sessions
* ❑ Add a user database
* ❑ Add ability to upload a PGN
* ❑ Add ability to store a compiled game tree as a JSON
* ❑ Add ability to export a compiled game tree as a PGN file
* ❑ Reprogram `buildtree()` to acknowledge transpositions. (This probably requires either (a) a fork or (b) conditional logic so that the code works whether or not transpositions are acknowledged.)
* ❑ Add ability to import an additional PGN file to be integrated with an existing compiled game tree. (Requires that `buildtree()` has been reprogrammed to acknowledge transpositions.)
* ❑ Add front-end interface to allow edits of the game tree via moving pieces using the mouse.
* ❑ Add ability to edit the game tree via the user interface.
* ❑ Optimizations
    * ❑ Roll my own chess board graphic, so that the entire SVG doesn’t need to be fetched each move. (I should need constituent graphics only for each piece type/color combination.)
    * ❑ Cache the computation of the game tree across a user’s queries.


# Completed To Dos
## ✅ GameNode: Add `.fen` attribute to `GameNode` and populate it when nodes are created
Each node needs to store the FEN corresponding to the position when the node is reached.

## ✅ Print FEN for chosen node-to-elevate to web page
This is just as an intermediate step, to demonstrate capability.

## ✅ Enhance /node/nnn route URL to support specifying a distinguished halfmove
Change traverse.py » `@blueprint.route('/node/<int:target_node_id>')` to pull in a string, e.g., nnn-mm, where nnn is 
the node number and mm is the halfmove number.

When that URL is visited, node nnn is promoted to the main line, as current, but in addition the mm halfmove of the
main line is highlighted, and—ultimately its position shown on the board.

## ✅ Variations Table: Wrap mainline moves in `<a href="/node/nnn-mm">`
Make mainline moves clickable links. Clicking on a mainline move would not change the node that is elevated to the 
main line. It would however refresh the page with the addition that:
* The mm-th halfmove of the main line would receive a CSS style that would result in its being specially highlighted
* Ultimately, the position resulting from this distinguised mainline halfmove would be displayed on the chess board.

In this way, the user can navigate *all* moves, mainline and alternatives, by clicking on moves on the variations table.

## ✅ Variations Table: Change layout of variations_table.html to provide space on l.h.s. for chessboard
pgn4people_poc_demo/templates/traverse/variations_table.html

## ✅ Display current position on chessboard

## ✅ Display comment for current move in text field below chessboard