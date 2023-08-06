<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/preprocessing/splines.py#L19)</span>
### EncodeSplines

```python
concise.preprocessing.splines.EncodeSplines(n_bases=10, degree=3, share_knots=False)
```

Transformer (class) for computing the B-spline basis values.

Pre-processing step for spline transformation (`SplineT`) layer.
This transformer works on arrays that are either `N x D` or `N x L x D` dimensional.
Last dimension encodes different features (D) and first dimension different examples.
Knot placement is specific for each feature individually,
unless `share_knots` is set `True`.
The final result is an array with a new axis:

- `N x D -> N x D x n_bases`
- `N x L x D -> N x L x D x n_bases`

__Arguments__

- __n_bases__: int; Number of basis functions.
- __degree__: int; 2 for quadratic, 3 for qubic splines
- __share_knots__: bool; if True, the spline knots are
	shared across all the features (last-dimension)

__Methods__

- __fit__: Calculate the knot placement from the values ranges.
- __transform__: Obtain the transformed values
- __fit_transform__: fit and transform.

----

### encodeSplines


```python
encodeSplines(x, n_bases=10, spline_order=3, start=None, end=None, warn=True)
```


**Deprecated**. Function version of the transformer class `EncodeSplines`.
Get B-spline base-function expansion

__Details__

First, the knots for B-spline basis functions are placed
equidistantly on the [start, end] range.
(inferred from the data if None). Next, b_n(x) value is
is computed for each x and each n (spline-index) with
`scipy.interpolate.splev`.

__Arguments__

- __x__: a numpy array of positions with 2 dimensions
n_bases int: Number of spline bases.
- __spline_order__: 2 for quadratic, 3 for qubic splines
start, end: range of values. If None, they are inferred from the data
as minimum and maximum value.
- __warn__: Show warnings.

__Returns__

`np.ndarray` of shape `(x.shape[0], x.shape[1], n_bases)`
