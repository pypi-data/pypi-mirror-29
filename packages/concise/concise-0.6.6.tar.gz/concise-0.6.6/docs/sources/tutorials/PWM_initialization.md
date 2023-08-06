
## Initializing filters on known motifs

In the scenario where data is scarse, it is often useful to initialize the filters of the first convolutional layer to some known position weights matrices (PWM's). That way, the model already starts with a parameter configuration much closer to the 'right' one.

Concise provides access to 3 PWM databases:

- transcription factors from ENCODE (2067 PWMs)
- transcription factors from HOCOMOCO v10 (640 PWMs)
- rna-binding proteins from ATtrACT (1583 PWMs)

### Find the motif of interest

Each PWM database is provided as a module under `concise.data`. It provides two functions:

- `concise.data.<db>.get_metadata()` - returns a pandas.DataFrame with metadata information about each PWM 
- `concise.data.<db>.get_pwm_list()` - given a list of PWM ids, return a list with `concise.utils.pwm.PWM` instances

#### Metadata tables


```python
%matplotlib inline
import matplotlib.pyplot as plt
```


```python
# RBP PWM's
from concise.data import attract

dfa = attract.get_metadata()
dfa
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
      <th>PWM_id</th>
      <th>Gene_name</th>
      <th>Gene_id</th>
      <th>Mutated</th>
      <th>Organism</th>
      <th>Motif</th>
      <th>Len</th>
      <th>Experiment_description</th>
      <th>Database</th>
      <th>Pubmed</th>
      <th>Experiment_description.1</th>
      <th>Family</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>519</td>
      <td>3IVK</td>
      <td>3IVK</td>
      <td>no</td>
      <td>Mus_musculus</td>
      <td>GAAACA</td>
      <td>6</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>19965478</td>
      <td>X-RAY DIFFRACTION</td>
      <td>NaN</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>1</th>
      <td>574</td>
      <td>3IVK</td>
      <td>3IVK</td>
      <td>no</td>
      <td>Mus_musculus</td>
      <td>UGGG</td>
      <td>4</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>19965478</td>
      <td>X-RAY DIFFRACTION</td>
      <td>NaN</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>2</th>
      <td>464</td>
      <td>4KZD</td>
      <td>4KZD</td>
      <td>no</td>
      <td>Mus_musculus</td>
      <td>GAAAC</td>
      <td>5</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>24952597</td>
      <td>X-RAY DIFFRACTION</td>
      <td>NaN</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4879</th>
      <td>1396</td>
      <td>HNRNPAB</td>
      <td>ENSG00000197451</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>AUAGCA</td>
      <td>6</td>
      <td>In vitro splicing assays</td>
      <td>AEDB</td>
      <td>12426391</td>
      <td>other</td>
      <td>RRM</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>4880</th>
      <td>1397</td>
      <td>HNRNPA1</td>
      <td>ENSG00000135486</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UAGG</td>
      <td>4</td>
      <td>Immunoprecipitation;U...</td>
      <td>AEDB</td>
      <td>15506926</td>
      <td>UV cross-linking</td>
      <td>RRM</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>4881</th>
      <td>1398</td>
      <td>PTBP1</td>
      <td>ENSG00000011304</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UUCUUC</td>
      <td>6</td>
      <td>In vivo splicing assa...</td>
      <td>AEDB</td>
      <td>14966131</td>
      <td>UV cross-linking</td>
      <td>RRM</td>
      <td>1.000000**</td>
    </tr>
  </tbody>
</table>
<p>4882 rows × 13 columns</p>
</div>




```python
# TF PWM's
from concise.data import encode

dfe = encode.get_metadata()
dfe
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
      <th>PWM_id</th>
      <th>info1</th>
      <th>info2</th>
      <th>consensus</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AFP_1</td>
      <td>AFP1_transfac_M00616</td>
      <td>None</td>
      <td>ATTAACTACAC</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AHR::ARNT::HIF1A_1</td>
      <td>AhR,-Arnt,-HIF-1_tran...</td>
      <td>None</td>
      <td>TGCGTGCGG</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AHR::ARNT_1</td>
      <td>AhR:Arnt_transfac_M00235</td>
      <td>None</td>
      <td>TAAGGGTTGCGTGCCC</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2064</th>
      <td>ZSCAN4_3</td>
      <td>ZSCAN4_jolma_full_M54</td>
      <td>None</td>
      <td>TGCACACACTGAAAA</td>
    </tr>
    <tr>
      <th>2065</th>
      <td>fake_AACGSSAA</td>
      <td>None</td>
      <td>None</td>
      <td>AACGCCAA</td>
    </tr>
    <tr>
      <th>2066</th>
      <td>fake_AAGCSSAA</td>
      <td>None</td>
      <td>None</td>
      <td>AAGCCCAA</td>
    </tr>
  </tbody>
</table>
<p>2067 rows × 4 columns</p>
</div>




```python
# TF PWM's
from concise.data import hocomoco

dfh = hocomoco.get_metadata()
dfh
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
      <th>PWM_id</th>
      <th>TF</th>
      <th>Organism</th>
      <th>DB</th>
      <th>info</th>
      <th>consensus</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AHR_HUMAN.H10MO.B</td>
      <td>AHR</td>
      <td>HUMAN</td>
      <td>H10MO</td>
      <td>B</td>
      <td>GTTGCGTGC</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AIRE_HUMAN.H10MO.C</td>
      <td>AIRE</td>
      <td>HUMAN</td>
      <td>H10MO</td>
      <td>C</td>
      <td>ATTGGTTATATTGGTTAA</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ALX1_HUMAN.H10MO.B</td>
      <td>ALX1</td>
      <td>HUMAN</td>
      <td>H10MO</td>
      <td>B</td>
      <td>ATAATTGAATTA</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>637</th>
      <td>ZN784_HUMAN.H10MO.D</td>
      <td>ZN784</td>
      <td>HUMAN</td>
      <td>H10MO</td>
      <td>D</td>
      <td>GAGGTAGGTAC</td>
    </tr>
    <tr>
      <th>638</th>
      <td>ZSC16_HUMAN.H10MO.D</td>
      <td>ZSC16</td>
      <td>HUMAN</td>
      <td>H10MO</td>
      <td>D</td>
      <td>GAGGTGTTCTGTTAACACTA</td>
    </tr>
    <tr>
      <th>639</th>
      <td>ZSCA4_HUMAN.H10MO.D</td>
      <td>ZSCA4</td>
      <td>HUMAN</td>
      <td>H10MO</td>
      <td>D</td>
      <td>AGTGTGTGCACT</td>
    </tr>
  </tbody>
</table>
<p>640 rows × 6 columns</p>
</div>



Let's choose PUM2 PWM (RBP in Human):


```python
dfa_pum2 = dfa[dfa.Gene_name.str.match("PUM2") & \
               dfa.Organism.str.match("Homo_sapiens")]
dfa_pum2
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
      <th>PWM_id</th>
      <th>Gene_name</th>
      <th>Gene_id</th>
      <th>Mutated</th>
      <th>Organism</th>
      <th>Motif</th>
      <th>Len</th>
      <th>Experiment_description</th>
      <th>Database</th>
      <th>Pubmed</th>
      <th>Experiment_description.1</th>
      <th>Family</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2603</th>
      <td>503</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUAAAUA</td>
      <td>8</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>21397187</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PUF</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>2604</th>
      <td>361</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUACAUC</td>
      <td>8</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>21397187</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PUF</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>2605</th>
      <td>514</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUAGAUA</td>
      <td>8</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PDB</td>
      <td>21397187</td>
      <td>X-RAY DIFFRACTION</td>
      <td>PUF</td>
      <td>1.000000**</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2613</th>
      <td>107</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUAUAUA</td>
      <td>8</td>
      <td>PAR-clip</td>
      <td>C</td>
      <td>20371350</td>
      <td>genome-wide in vivo i...</td>
      <td>PUF</td>
      <td>0.250000**</td>
    </tr>
    <tr>
      <th>2614</th>
      <td>107</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUACAUA</td>
      <td>8</td>
      <td>PAR-clip</td>
      <td>C</td>
      <td>20371350</td>
      <td>genome-wide in vivo i...</td>
      <td>PUF</td>
      <td>0.250000**</td>
    </tr>
    <tr>
      <th>2615</th>
      <td>107</td>
      <td>PUM2</td>
      <td>ENSG00000055917</td>
      <td>no</td>
      <td>Homo_sapiens</td>
      <td>UGUAGAUA</td>
      <td>8</td>
      <td>PAR-clip</td>
      <td>C</td>
      <td>20371350</td>
      <td>genome-wide in vivo i...</td>
      <td>PUF</td>
      <td>0.250000**</td>
    </tr>
  </tbody>
</table>
<p>13 rows × 13 columns</p>
</div>



#### Visualization - PWM class

The `PWM` class provides a method `plotPWM` to visualize the PWM.


```python
# Visualize the PUM2 Motifs from different experiments
from concise.utils.pwm import PWM
dfa_pum2_uniq = dfa_pum2[["Experiment_description", "PWM_id"]].drop_duplicates()
pwm_list = attract.get_pwm_list(dfa_pum2_uniq.PWM_id)
```


```python
for i, pwm in enumerate(pwm_list):
    print("PWM_id:", pwm.name, "; Experiment_description:", dfa_pum2_uniq.Experiment_description.iloc[i])
    pwm.plotPWM(figsize=(3,1))
```

    PWM_id: 503 ; Experiment_description: X-RAY DIFFRACTION
    PWM_id: 361 ; Experiment_description: X-RAY DIFFRACTION
    PWM_id: 514 ; Experiment_description: X-RAY DIFFRACTION
    PWM_id: 116 ; Experiment_description: RIP-chip
    PWM_id: 129 ; Experiment_description: genome-wide in vivo immunoprecipitation
    PWM_id: 107 ; Experiment_description: PAR-clip



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_12_1.png)



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_12_2.png)



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_12_3.png)



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_12_4.png)



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_12_5.png)



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_12_6.png)


