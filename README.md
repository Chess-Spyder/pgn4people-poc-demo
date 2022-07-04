# Overview

Implements [pgn4people-poc](https://github.com/jimratliff/pgn4people-poc) as a [Flask](https://flask.palletsprojects.com) web app.

Directory structure, etc., adapted from the [Flask Tutorial](https://flask.palletsprojects.com/en/2.1.x/tutorial/). Note that this web app is much simpler in many respects than that created in the tutorial:

- There is no need for creation of users or for authentication
- Thus there is no need for forms
- There is no need for a database

Normally, I would adopt the `/src` directory structure (e.g., [Anthony Sottile’s explanation](https://www.youtube.com/watch?v=sW1qUZ_nSXk)), but as so much is unfamiliar to me about Flask, I strongly wanted to follow a clear, established roadmap. I haven’t found such a roadmap for Flask using the `/src` directory structure. Hence, I don’t adopt that layout here.

# Routes
## The root URL (`"/"`) is the only publicly exposed URL
(For the sake of discussion, I’ll assume that the URL for this app will be `https://pgn4people.org`.)

At least initially, the only URL deliberately exposed to web visitors is `https://pgn4people.org`.

All of the other Flask “routes,” while not hidden from visitors, are only implementation details.

## The `/node/nnn` routes are used for navigating the tree
When the root route (`"/"`) is reached, it is effectively redirected to `/node/0`, which displays the variations table, treating the original main line in the PGN as the main line to be displayed.

As I learned from [pgn4people-poc](https://github.com/jimratliff/pgn4people-poc), any alternative variation can be identified and fully represented by simply a single node ID. (There is a one-to-one correspondence between the set of possible “lines/variations” and the set of terminal nodes. For any terminal node, the path that leads there can be specified as a set of deviations (node_id, edge), where edge has a nonzero index, i.e., is not the locally mainline move at node_id. The last such deviation (i.e., has no successor deviation on that path) implies all prior deviations. Thus, the node_id of the last such deviation uniquely determines the entire line.)

Each alternative halfmove on the variations table corresponds to a particular node. (This is the destination node to which the chosen action leads.) Let that node has id n. Then clicking on that chosen alternative halfmove should take us to route `/node/n`.

We implement this by wrapping each alternative halfmove in a `<a>` anchor element, e.g., tag `<a src=/node/nnn>…Be5<a>`. Clicking on that halfmove takes control to the `/node/nnn` route, which tells the app to display the variations table for the unique main line that reaches node nnn and has no downstream deviations from locally mainline moves.

## The `/dump_pgn` outputs verbatim the stored sample PGN file
The `/dump_pgn` outputs verbatim the stored sample PGN file.

The user would effect this, however, not by entering this URL but rather by choosing some interface elemeent that would itself trigger this URL.
## The `/report` route prints the report about the game tree
The `/report` route prints the report about the game tree.

The user would effect this, however, not by entering this URL but rather by choosing some interface elemeent that would itself trigger this URL.


# Implementation details
## The app is created in the package’s `__init__.py`
## The game tree needs to be created only once and then persist across requests

## Use `flask-caching` to persist the `nodedict` dictionary across requests
## Modules and blueprints
### traverse
The view functions related to the traversal of the game tree (but not the creation of the game tree) are located in the module:
```
/path/to/pgn4people-poc-demo/pgn4people_poc_demo/traverse.py
```
These view functions are organized under the Blueprint `traverse`.

## Templates
### Default template
The default template is `site_template.html` at:
```
/path/to/pgn4people-poc-demo/pgn4people_poc_demo/templates/site_template.html
```
All other templates inherit from (i.e., extend) this template.
### “traverse” templates
- `variations_table.html`
    - For all routes of the form `/node/nnn`
- `dump_pgn.html`
    - For route: `/dump_pgn`
- `report.html`
    - For route: `report.html`