# PythonBotModule

This repository contains code for the Bot module written in python.

### Description

This repository contains a ChatterBot module trained with English language and some facts about general science and social life. ChatterBot is wrapped with a Flask server to makeem. a public API available to be consumed.
We're currently using Railway API in order to perform actions related to Indian Railway booking and ticket management system.

### Technologies Used

- [Python 3](http://python.org/)
- [Pipenv](https://docs.pipenv.org/)
- [ChatterBot](http://chatterbot.readthedocs.io/)
- [Flask](http://flask.pocoo.org/)
- [Railway API](https://railwayapi.com/)
- [Git](https://git-scm.com/)

### Setting up server

###### Clone the repository
`git clone https://github.com/RailwayAssistant/PythonBotModule.git`
`cd RailwayAssistant`

###### Setup Python 3 Virtual Environment
`pip install pipenv`
`pipenv --three`
`pipenv install`

###### Running the server

`pipenv run python server.py`

### Sending request

By default Flask in serving at `0.0.0.0`.
You have to simple send a get request to the server with key `q`.
For example, sending request to `0.0.0.0/?q=Hi` would respond with `How are you doing?` in plain text which you can use in your application.

### More about the important files

`server.py` contains the flask server which manages ChatterBot and RailwayAPI.
`bot.py` contains ChatterBot logics which is used to Train and then Consume the knowledge.
`db.sqlite3` contains the knowledge base or training data for the bot.
`Pipfile` and `Pipfile.lock` contains dependencies and locking informations which is used by Pipenv.