We can select the PWM with id 129.


```python
pwm_list = [pwm for pwm in pwm_list if pwm.name == "129"]
```


```python
pwm_list
```




    [PWM(name: 129, consensus: TGTAAATA)]



### Initialize the conv filters with PWM values


```python
import concise.layers as cl
import keras.layers as kl
import concise.initializers as ci
import concise.regularizers as cr
from keras.callbacks import EarlyStopping
from concise.preprocessing import encodeDNA
from keras.models import Model, load_model
from keras.optimizers import Adam
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

# deduce sequence length
seq_length = train[0]["seq"].shape[1]
```


```python
# define the model
def model(train, filters=1, kernel_size=9, pwm_list=None, lr=0.001):
    seq_length = train[0]["seq"].shape[1]
    if pwm_list is None:
        kinit = "glorot_uniform"
        binit = "zeros"
    else:
        kinit = ci.PSSMKernelInitializer(pwm_list, add_noise_before_Pwm2Pssm=True)
        binit = "zeros"
        
    # sequence
    in_dna = cl.InputDNA(seq_length=seq_length, name="seq")
    x = cl.ConvDNA(filters=filters, 
                   kernel_size=kernel_size, 
                   activation="relu",
                   kernel_initializer=kinit,
                   bias_initializer=binit,
                   name="conv1")(in_dna)
    x = kl.AveragePooling1D(pool_size=4)(x)
    x = kl.Flatten()(x)
    
    x = kl.Dense(units=1)(x)
    m = Model(in_dna, x)
    m.compile(Adam(lr=lr), loss="binary_crossentropy", metrics=["acc"])
    return m
```

