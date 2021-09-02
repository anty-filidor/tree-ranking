# Tree Ranking
This repository contains implementation of task described in 'TASK.md'

Author: Michał Czuba
Date: 16.08.2021

## Manual

### Set up python environment
```
conda create -y --name tree_ranking python=3.8
conda activate tree_ranking
pip install -r requirements.txt
```

In order to see visualisations please install graphviz library on your machine (use terminal):
* for MacOS: `brew install graphviz`,
* for Linux: `sudo apt-get install graphviz`,
* for Windows: just switch to Unix ;),
then uncomment lines 68-69 in src/tree.py.

### Run the code
This command runs the solution: `python color_ranking.py --criteria <choose criterium> --file <path to file>`

You can select criteria from following options: `subtree-count`, `subtree-maxdepth`, `subtree-average-value`.
Path to the file should be a string like: `examples/tree_02.csv`

### Run tests
You can run tests via pre-commit (`pre-commit install`, `pre-commit run`) or with CLI (`python -m pytest -v src/tests`).
