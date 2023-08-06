In bioinformatics we often deal with missing values. When doing a multi-task classification, one might come across a case where not all the reponse values are allways present. For this purpose, one should mask the missing values and hence ignore them in our loss-function.

Default `MASK_VALUE` = -1. Hence when training our model:

```python
model.fit(X, y)
```

data-points where `y == -1` do not contribute to parameter update.


<!-- TODO - what numeber to take for regression -9999999999 ?  -->

## Available loss functions

### mask_loss


```python
mask_loss(loss, mask_value=-1)
```


Generates a new loss function that ignores values where `y_true == mask_value`.

__Arguments__

- __loss__: str; name of the keras loss function from `keras.losses`
- __mask_value__: int; which values should be masked

__Returns__

function; Masked version of the `loss`

__Example__

```python
	categorical_crossentropy_masked = mask_loss("categorical_crossentropy")
```

----

### categorical_crossentropy_masked


```python
categorical_crossentropy_masked(y_true, y_pred)
```

----

### sparse_categorical_crossentropy_masked


```python
sparse_categorical_crossentropy_masked(y_true, y_pred)
```

----

### binary_crossentropy_masked


```python
binary_crossentropy_masked(y_true, y_pred)
```

----

### kullback_leibler_divergence_masked


```python
kullback_leibler_divergence_masked(y_true, y_pred)
```