`ci.PSSMKernelInitializer` will set the filters of the first convolutional layer to the values of the position-specific scoring matrix (PSSM):

$$ pssm_{ij} = log \frac{pwm_{ij}}{b_j} \;,$$

where $b_j$ is the background probability of observing base $j$.

We add gaussian noise to each individual filter. Let's visualize the filters:


```python
# create two models: with and without PWM initialization
m_rand_init = model(train, filters=3, pwm_list=None) # random initialization
m_pwm_init = model(train, filters=3, pwm_list=pwm_list) # motif initialization
```


```python
print("Random initialization:")
m_rand_init.get_layer("conv1").plot_weights(figsize=(3, 5));
```

    Random initialization:



    <matplotlib.figure.Figure at 0x7f9003607208>



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_22_2.png)



```python
print("Known PWM initialization:")
m_pwm_init.get_layer("conv1").plot_weights(figsize=(3, 5));
```

    Known PWM initialization:



    <matplotlib.figure.Figure at 0x7f8f965565f8>



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_23_2.png)



```python
# train the models
m_rand_init.fit(train[0], train[1], epochs=50, validation_data=valid, 
                verbose=0,
                callbacks=[EarlyStopping(patience=5)])
```




    <keras.callbacks.History at 0x7f8f9b78ce48>




```python
m_pwm_init.fit(train[0], train[1], epochs=50, validation_data=valid, 
                verbose=0,
                callbacks=[EarlyStopping(patience=5)]);
```

### Test-set performance


```python
import concise.eval_metrics as cem
```


```python
# performance on the test-set
# Random initialization
print("Random intiailzation auPR:", cem.auprc(test[1], m_rand_init.predict(test[0])))
# PWM initialization
print("Known PWM initialization auPR:", cem.auprc(test[1], m_pwm_init.predict(test[0])))
```

    Random intiailzation auPR: 0.580103849926
    Known PWM initialization auPR: 0.713372711603


### Filter visualization


```python
m_rand_init.get_layer("conv1").plot_weights(plot_type="motif_pwm_info", figsize=(3, 5));
```


    <matplotlib.figure.Figure at 0x7f8f9b7d0fd0>



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_30_1.png)



```python
m_pwm_init.get_layer("conv1").plot_weights(plot_type="motif_pwm_info", figsize=(3, 5));
```


    <matplotlib.figure.Figure at 0x7f8f9b94c4e0>



![png](/img/ipynb/PWM_initialization_files/PWM_initialization_31_1.png)


## Benefits of motif initialization

- Interpretatbility
  - we can use fewer filters and know that the major effect will be captured by the first filters
    - handy when studying the model parameters
- Better predictive performance
- More stable training
