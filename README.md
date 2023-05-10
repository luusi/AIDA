# AIDA

[![](https://img.shields.io/github/license/luusi/aida)](./LICENSE)

AIDA (Adaptive InDustrial APIs) is a tool for the composition of Industrial APIs for resilience manufacturing. 

The proposed technique generates a plan for a manufacturing process by orchestrating manufacturing actors which are depicted as services.

[comment]: # (To show the correctness of the tool we propose the electric motor case study.)

## Preliminaries

We assume the user uses a **UNIX-like** machine and that has **Python 3.10** installed.

- To set up the virtual environment install [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/) (<code>pip install pipenv</code>), then execute
```
pipenv install --dev
```

- Start a shell within the Python virtual environment (to be done whenever a new terminal is opened):
```
pipenv shell
```

- Install the Python package in development mode:
```
pip install -e .
```

- Install Graphviz to use rendering functionalities. 
  At [this page](https://www.graphviz.org/download/) you will find the releases for all the supported platform.

- Install [Lydia](https://github.com/whitemech/lydia). 
  We suggest to install it by [building it from source](https://github.com/whitemech/lydia#build-from-source).

- Generate Python client from OpenAPI v3.0 specification (maybe you need to change permissions of the script file):
```
cd local/IndustrialAPI/actors_api_mdp_ltlf/openapi_client_script
# chmod 777 generate-openapi-client.sh
./generate-openapi-client.sh
```
## Structure of the code
- `aida`: the library that contains reusable software components of the code where services, target and the composition LMDP are defined.
- `local`: the library that shows the orchestration of the Industrial APIs.
- `docs/notebooks/electric-motor-production.ipynb`: the notebook that shows the electric motor case study using Lexicographic Markov Decision Processes.

## Instructions on how to run the experiment
- To run the local code each of the following commands must be executed on a separate terminal with the virtual environment activated.

First, run the HTTP server that acts as a service repository and a communication middleware:
```
cd local/IndustrialAPI
python app.py
```

Then, put the <code>.sdl</code> and <code>.tdl</code> files representing services and target respectively in the relative directory, i.e,. [descriptions](local/IndustrialAPI/actors_api_mdp_ltlf/descriptions/). 

Run all the services (i.e. Industrial APIs):
```
cd local
python launch_devices.py
```
Finally, run the orchestrator:
```
cd local
python main.py
```

- To see the Jupyter Notebook run the server:
```
jupyter-notebook
```
then, open the link and navigate through `docs/notebooks` and run the notebook [electric-motor-production.ipynb](./docs/notebooks/electric-motor-production.ipynb) to replicate the experiment.

## License
The software is released under the MIT license.
