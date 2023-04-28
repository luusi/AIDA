# AIDA

[![](https://img.shields.io/github/license/luusi/aida)](./LICENSE)

AIDA (Adaptive InDustrial APIs) is a tool for the composition of Industrial APIs for resilience manufacturing. 

The proposed technique generates a plan for a manufacturing process by orchestrating manufacturing actors which are depicted as services.

To show the correctness of the tool we propose the electric motor case study.

The following sections are:
- Preliminaries
- Structure of the code
- Instructions on how to run the experiment
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
# alternatively:
# python setup.py develop 
```

- Install Graphviz to use rendering functionalities. 
  At [this page](https://www.graphviz.org/download/) you will find the releases for all the supported platform.

- Install [Lydia](https://github.com/whitemech/lydia). 
  We suggest to install it by [building it from source](https://github.com/whitemech/lydia#build-from-source).

- Generate Python client from OpenAPI v3.0 specification:
```
./scripts/generate-openapi-client.sh
```
## Structure of the code
- `aida`: the library; reusable software components of the code where are defined services, target and the composition LMDP.
- `local`: the library that shows the orchestration between the Industrial APIs.
- `docs/notebooks/electric-motor-production.ipynb`: link to the notebook that shows the electric motor case study using Lexicographic Markov Decision Processes as described in the paper.

## Instructions on how to run the experiment
- To run the local code each of the following commands must be on a separate terminal with the virtual environment activated.

First, run the HTTP server that acts as service repository and communication middleware:
```
cd local/IndustrialAPI
python app.py
```
Then, run all the services (i.e. Industrial APIs):
```
cd local
python ./launch_devices.py
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
