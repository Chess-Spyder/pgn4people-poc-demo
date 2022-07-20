# pgn4people: A web-based demo of a better way to view PGN chess games

<img width="1284" alt="Screeenshot_pgn4people_demo_2022_07_19" src="https://user-images.githubusercontent.com/8410716/179891721-aad4ee6f-5845-49e6-837b-23c698659093.png">


This repository is the code for a [Flask](https://flask.palletsprojects.com) web app currently hosted on [PythonAnywhere](https://www.pythonanywhere.com/). The app  can be visited and explored at [pgn4people.app](http://127.0.0.1:4991/).

__pgn4people__ is a demonstration, and proof of concept, of a new and better way to navigate complex chess games and repertoires. This web app allows you to play around with the __pgn4people__ concept using a sample PGN file meant to simulate working with a large repertoire.

This idea was previously implemented, in a less-functional form, as a CLI command-line application at the GitHub repository [pgn4people-poc](https://github.com/jimratliff/pgn4people-poc).

Read the [README](https://github.com/jimratliff/pgn4people-poc/blob/main/README.md) at that project for much more discussion about what’s wrong with traditional PGN interfaces when faced with complex chess games and repertoires and how __pgn4people__ improves usability.

# To run locally
```
export FLASK_DEBUG=1
export FLASK_APP=pgn4people_poc_demo
```

## Version History
* 1.0.0, 7/6/2022
    * Initial release
    * Launched on PythonAnywhere at the URL [pgn4people.app](https://www.pgn4people.app/).
* 1.2.0, 7/19/2022
    * Now chess aware thanks to incorporation of Niklas Fiekas’s awesome [python-chess](https://github.com/niklasf/python-chess) library.
    * Navigating the PGN now updates a graphic chess board, thanks to Niklas Fiekas’s [web-boardimage](https://github.com/niklasf/web-boardimage), and associated [web service](https://backscattering.de/web-boardimage/board.svg?fen=5r1k/1b4pp/3pB1N1/p2Pq2Q/PpP5/6PK/8/8&lastMove=f4g6&check=h8&arrows=Ge6g8,Bh7&squares=a3,c3).
    * Add a FEN string text area.
    * Add text-annotation area.
    * Change license for the project as a whole from MIT to GNU GPL 3, because of the reliance on python-chess.
<!--
* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release
-->
## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
