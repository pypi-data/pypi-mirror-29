Functions in this module work with a simple tuple representation of the dataset `(x, y)`, where

- **x**: input - np.array, list of np.arrays or a dictionary of np.arrays
- **y**: target - np.array


## Available functions

### split_KFold_idx


```python
split_KFold_idx(train, cv_n_folds=5, stratified=False, random_state=None)
```


Get k-fold indices generator

----

### subset


```python
subset(train, idx, keep_other=True)
```


Subset the `train=(x, y)` data tuple, each of the form:

- list, np.ndarray
- tuple, np.ndarray
- dictionary, np.ndarray
- np.ndarray, np.ndarray

__Note__

In case there are other data present in the tuple:
`(x, y, other1, other2, ...)`, these get passed on as:
`(x_sub, y_sub, other1, other2)`

__Arguments__

- __train__: `(x,y, other1, other2, ...)` tuple of data
- __idx__: indices to subset the data with
- __keep_other__: bool; If True, the additional tuple elements `(other1, other2, ...)` are passed
together with `(x, y)` but don't get subsetted.

----

### test_len


```python
test_len(train)
```


Test if all the elements in `train=(x,y)` the same `shape[0]`

----

### split_train_test_idx


```python
split_train_test_idx(train, valid_split=0.2, stratified=False, random_state=None)
```


Return indicies for train-test split

