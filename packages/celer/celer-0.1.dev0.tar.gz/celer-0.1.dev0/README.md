# celer

[![](https://travis-ci.org/mathurinm/celer.svg?branch=master)](https://travis-ci.org/mathurinm/celer/)
[![](https://codecov.io/gh/mathurinm/celer/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/mathurinm/celer)


Fast algorithm to solve the Lasso with dual extrapolation

# Documentation

Please visit https://mathurinm.github.io/celer/ for the latest version of the documentation.

# Basic instructions
Clone the repository:

```
$git clone https://github.com/mathurinm/celer.git
$cd celer/
$conda env create --file environment.yml
$source activate celer-env
$pip install --no-deps -e .
```

# Demos
Lasso path computation on the Leukemia dataset (comparison with scikit-learn):
```
$source activate celer-env
$ipython
%run examples/plot_leukemia_path.py
```

Lasso path computation on the Finance/log1p dataset (more significant, but it takes times to download the data, preprocess it, and compute the path):
```
$source activate celer-env
$ipython
%run examples/plot_finance_path.py
```

# Dependencies
All dependencies are in  ```./environment.yml```

# Cite
If you use this code, please cite [this paper](https://arxiv.org/abs/1802.07481):

Mathurin Massias, Alexandre Gramfort and Joseph Salmon

Dual Extrapolation for Faster Lasso Solvers

Arxiv preprint, 2018
