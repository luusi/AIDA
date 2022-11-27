# Industrial APIs composition via Markov Decision Processes (MDP)

Implementation a tool to compose Industrial APIs via Markov Decision Processes (MDP).

## Preliminaries

We assume the review uses a UNIX-like machine and that has Python 3.8 installed.

- Set up the virtual environment. 
First, install [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/).
Then:
```
pipenv install --dev
```
                    
- this command is to start a shell within the Python virtual environment (to be done whenever a new terminal is opened):
```
pipenv shell
```

- Install the Python package in development mode:
```
pip install -e .
# alternatively:
# python setup.py develop 
```

- Install Graphviz to use rendering functionalities. 
  At [this page](https://www.graphviz.org/download/) you will find the releases for all the supported platform.

- Install [Lydia](https://github.com/whitemech/lydia). 
  We suggest to install it by [building it from source](https://github.com/whitemech/lydia#build-from-source).

~~Install BLACK to check satisfiability of LTLf formulas. At [this page](https://www.black-sat.org/en/stable/installation.html) you will find the releases for all the supported platform.~~

## How to run the code

- Run a Jupyter Notebook server:

```
jupyter-notebook
```

- Open the link and navigate through `docs/notebooks` and run the notebook [electric-motor-production.ipynb](./docs/notebooks/electric-motor-production.ipynb) to replicate the experiment.

## License

The software is released under the MIT license.
