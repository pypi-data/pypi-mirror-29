
# Variant effect prediction
The variant effect prediction parts integrated in `concise` are designed to extract importance scores for a single nucleotide variant in a given sequence. Predictions are made for each output individually for a multi-task model. In this short tutorial we will be using a small model to explain the basic functionality and outputs.

At the moment there are three different effect scores to be chosen from. All of them require as in input:

* The input sequence with the variant with its reference genotype
* The input sequence with the variant with its alternative genotype
* Both aformentioned sequences in reverse-complement
* Information on where (which basepair, 0-based) the mutation is placed in the forward sequences

The following variant scores are available:

* In-silico mutagenesis (ISM):
	- Predict the outputs of the sequences containing the reference and alternative genotype of the variant and use the differential output as a effect score.

* Gradient-based score
* Dropout-based score

## Calculating effect scores
Firstly we will need to have a trained model and a set of input sequences containing the variants we want to look at. For this tutorial we will be using a small model:


```python
from effect_demo_setup import *
from concise.models import single_layer_pos_effect as concise_model
import numpy as np

# Generate training data for the model, use a 1000bp sequence
param, X_feat, X_seq, y, id_vec = load_example_data(trim_seq_len = 1000)

# Generate the model
dc = concise_model(pooling_layer="sum",
                   init_motifs=["TGCGAT", "TATTTAT"],
                   n_splines=10,
                   n_covariates=0,
                   seq_length=X_seq.shape[1],
                   **param)

# Train the model
dc.fit([X_seq], y, epochs=1,
       validation_data=([X_seq], y))
    
# In order to select the right output of a potential multitask model we have to generate a list of output labels, which will be used alongside the model itself.
model_output_annotation = np.array(["output_1"])
```

    Using TensorFlow backend.


    Removing 1 pwm's from pwm_list
    Removing 1 pwm's from pwm_list
    Train on 3713 samples, validate on 3713 samples
    Epoch 1/1
    3713/3713 [==============================] - 2s - loss: 0.4300 - mean_squared_error: 0.4299 - val_loss: 0.2329 - val_mean_squared_error: 0.2328


As with any prediction that you want to make with a model it is necessary that the input sequences have to fit the input dimensions of your model, in this case the reference and alternative sequences in their forward and reverse-complement state have to have the shape [?, 1000, 4].

We will be storing the dataset in a dictionary for convenience:


```python
import h5py

dataset_path = "%s/data/sample_hqtl_res.hdf5"%concise_demo_data_path
dataset = {}
with h5py.File(dataset_path, "r") as ifh:
    ref = ifh["test_in_ref"].value
    alt = ifh["test_in_alt"].value
    dirs = ifh["test_out"]["seq_direction"].value
    
    # This datset is stored with forward and reverse-complement sequences in an interlaced manner
    assert(dirs[0] == b"fwd")
    dataset["ref"] = ref[::2,...]
    dataset["alt"] = alt[::2,...]
    dataset["ref_rc"] = ref[1::2,...]
    dataset["alt_rc"] = alt[1::2,...]
    dataset["y"] = ifh["test_out"]["type"].value[::2]
    
    # The sequence is centered around the mutatiom with the mutation occuring on position when looking at forward sequences
    dataset["mutation_position"] = np.array([500]*dataset["ref"].shape[0])
```

All prediction functions have the same general set of required input values. Before going into more detail of the individual prediction functions We will look into how to run them. The following input arguments are availble for all functions:

	model: Keras model
	ref: Input sequence with the reference genotype in the mutation position
	ref_rc: Reverse complement of the 'ref' argument
	alt: Input sequence with the alternative genotype in the mutation position
	alt_rc: Reverse complement of the 'alt' argument
	mutation_positions: Position on which the mutation was placed in the forward sequences
	out_annotation_all_outputs: Output labels of the model.
	out_annotation: Select for which of the outputs (in case of a multi-task model) the predictions should be calculated.

The `out_annotation` argument is not required. We will now run the available predictions individually.


