<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/regularizers.py#L8)</span>
### SplineSmoother

```python
concise.regularizers.SplineSmoother(diff_order=2, l2_smooth=0.0, l2=0.0)
```

Smoothness regularizer for spline transformation.

It penalizes the differences of neighbouring coefficients.

__Arguments__

- __diff_order__: neighbouring coefficient difference order
   (2 for second-order differences)
- __l2_smooth__: float; Non-smoothness penalty (penalize w' * S * w)
- __l2__: float; L2 regularization factor - overall weights regularizer
