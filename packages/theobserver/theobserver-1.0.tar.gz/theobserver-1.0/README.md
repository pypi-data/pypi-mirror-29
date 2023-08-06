# The Observer
[![docs](https://readthedocs.org/projects/theobserver/badge/?version=latest)](http://theobserver.readthedocs.io/en/latest/?badge=latest)

A dataset characteristic extractor for machine learning processing.

### Observed Characteristics
- Number of instances
- Number of features
- Number of targets
- Silhouette (Dunn Index)
- Entropy
- Unbalanced

### Installation
```bash
$ pip3 install theobserver
```

### Example
```python
from theobserver import Observer

obs = Observer('examples/letter_0.csv', target_i=0)

# Return the number of instances
obs.n_instances()

# Return all characteristics
# [n_instances, n_features, n_targets, silhouette, unbalanced]
obs.extract()
```

## Docs and stuff
You can find docs, api and examples in [here](http://theobserver.readthedocs.io/en/latest/).
