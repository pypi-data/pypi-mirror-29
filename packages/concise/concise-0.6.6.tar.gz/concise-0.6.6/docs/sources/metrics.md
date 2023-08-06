`concise.metrics` provides a masked version of `keras.metrics` for classification (mask value = -1) and introduces additional metrics. ***Note:*** Be careful when using the additional metrics (`f1`, `precision`, ...). For those, the average accross minibatches is namely not equal to the metric evaluated on the whole dataset.

## Available metrics

### contingency_table


```python
contingency_table(y, z)
```


Note:  if y and z are not rounded to 0 or 1, they are ignored

----

### sensitivity


```python
sensitivity(y, z)
```


True positive rate `tp / (tp + fn)`

----

### specificity


```python
specificity(y, z)
```


True negative rate `tn / (tn + fp)`

----

### fpr


```python
fpr(y, z)
```


False positive rate `fp / (fp + tn)`

----

### fnr


```python
fnr(y, z)
```


False negative rate `fn / (fn + tp)`

----

### precision


```python
precision(y, z)
```


Precision `tp / (tp + fp)`

----

### fdr


```python
fdr(y, z)
```


False discovery rate `fp / (tp + fp)`

----

### accuracy


```python
accuracy(y, z)
```


Classification accuracy `(tp + tn) / (tp + tn + fp + fn)`

----

### f1


```python
f1(y, z)
```


F1 score: `2 * (p * r) / (p + r)`, where p=precision and r=recall.

----

### mcc


```python
mcc(y, z)
```


Matthews correlation coefficient

----

### cat_acc


```python
cat_acc(y, z)
```


Classification accuracy for multi-categorical case

----

### var_explained


```python
var_explained(y_true, y_pred)
```


Fraction of variance explained.

