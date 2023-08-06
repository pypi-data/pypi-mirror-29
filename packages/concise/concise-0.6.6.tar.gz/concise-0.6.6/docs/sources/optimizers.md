## Weight normalization

For convenience, the wight normalization code from <https://github.com/openai/weightnorm> was added to concise.

***Paper:*** *Weight Normalization: A Simple Reparameterization to Accelerate Training of Deep Neural Networks, by Tim Salimans, and Diederik P. Kingma."*

Note: when using weight-normalization, the model should be initialized with `data_based_init` after compiling:

```python
model.compile(AdamWithweightnorm(), "mse")
data_based_init(model, input)
```

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/optimizers.py#L16)</span>
### SGDWithWeightnorm

```python
keras.optimizers.SGDWithWeightnorm(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
```

----

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/optimizers.py#L87)</span>
### AdamWithWeightnorm

```python
keras.optimizers.AdamWithWeightnorm(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
```

----

### data_based_init


```python
data_based_init(model, input)
```

