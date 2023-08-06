<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/layers.py#L443)</span>
### SplineT

```python
concise.layers.SplineT(shared_weights=False, kernel_regularizer=None, use_bias=False, kernel_initializer='glorot_uniform', bias_initializer='zeros')
```

Spline transformation layer.

As input, it needs an array of scalars pre-processed by `concise.preprocessing.EncodeSplines`
Specifically, the input/output dimensions are:

- Input: N x ... x channels x n_bases
- Output: N x ... x channels

__Arguments__

- __shared_weights__: bool, if True spline transformation weights
are shared across different features
- __kernel_regularizer__: use `concise.regularizers.SplineSmoother`
other arguments: See `keras.layers.Dense`

----

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/layers.py#L310)</span>
### SplineWeight1D

```python
concise.layers.SplineWeight1D(n_bases=10, spline_degree=3, share_splines=False, l2_smooth=0, l2=0, use_bias=False, bias_initializer='zeros')
```

Up- or down-weight positions in the activation array of 1D convolutions:

`x^{out}_{ijk} = x^{in}_{ijk} + f_S^k(j) \;,`
where f_S is the spline transformation.

__Arguments__

- __n_bases__: int; Number of spline bases used for the positional effect.
- __l2_smooth__: (float) L2 regularization strength for the second
order differences in positional bias' smooth splines. (GAM smoothing regularization)
- __l2__: (float) L2 regularization strength for the spline base coefficients.
- __use_bias__: boolean; should we add a bias to the transition
- __bias_initializer__: bias initializer - from `keras.initializers`

----

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/layers.py#L122)</span>
### ConvSequence

```python
concise.layers.ConvSequence(filters, kernel_size, strides=1, padding='valid', dilation_rate=1, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None, seq_length=None)
```

Convenience wrapper over `keras.layers.Conv1D` with 3 changes:

- additional plotting method: `plot_weights(index=None, plot_type="motif_raw", figsize=None, ncol=1)`
	- **index**: can be a particular index or a list of indicies
	- **plot_type**: Can be one of `"heatmap"`, `"motif_raw"`, `"motif_pwm"` or `"motif_pwm_info"`.
	- **figsize**: tuple, Figure size
	- **ncol**: Number of axis columns
- additional argument `seq_length` instead of `input_shape`
- restriction in build method: `input_shape[-1]` needs to the match the vocabulary size

Clasess `Conv*` all inherit from `ConvSequence` and define the corresponding vocabulary:

- ConvDNA
- ConvRNA
- ConvRNAStructure
- ConvAA
- ConvCodon

----

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/layers.py#L260)</span>
### ConvDNA

```python
concise.layers.ConvDNA(filters, kernel_size, strides=1, padding='valid', dilation_rate=1, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None, seq_length=None)
```

----

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/layers.py#L266)</span>
### ConvRNA

```python
concise.layers.ConvRNA(filters, kernel_size, strides=1, padding='valid', dilation_rate=1, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None, seq_length=None)
```

----

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/layers.py#L278)</span>
### ConvRNAStructure

```python
concise.layers.ConvRNAStructure(filters, kernel_size, strides=1, padding='valid', dilation_rate=1, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None, seq_length=None)
```

----

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/layers.py#L272)</span>
### ConvAA

```python
concise.layers.ConvAA(filters, kernel_size, strides=1, padding='valid', dilation_rate=1, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None, seq_length=None)
```

----

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/layers.py#L284)</span>
### ConvCodon

```python
concise.layers.ConvCodon(filters, kernel_size, strides=1, padding='valid', dilation_rate=1, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None, seq_length=None)
```

----

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/layers.py#L109)</span>
### GlobalSumPooling1D

```python
keras.layers.pooling.GlobalSumPooling1D()
```

Global average pooling operation for temporal data.

__Note__

  - Input shape: 3D tensor with shape: `(batch_size, steps, features)`.
  - Output shape: 2D tensor with shape: `(batch_size, channels)`


----

### InputDNA


```python
InputDNA(seq_length, name=None)
```


Input placeholder for array returned by `encodeDNA` or `encodeRNA`

Wrapper for: `keras.layers.Input((seq_length, 4), name=name, **kwargs)`

----

### InputDNA


```python
InputDNA(seq_length, name=None)
```


Input placeholder for array returned by `encodeDNA` or `encodeRNA`

Wrapper for: `keras.layers.Input((seq_length, 4), name=name, **kwargs)`

----

### InputRNAStructure


```python
InputRNAStructure(seq_length, name=None)
```


Input placeholder for array returned by `encodeRNAStructure`

Wrapper for: `keras.layers.Input((seq_length, 5), name=name, **kwargs)`

----

### InputCodon


```python
InputCodon(seq_length, ignore_stop_codons=True, name=None)
```


Input placeholder for array returned by `encodeCodon`

- __Note__: The seq_length is divided by 3

Wrapper for: `keras.layers.Input((seq_length / 3, 61 or 61), name=name, **kwargs)`

----

### InputAA


```python
InputAA(seq_length, name=None)
```


Input placeholder for array returned by `encodeAA`

Wrapper for: `keras.layers.Input((seq_length, 22), name=name, **kwargs)`

----

### InputSplines


```python
InputSplines(seq_length, n_bases=10, name=None)
```


Input placeholder for array returned by `encodeSplines`

Wrapper for: `keras.layers.Input((seq_length, n_bases), name=name, **kwargs)`