```python
from concise.effects.ism import ism
from concise.effects.gradient import gradient_pred
from concise.effects.dropout import dropout_pred

ism_result = ism(model = dc, 
                 ref = dataset["ref"], 
                 ref_rc = dataset["ref_rc"], 
                 alt = dataset["alt"], 
                 alt_rc = dataset["alt_rc"], 
                 mutation_positions = dataset["mutation_position"], 
                 out_annotation_all_outputs = model_output_annotation, diff_type = "diff")
gradient_result = gradient_pred(model = dc, 
                                ref = dataset["ref"], 
                                ref_rc = dataset["ref_rc"], 
                                alt = dataset["alt"], 
                                alt_rc = dataset["alt_rc"], 
                                mutation_positions = dataset["mutation_position"], 
                                out_annotation_all_outputs = model_output_annotation)
dropout_result = dropout_pred(model = dc, 
                              ref = dataset["ref"], 
                              ref_rc = dataset["ref_rc"], 
                              alt = dataset["alt"], alt_rc = dataset["alt_rc"], mutation_positions = dataset["mutation_position"], out_annotation_all_outputs = model_output_annotation)
```

    Removing 1 pwm's from pwm_list
    Removing 1 pwm's from pwm_list


    /home/avsec/bin/anaconda3/lib/python3.5/site-packages/scipy/stats/_distn_infrastructure.py:879: RuntimeWarning: invalid value encountered in greater
      return (self.a < x) & (x < self.b)
    /home/avsec/bin/anaconda3/lib/python3.5/site-packages/scipy/stats/_distn_infrastructure.py:879: RuntimeWarning: invalid value encountered in less
      return (self.a < x) & (x < self.b)
    /home/avsec/bin/anaconda3/lib/python3.5/site-packages/scipy/stats/_distn_infrastructure.py:1818: RuntimeWarning: invalid value encountered in less_equal
      cond2 = cond0 & (x <= self.a)
    /home/avsec/bin/anaconda3/lib/python3.5/site-packages/concise/effects/dropout.py:183: RuntimeWarning: invalid value encountered in greater
      sel = (np.abs(prob) > np.abs(prob_rc)).astype(np.int)  # Select the LOWER p-value among fwd and rc



```python
gradient_result
```




    {'alt':      output_1
     0      0.0051
     1      0.0051
     2      0.0000
     ..        ...
     753    0.0048
     754    0.0037
     755    0.0096
     
     [756 rows x 1 columns], 'diff':      output_1
     0      0.0051
     1      0.0051
     2     -0.0050
     ..        ...
     753    0.0048
     754   -0.0010
     755    0.0060
     
     [756 rows x 1 columns], 'ref':      output_1
     0      0.0000
     1      0.0000
     2      0.0050
     ..        ...
     753    0.0000
     754    0.0047
     755    0.0036
     
     [756 rows x 1 columns]}



The output of all functions is a dictionary, please refer to the individual chapters further on for an explanation of the individual values. Every dictionary contains pandas dataframes as values. Every column of the dataframe is named according to the values given in the `out_annotation_all_outputs` labels and contains the respective predicted scores.

### Convenience function
For convenience there is also a function available which enables the execution of all functions in one call.
Additional arguments of the `effect_from_model` function are:

	methods: A list of prediction functions to be executed. Using the same function more often than once (even with different parameters) will overwrite the results of the previous calculation of that function.
	extra_args: None or a list of the same length as 'methods'. The elements of the list are dictionaries with additional arguments that should be passed on to the respective functions in 'methods'. Arguments defined here will overwrite arguments that are passed to all methods.
	**argv: Additional arguments to be passed on to all methods, e.g,: out_annotation.


