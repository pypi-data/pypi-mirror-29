
# Spline transformation in CONCISE

This notebook will demonstrate the use of [spline transformation](http://www.biorxiv.org/content/early/2017/07/18/165183) in CONCISE.

## B-splines crash course

Core component of spline transformation are B-splines (See [Splines, Knots and Penalties](http://statweb.lsu.edu/faculty/marx/SKiP.pdf) by Eilers and and Marx). Here is how they look like and how to compute them with concise.


```python
%matplotlib inline
import matplotlib.pyplot as plt
from concise.utils.splines import BSpline
from concise.preprocessing import EncodeSplines # uses BSpline
```

    Using TensorFlow backend.



```python
def plot_order(degree, ax):
    x = np.linspace(0, 1, 100).reshape((-1,1))
    y = EncodeSplines(n_bases=10, degree=degree).fit_transform(x).squeeze() 
    # alternatively: y = BSpline(0, 1, 10, degree).predict(x)
    ax.plot(x, y)
    ax.set(title="Degree: {d}, order: {o}".format(d=degree, o=degree+1))
```


```python
fig, ax = plt.subplots(nrows=4)
fig.tight_layout()
for i in range(ax.shape[0]):
    plot_order(i, ax[i])
```


![png](/img/ipynb/spline_transformation_files/spline_transformation_5_0.png)


We can see that for degree=0, they are just segmenting the range into equally-sized bins.

## Generalized additive models with Keras

Let's see how to fit a simple smooth curve, as usually done with generalized additive models (using say [mgcv](https://cran.r-project.org/web/packages/mgcv/) package in R).


```python
# some data
x = np.linspace(1, 15)
y_true = np.sin(x)
y = y_true + np.random.normal(scale=0.3, size=len(x))

plt.scatter(x,y);
```


![png](/img/ipynb/spline_transformation_files/spline_transformation_8_0.png)



```python
import concise.layers as cl
import concise.regularizers as cr
import keras.layers as kl
from keras.models import Model, Sequential
from keras.optimizers import Adam
```


```python
# pre-processor
x_spl = EncodeSplines(n_bases=10).fit_transform(x.reshape((-1,1)))
```


```python
x_spl.shape
```




    (50, 1, 10)




```python
# keras model
m = Sequential([
        cl.SplineT(input_shape=x_spl.shape[1:])
    ])
m.compile(Adam(lr=0.1), "mse")
```


```python
m.fit(x_spl, y, epochs=10, verbose=0);
```


```python
plt.scatter(x,y)
plt.plot(x, m.predict(x_spl));
```


![png](/img/ipynb/spline_transformation_files/spline_transformation_14_0.png)


### Smoothness regularizaion

The advantage of penalized B-splines (P-splines) is that we can use a large number of spline knots with smoothness regularization. In concise, this is achieved by adding a regularizer to the `SplineT` layer: `concise.regularizers.SplineSmoother(diff_order=2, l2_smooth=0.0, l2=0.0)`.


```python
def fit_lines(x, n_bases=10, l2_smooth=0, diff_order=2):
    # train the pre-processor
    es = EncodeSplines(n_bases=n_bases)
    es.fit(x.reshape((-1,1)))
    
    # train the model
    x_spl = es.transform(x.reshape((-1,1)))
    m = Sequential([
            cl.SplineT(kernel_regularizer=cr.SplineSmoother(diff_order=diff_order, # Smoothness regularization
                                                            l2_smooth=l2_smooth),
                       input_shape=x_spl.shape[1:])
                    ])
    m.compile(Adam(lr=0.1), "mse")
    m.fit(x_spl, y, epochs=150, verbose=0)
    
    # denser grid to predict
    x_pred = np.linspace(x.min(), x.max(), num=100)
    return x_pred, m.predict(es.transform(x_pred.reshape((-1,1))))
```


```python
# Generate data
x = np.linspace(1, 15, num=20)
y_true = np.sin(x)
y = y_true + np.random.normal(scale=0.3, size=len(x))
```


```python
l2s_list = [0, 10]
y_pred_l = [fit_lines(x, n_bases=50, l2_smooth=l2s) for l2s in l2s_list]
```


```python
plt.scatter(x,y)
for i, (x_pred, y_pred) in enumerate(y_pred_l):
    plt.plot(x_pred, y_pred, label=l2s_list[i])
plt.legend(title="l2_smooth");    
```


![png](/img/ipynb/spline_transformation_files/spline_transformation_19_0.png)


## SplineT in sequence-based models

Let's show a simple use-case of spline transformation in the context of DNA sequence-based models. The core idea is to have, in addition to sequence, a scalar vector along the sequence encoding distances to some genomic landmarks. For simplicity, we will here consider the distance within the sequence. 

We will use a simple simulated dataset, where multiple TTAATGA motifs were embeded in the sequence and the response was computed as the sum of the position-dependent motif effects:

$$ f_{pos} (x) = 0.3*\frac{1}{\sqrt{2 \pi 0.01}} \exp{\{- \frac{(x - 0.2)^2}{0.02}\}} + 0.05 \sin(15 x) + 0.8 \;,$$

where $x\in[0,1]$ is the position within the sequence.


```python
from scipy.stats import norm
pef = lambda x: 0.3*norm.pdf(x, 0.2, 0.1) + 0.05*np.sin(15*x) + 0.8
```


```python
positions = np.arange(499)
pos_effect_theoretical = pef(positions/positions.max())
plt.plot(pos_effect_theoretical);
plt.xlabel("Position")
plt.ylabel("Pos. effect");
```


![png](/img/ipynb/spline_transformation_files/spline_transformation_22_0.png)



```python
from concise.preprocessing import encodeDNA
from concise.utils.pwm import PWM
import concise.initializers as ci
from keras.callbacks import EarlyStopping
```


```python
# Load the data
data_dir = "../data/"
dt = pd.read_csv(data_dir + "/01-fixed_seq_len-1.csv")
motifs = ["TTAATGA"]
dt
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>y</th>
      <th>seq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5.4763</td>
      <td>TTCTGGGAGGCGTCCTTACGT...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.2309</td>
      <td>AAGTATGATCATACGCACCGT...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>6.0881</td>
      <td>TATGCAGGATCGAAATACTCT...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2997</th>
      <td>0.2773</td>
      <td>GAGGGGTCAGCATGCGTATGA...</td>
    </tr>
    <tr>
      <th>2998</th>
      <td>15.6793</td>
      <td>CTACCAAATCCAAACTTCAGC...</td>
    </tr>
    <tr>
      <th>2999</th>
      <td>13.0256</td>
      <td>CTGACCATACGTTTCACACCG...</td>
    </tr>
  </tbody>
</table>
<p>3000 rows × 2 columns</p>
</div>




```python
# Create arrays for model training
x_seq = encodeDNA(dt["seq"])
y = dt.y.as_matrix()
seq_length = x_seq.shape[1]

x_seq.shape # (n_samples, seq_length, n_bases)
```




    (3000, 500, 4)




```python
# positional track
x_pos = np.repeat(np.arange(seq_length).reshape((1,-1)), y.shape[0], axis=0)
x_pos[:5]
```




    array([[  0,   1,   2, ..., 497, 498, 499],
           [  0,   1,   2, ..., 497, 498, 499],
           [  0,   1,   2, ..., 497, 498, 499],
           [  0,   1,   2, ..., 497, 498, 499],
           [  0,   1,   2, ..., 497, 498, 499]])




```python
# default data-format for SplineT positions is: (N_batch, seq_length, channels)
x_pos = x_pos.reshape((-1, seq_length, 1)) 
x_pos.shape
```




    (3000, 500, 1)




```python
# transform positions with the EncodeSplines pre-processor
es = EncodeSplines(n_bases=10)
x_pos_spl = es.fit_transform(x_pos)
# This adds a new axis n_bases to the end
x_pos_spl.shape
```




    (3000, 500, 1, 10)




```python
# Compile the training set
train = {"seq": x_seq, "pos": x_pos_spl}, y
```


```python
# To make the task easier, we will initialize the filters 
# of the conv layer to the simulated motif
pwm_list = [PWM.from_consensus(motif) for motif in motifs]
motif_width = 7
print(pwm_list)
pwm_list[0].plotPWM(figsize=(3,0.5));
```

    [PWM(name: None, consensus: TTAATGA)]



![png](/img/ipynb/spline_transformation_files/spline_transformation_30_1.png)



```python
def model_SplineT(n_bases=10):
    """Create Keras model based on two data inputs: sequence and scalar-vector along the sequence"""
    np.random.seed(42)

    # DNA input
    input_dna = cl.InputDNA(seq_length, name="seq")
    
    # Positions input
    input_pos = kl.Input((seq_length, 1, n_bases), name="pos")

    # Sequence module
    x_seq = cl.ConvDNA(filters=1, 
                       kernel_size=motif_width, ## motif width
                       activation="relu", 
                       # motif initialization
                       kernel_initializer=ci.PSSMKernelInitializer(pwm_list),
                       bias_initializer=ci.PSSMBiasInitializer(pwm_list,
                                                               kernel_size=motif_width, 
                                                               mean_max_scale=0.99),
                       padding="same",
                       name="conv_dna",
                       ## mean_max_scale of 1 means that only consensus sequence gets score larger than 0
                      )(input_dna)
    
    # Positional module
    x_pos = cl.SplineT(kernel_regularizer=cr.SplineSmoother(l2_smooth=1e-3), 
                       kernel_initializer="zeros",
                       name="SplineT")(input_pos)
    x_pos = kl.Lambda(lambda x: 1 + x)(x_pos)
    
    # Merge
    x = kl.multiply([x_seq, x_pos])
    x = cl.GlobalSumPooling1D()(x)
    x = kl.Dense(units=1,activation="linear")(x)
    model = Model(inputs=[input_dna, input_pos], outputs=x)

    # compile the model
    model.compile(optimizer=Adam(lr=0.1), loss="mse")
    return model
```


```python
# Get the compiled model
np.random.seed(42)
m = model_SplineT()
```


```python
# Train
np.random.seed(42)
m.fit(train[0], train[1],
      epochs=30, verbose=2,
      callbacks=[EarlyStopping(patience=5)],
      validation_split=.2);
```

    Train on 2400 samples, validate on 600 samples
    Epoch 1/30
    0s - loss: 2.4880 - val_loss: 1.7815
    Epoch 2/30
    0s - loss: 1.7226 - val_loss: 1.5614
    Epoch 3/30
    0s - loss: 1.6402 - val_loss: 1.5303
    Epoch 4/30
    0s - loss: 1.7361 - val_loss: 1.6460
    Epoch 5/30
    0s - loss: 1.7810 - val_loss: 1.5749
    Epoch 6/30
    0s - loss: 1.8376 - val_loss: 1.5673
    Epoch 7/30
    0s - loss: 1.7018 - val_loss: 1.9090
    Epoch 8/30
    0s - loss: 1.6653 - val_loss: 1.6473
    Epoch 9/30
    0s - loss: 1.7693 - val_loss: 1.5478



```python
## visualize the effect
w_pos = m.get_layer("SplineT").get_weights()[0]
x_pos_single = train[0]["pos"][0,:,0,:]
```


```python
plt.plot(1 + np.dot(x_pos_single, np.ravel(w_pos)))
plt.plot(pos_effect_theoretical);
plt.ylabel('Positional effect')
plt.xlabel('Position')
plt.title("Positional effect")
plt.legend(labels=["Inferred", "Theoretical"]);
```


![png](/img/ipynb/spline_transformation_files/spline_transformation_35_0.png)


### Convenience function: SplineWeight1D

Concise provides a shortcut to modelling internal positions: `SplineWeight1D`.


```python
def model_SplineWeight1D():
    np.random.seed(42)
    model = Sequential([
                cl.ConvDNA(filters=1, 
                       kernel_size=motif_width, ## motif width
                       activation="relu", 
                       kernel_initializer=ci.PSSMKernelInitializer(pwm_list),
                       bias_initializer=ci.PSSMBiasInitializer(pwm_list,kernel_size=motif_width, mean_max_scale=0.99),
                       padding="same",
                       name="conv_dna",
                       seq_length=seq_length
                       ## mean_max_scale of 1 means that only consensus sequence gets score larger than 0
                      ),
                cl.SplineWeight1D(n_bases=10, l2_smooth=1e-3, l2=0, name="spline_weight"),
                cl.GlobalSumPooling1D(),
                kl.Dense(units=1,activation="linear")
        ])
    model.compile(optimizer=Adam(lr=0.1), loss="mse")
    return model
```


```python
# Train
np.random.seed(42)
m = model_SplineWeight1D()
m.fit(train[0]["seq"], train[1],
      epochs=30, verbose=2,
      callbacks=[EarlyStopping(patience=5)],
      validation_split=.2);
```

    Train on 2400 samples, validate on 600 samples
    Epoch 1/30
    0s - loss: 2.4785 - val_loss: 1.8418
    Epoch 2/30
    0s - loss: 1.6359 - val_loss: 1.5540
    Epoch 3/30
    0s - loss: 1.6398 - val_loss: 1.6543
    Epoch 4/30
    0s - loss: 1.6762 - val_loss: 1.4844
    Epoch 5/30
    0s - loss: 1.7411 - val_loss: 1.6224
    Epoch 6/30
    0s - loss: 1.9801 - val_loss: 1.8591
    Epoch 7/30
    0s - loss: 1.8632 - val_loss: 1.6679
    Epoch 8/30
    0s - loss: 1.8000 - val_loss: 1.5397
    Epoch 9/30
    0s - loss: 1.6719 - val_loss: 1.7291
    Epoch 10/30
    0s - loss: 1.6877 - val_loss: 1.7287



```python
# plot
m.get_layer("spline_weight").plot() # layer also has a plotting method
plt.plot(positions, pos_effect_theoretical - 1)
plt.ylabel('Positional effect')
plt.xlabel('Position')
plt.title("Positional effect")
plt.legend(labels=["Inferred", "Theoretical"]);
```


![png](/img/ipynb/spline_transformation_files/spline_transformation_39_0.png)

