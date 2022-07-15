# Integrating python-chess and providing a more-comprehensive chess interface
Version 1.0.0 knew nothing about chess—e.g., whether a movetext string made any sense as a chess move, if so, was it legal,
and what chess position did it lead to.

Moving forward, I incorporate Niklas Fiekas’s `chess` package (previously, `python-chess`). ([GitHub](https://github.com/niklasf/python-chess), [Read the Docs](https://python-chess.readthedocs.io/en/latest/index.html))

I use python-chess for:
* Parsing a PGN file to harvest its headers, movetext, [NAG](https://en.wikipedia.org/wiki/Numeric_Annotation_Glyphs) annotations, and text annotations.
* Computing the chess position that results from implementing a move or a series of moves, and constructing the FEN
string for that resulting position.

I do not fully adopt python-chess’s game model, i.e., its particular model of nodes and moves and its classes and methods that
implement that model.

Instead, I maintain the basic game-tree classes and methodology I developed in [pgn4people-poc](pgn4people-poc) and used in version 1.0.0
of this project.

I exploit the foresight of Niklas Fiekas to provide hooks within python-chess for custom “visitors” to “[use a custom data structure,
or as an optization](https://stackoverflow.com/a/63520025/8401379).” I eschew python-chess’s
[`chess.pgn.GameBuilder` visitor](https://python-chess.readthedocs.io/en/latest/pgn.html#chess.pgn.GameBuilder), which is the default
visitor for [`chess.pgn.read_game()`](https://python-chess.readthedocs.io/en/latest/pgn.html#chess.pgn.read_game),
and replace it with my own class `PGNTokenizer`. This allows me to use the chess and PGN smarts of python-chess to
extract the information from a PGN and convert it into a token string, that I then pass along to `buildtree()`, which creates
the representation of the game tree as a dictionary of nodes, each node with zero, one, or more “edges,” which correspon to moves.