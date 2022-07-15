# pgn4people: A web-based demo of a better way to view PGN chess games

<img width="841" alt="Screenshot_pgn4people_web_app_sans_welcome" src="https://user-images.githubusercontent.com/8410716/177692439-129d6eda-3f15-4f84-8114-1094dab7732b.png">


This repository is the code for a [Flask](https://flask.palletsprojects.com) web app currently hosted on [PythonAnywhere](https://www.pythonanywhere.com/). The app  can be visited and explored at [pgn4people.app](http://127.0.0.1:4991/).

__pgn4people__ is a demonstration, and proof of concept, of a new and better way to navigate complex chess games and repertoires. This web app allows you to play around with the __pgn4people__ concept using a sample PGN file meant to simulate working with a large repertoire.

Essentially the same code was previously implemented as a CLI command-line application at the GitHub repository [pgn4people-poc](https://github.com/jimratliff/pgn4people-poc).

Read the [README](https://github.com/jimratliff/pgn4people-poc/blob/main/README.md) at that project for much more discussion about what’s wrong with traditional PGN interfaces when faced with complex chess games and repertoires and how __pgn4people__ improves usability.

# To run locally
```
export FLASK_DEBUG=1
export FLASK_APP=pgn4people_poc_demo
```

## Version History
* 1.0.0 7/6/2022
    * Initial release
    * Launched on PythonAnywhere at the URL [pgn4people.app](https://www.pgn4people.app/).
<!--
* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release
-->
## License

This project is licensed under the MIT License - see the LICENSE.md file for details.