```python
from concise.effects.snp_effects import effect_from_model

# Define the parameters:
params = {"methods": [gradient_pred, dropout_pred, ism],
         "model": dc,
         "ref": dataset["ref"],
         "ref_rc": dataset["ref_rc"],
         "alt": dataset["alt"],
         "alt_rc": dataset["alt_rc"],
         "mutation_positions": dataset["mutation_position"],
         "extra_args": [None, {"dropout_iterations": 60},
         		{"rc_handling" : "maximum", "diff_type":"diff"}],
         "out_annotation_all_outputs": model_output_annotation,
         }

results = effect_from_model(**params)
```

Again the returned value is a dictionary containing the results of the individual calculations, the keys are the names of the executed functions:


```python
print(results.keys())
```

## ISM

`concise.effects.ism.ism`

ISM offers two ways to calculate the difference between the outputs created by reference and alternative sequence and two different methods to select whether to use the output generated from the forward or from the reverse-complement sequences. You will have to choose those parameters according to your model design:

	diff_type: "log_odds" or "diff". When set to 'log_odds' calculate scores based on log_odds, which assumes the model output is a probability. When set to 'diff' the model output for 'ref' is subtracted from 'alt'. Using 'log_odds' with outputs that are not in the range [0,1] nan will be returned.
	rc_handling: "average" or "maximum". Either average over the predictions derived from forward and reverse-complement predictions ('average') or pick the prediction with the bigger absolute value ('maximum').
	
This function returns a dictionary with the key `ism` which contains a pandas DataFrame containing the calculated values for each (selected) model output and input sequence. Using ISM in with diff_type 'log_odds' and rc_handling 'maximum' will produce predictions as used in [DeepSEA](http://www.nature.com/nmeth/journal/v12/n10/full/nmeth.3547.html). To calculate "e-values" as mentioned in DeepSEA the same ISM prediction has to be performed on a randomised set of 1 million 1000genomes, MAF-matched variants to get a background of predicted effects of random SNPs.

## Gradient
`concise.effects.gradient.gradient_pred`

Based on the idea of [saliency maps](https://arxiv.org/pdf/1312.6034.pdf) the gradient-based prediction of variant effects uses the `gradient` function of the Keras backend to estimate the importance of a variant for a given output. This value is then multiplied by the input, as recommended by [Shrikumar et al., 2017](https://arxiv.org/pdf/1605.01713.pdf).

This function returns a dictionary with three different entries:

	ref: Gradient * input at the mutation position using the reference sequence. Forward or reverse-complement sequence is chose based on sequence direction caused the bigger absolute difference ('diff')
	alt: Gradient * input at the mutation position using the alternative sequence. Forward or reverse-complement sequence is chose based on sequence direction caused the bigger absolute difference ('diff')
	diff: 'alt' - 'ref'. Forward or reverse-complement sequence is chose based on sequence direction caused the bigger absolute difference.
	

## Dropout
`concise.effects.dropout.dropout_pred`

This method is based on the ideas in [Gal et al.](https://arxiv.org/pdf/1506.02142.pdf) where dropout layers are also actived in the model prediction phase in order to estimate model uncertainty. The advantage of this method is that instead of a point estimate of the model output the distribution of the model output is estimated. This function has one additional parameter:

	dropout_iterations: Number of prediction iterations to be performed in order to estimate the output distribution. Values greater than 30 are recommended to get a reliable p-value.
	
This function returns a dictionary with a set of measures of the model uncertainty in the variant position. The ones of interest are:

	do_{ref, alt}_mean: Mean of the model predictions given the respective input sequence and dropout. Forward or reverse-complement sequences are chosen as for 'do_pv'.
	do_{ref, alt}_var: Variance of the model predictions given the respective input sequence and dropout. Forward or reverse-complement sequences are chosen as for 'do_pv'.
	do_diff: 'do_alt_mean' - 'do_alt_mean', which is an estimate similar to ISM using diff_type "diff".
	do_pv: P-value of a paired t-test, comparing the predictions of ref with the ones of alt. Forward or reverse-complement sequences are chosen based on which pair has the lower p-value.
	
The values in 'do_pv' should be used as score, where the lowest p-values indicate the strongest and most certain predicted effect. The p-values will be nan if the difference in means and variance for reference and alternative sequence are zero.
