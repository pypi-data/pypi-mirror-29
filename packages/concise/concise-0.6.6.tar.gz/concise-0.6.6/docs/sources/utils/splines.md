<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/utils/splines.py#L10)</span>
### BSpline

```python
concise.utils.splines.BSpline(start=0, end=1, n_bases=10, spline_order=3)
```

Class for computing the B-spline funcions b_i(x) and
constructing the penality matrix S.

__Arguments__

- __start__: float or int; start of the region
- __end__: float or int; end of the region
- __n_bases__: int; number of spline bases
- __spline_order__: int; spline order

__Methods__

- **getS(add_intercept=False)** - Get the penalty matrix S
	  - Arguments
		 - **add_intercept**: bool. If true, intercept column is added to the returned matrix.
	  - Returns
		 - `np.array`, of shape `(n_bases + add_intercept, n_bases + add_intercept)`
- **predict(x, add_intercept=False)** - For some x, predict the bn(x) for each base
	  - Arguments
		 - **x**: np.array; Vector of dimension 1
		 - **add_intercept**: bool; If True, intercept column is added to the to the final array
	  - Returns
		 - `np.array`, of shape `(len(x), n_bases + (add_intercept))`
