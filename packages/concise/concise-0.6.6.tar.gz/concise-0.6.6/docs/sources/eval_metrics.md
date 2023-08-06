Global evaluation metrics. Similar to `concise.metrics` or `keras.metrics` but implemented with numpy and intended to be used on the *whole dataset* after training the model. Many evaluation metrics (AUC, F1, ...) namely can't be expressed as an average over minibatches and are hence not implemented in `keras.metrics` (see [this](https://github.com/fchollet/keras/issues/5794) discussion).

***Note:*** All the metrics mask values -1 for classification and `np.nan` for regression.

## Available evaluation metrics

### cat_acc


```python
cat_acc(y_true, y_pred)
```


Categorical accuracy

----

### cor


```python
cor(y_true, y_pred)
```


Compute Pearson correlation coefficient.

----

### kendall


```python
kendall(y_true, y_pred, nb_sample=100000)
```


Kendall's tau coefficient, Kendall rank correlation coefficient

----

### mad


```python
mad(y_true, y_pred)
```


Median absolute deviation

----

### rmse


```python
rmse(y_true, y_pred)
```


Root mean-squared error

----

### rrmse


```python
rrmse(y_true, y_pred)
```


1 - rmse

----

### mse


```python
mse(y_true, y_pred)
```


Mean squared error

----

### ermse


```python
ermse(y_true, y_pred)
```


Exponentiated root-mean-squared error

----

### var_explained


```python
var_explained(y_true, y_pred)
```


Fraction of variance explained.

----

### auc


```python
auc(y_true, y_pred, round=True)
```


Area under the ROC curve

----

### auprc


```python
auprc(y_true, y_pred)
```


Area under the precision-recall curve

----

### accuracy


```python
accuracy(y_true, y_pred, round=True)
```


Classification accuracy

----

### tpr


```python
tpr(y_true, y_pred, round=True)
```


True positive rate `tp / (tp + fn)`

----

### tnr


```python
tnr(y_true, y_pred, round=True)
```


True negative rate `tn / (tn + fp)`

----

### mcc


```python
mcc(y_true, y_pred, round=True)
```


Matthews correlation coefficient

----

### f1


```python
f1(y_true, y_pred, round=True)
```


F1 score: `2 * (p * r) / (p + r)`, where p=precision and r=recall.

