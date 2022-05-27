# Carcassone-AI



<br/><br/>
## About the Project

The goal of this project was to explore the possibilities of applying an agnostic decision algorithm to the game of Carcassonne. <br>
The project became a ground-up python reimplementation of the board game to establish an API that was then used to develop and analyze a variety of agents.


<br/><br/>
## Built With

The backend, API, and agents are made with pure python. 
The UI is built with [PyQt5](https://pypi.org/project/PyQt5/)


<br/><br/>
## Getting Started

### Prerequisites

* python3.9

### Installation

1. Clone the repo
  ```sh
  git clone git@github.com:cschnelz/CarcassoneAI.git
  ```
2. Install requirements
  ```sh
  pip install requirements
  ```


<br/><br/>
## Usage

There are two main ways of interacting with this project:
1. Running the app to play a game of Carcassonne against the leading bot
2. Using the API to set up and analyze other games

### Running the app

Running

```sh
python3.9 app.py
```

launches a game where a human player competes 1 on 1 with the leading agent (currently, the heuristic-based MCTS agent)

### Using the API

The API provides a much richer variety of interacting with the implementation and the agents. For example,

```python
Carcassonne = Game(players=[MCTS_Saver(info=heuristic),GreedyAgent()])
renderer = Renderer()

while(Carcassonne.gameOver() is False):
  actions = Carcassonne.getActions()
  agent = Carcassonne.currentPlayer().agent
  
  response = agent.getResponse(None,game=Carcassonne,maxPlayer=Carcassonne.currentPlayerId())
  Carcassonne.applyAction(response)
  
  Carcassonne.render(renderer)
  
print(Carcassonne.finalScore())
```

will create and run a game between an MCTS-heuristic bot and a Greedy bot.  The API provides many options for running and analyzing Carcassonne games.


<br/><br/>
## Current Agents
* Human Agent - Gets CLI response from human for moves
* Random Agent - Randomly picks from valid actions
* Greedy Agent - Full-tree analysis with a depth of 1. Evaluates as if game was to end after 1 move and makes highest scoring move
* MCTS-rollout - MCTS agent applied to Carcassonne system.  Uses random rollout for the default policy and can be tuned to run in desired amount of time
* MCTS-heuristic - Current best-bot.  MCTS system with a hand crafted heuristic evaluation in place of random rollout
