
# Getting started with concise

## Become familiar with Keras

In order to successfully use Concise, please make sure you are familiar with Keras. I strongly advise everyone to read the excellent [Keras documentation](http://keras.io) first. As a Keras extension, Concise closely follows the Keras API.

## Modules overview

### Pre-processing functions 

Encoding different objects into modeling-ready numpy arrays

- `concise.preprocessing`

### Custom Keras components

- `concise.layers`
- `concise.initializers`
- `concise.regularizers`
- `concise.losses`
- `concise.metrics`

### Hyper-parameter tuning

- `concise.hyopt`
- `concise.eval_metrics`

### SNP-effect prediction

- `concise.effects`

### Other utilities

- `concise.utils`

## Example: RBP binding model in concise

Here we will show a simple use-case with Concise. We will predict the eCLIP binding peaks of the RNA-binding protein (RBP) PUM2.

- eCLIP raw data [ENCODE](https://www.encodeproject.org/search/?type=Experiment&assay_slims=RNA+binding&assay_title=eCLIP)
- eCLIP paper [Van Nostrand *et al*, Nature Meth. 2016](http://www.nature.com/nmeth/journal/v13/n6/full/nmeth.3810.html)
- paper also using this data: [Avsec *et al*, Bioarxiv 2017](http://www.biorxiv.org/content/early/2017/07/18/165183)



```python
%matplotlib inline
import matplotlib.pyplot as plt

import concise.layers as cl
import keras.layers as kl
import concise.initializers as ci
import concise.regularizers as cr
from keras.callbacks import EarlyStopping
from concise.preprocessing import encodeDNA
from keras.models import Model, load_model
```


```python
# get the data
def load(split="train", st=None):
    dt = pd.read_csv("../data/RBP/PUM2_{0}.csv".format(split))
    # DNA/RNA sequence
    xseq = encodeDNA(dt.seq) # list of sequences -> np.ndarray
    # response variable
    y = dt.binding_site.as_matrix().reshape((-1, 1)).astype("float")
    return {"seq": xseq}, y

train, valid, test = load("train"), load("valid"), load("test")

# extract sequence length
seq_length = train[0]["seq"].shape[1]

# get the PWM list for initialization
from concise.data import attract
dfa = attract.get_metadata() # table with PWM meta-info
dfa_pum2 = dfa[dfa.Gene_name.str.match("PUM2") & \
               dfa.Organism.str.match("Homo_sapiens") & \
               (dfa.Experiment_description == "genome-wide in vivo immunoprecipitation")]
pwm_list = attract.get_pwm_list(dfa_pum2.PWM_id.unique()) # retrieve the PWM by id
```


```python
print(pwm_list)
```

    [PWM(name: 129, consensus: TGTAAATA)]



```python
# specify the model
in_dna = cl.InputDNA(seq_length=seq_length, name="seq") # Convenience wrapper around keras.layers.Input()
x = cl.ConvDNA(filters=4, # Convenience wrapper around keras.layers.Conv1D()
               kernel_size=8, 
               kernel_initializer=ci.PSSMKernelInitializer(pwm_list), # intialize the filters on the PWM values
               activation="relu",
               name="conv1")(in_dna)

x = kl.AveragePooling1D(pool_size=4)(x)
x = kl.Flatten()(x)

x = kl.Dense(units=1)(x)
m = Model(in_dna, x)
m.compile("adam", loss="binary_crossentropy", metrics=["acc"])

# train the model
m.fit(train[0], train[1], epochs=5);
```

    Epoch 1/5
    17713/17713 [==============================] - 1s - loss: 0.6779 - acc: 0.8112     
    Epoch 2/5
    17713/17713 [==============================] - 1s - loss: 0.5294 - acc: 0.8260     
    Epoch 3/5
    17713/17713 [==============================] - 1s - loss: 0.4722 - acc: 0.8309     
    Epoch 4/5
    17713/17713 [==============================] - 1s - loss: 0.4353 - acc: 0.8358     
    Epoch 5/5
    17713/17713 [==============================] - 1s - loss: 0.4274 - acc: 0.8374     


Concise is fully compatible with Keras; we can save and load the Keras models (note: `concise` package needs to be imported before loading: `import concise...`).


```python
# save the model
m.save("/tmp/model.h5")

# load the model
m2 = load_model("/tmp/model.h5")
```


```python
# Convenience layers extend the base class (here keras.layers.Conv1D) with .plot_weights for filter visualization
m.get_layer("conv1").plot_weights(plot_type="motif_pwm_info", figsize=(4, 6));
```


    <matplotlib.figure.Figure at 0x7f701cfaf710>



![png](/img/ipynb/getting_started_files/getting_started_11_1.png)


## Used features

### Pre-processing and convenience wrappers

We used `concise.preprocessing.encodeDNA` to convert a list of sequences into a one-hot-encoded array. For each pre-processing function, Concise provides a corresponding Input and Conv1D convenience wrappers. We used the following two in our code:

- `InputDNA` wraps concise.layers.Input and sets the number of channels to 4. 
- `ConvDNA` is a convenience wrapper around Conv1D with the following two modifications:
  - `ConvDNA` checks that the number of input chanels is 4
  - `ConvDNA` has a method for plotting weights: `plot_weights`

Here is a complete list of pre-processors and convenience layers:

|preprocessing| preprocessing type |input layer | convolutional layer| Vocabulary |
|--------------|-------------|-------------|--------------------|------------|
| `encodeDNA` | one-hot| `InputDNA` | `ConvDNA` | `["A", "C", "G", "T"]` |
| `encodeRNA` | one-hot | `InputRNA` | `ConvRNA` | `["A", "C", "G", "U"]` | 
| `encodeCodon` | one-hot, token | `InputCodon` | `ConvCodon` | `["AAA", "AAC", ...]` | 
| `encodeAA`  | one-hot, token| `InputAA` | `ConvAA` | `["A", "R", "N", ...]` |
| `encodeRNAStructure` | probabilities | `InputRNAStructure` | `ConvRNAStructure` | /|
| `encodeSplines` | B-spline basis functions | `InputSplines` | `ConvSplines` | Numerical values|

### PWM initialization

See the PWM initialization notebook in getting-started section of the [concise documentation](https://i12g-gagneurweb.in.tum.de/public/docs/concise/)

### Other features

Check out other notebooks in getting-started section of the [concise documentation](https://i12g-gagneurweb.in.tum.de/public/docs/concise/)
