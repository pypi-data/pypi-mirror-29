The variant effect prediction parts integrated in concise are designed to extract importance scores for a single nucleotide variant in a given sequence. Predictions are made for each output individually for a multi-task model. 

## Available functions

### effect_from_model


```python
effect_from_model(model, ref, ref_rc, alt, alt_rc, methods, mutation_positions, out_annotation_all_outputs, extra_args=None)
```


Convenience function to execute multiple effect predictions in one call

__Arguments__

- __model__: Keras model
- __ref__: Input sequence with the reference genotype in the mutation position
- __ref_rc__: Reverse complement of the 'ref' argument
- __alt__: Input sequence with the alternative genotype in the mutation position
- __alt_rc__: Reverse complement of the 'alt' argument
- __methods__: A list of prediction functions to be executed, e.g.: from concise.effects.ism.ism. Using the same
function more often than once (even with different parameters) will overwrite the results of the
previous calculation of that function.
- __mutation_positions__: Position on which the mutation was placed in the forward sequences
- __out_annotation_all_outputs__: Output labels of the model.
- __extra_args__: None or a list of the same length as 'methods'. The elements of the list are dictionaries with
additional arguments that should be passed on to the respective functions in 'methods'. Arguments
defined here will overwrite arguments that are passed to all methods.
- __**argv__: Additional arguments to be passed on to all methods, e.g,: out_annotation.

__Returns__

Dictionary containing the results of the individual calculations, the keys are the
names of the executed functions

----

### gradient_pred


```python
gradient_pred(model, ref, ref_rc, alt, alt_rc, mutation_positions, out_annotation_all_outputs, output_filter_mask=None, out_annotation=None)
```


Gradient-based (saliency) variant effect prediction

Based on the idea of [saliency maps](https://arxiv.org/pdf/1312.6034.pdf) the gradient-based prediction of
variant effects uses the `gradient` function of the Keras backend to estimate the importance of a variant
for a given output. This value is then multiplied by the input, as recommended by
[Shrikumar et al., 2017](https://arxiv.org/pdf/1605.01713.pdf).

__Arguments__

- __model__: Keras model
- __ref__: Input sequence with the reference genotype in the mutation position
- __ref_rc__: Reverse complement of the 'ref' argument
- __alt__: Input sequence with the alternative genotype in the mutation position
- __alt_rc__: Reverse complement of the 'alt' argument
- __mutation_positions__: Position on which the mutation was placed in the forward sequences
- __out_annotation_all_outputs__: Output labels of the model.
- __output_filter_mask__: Mask of boolean values indicating which model outputs should be used.
Use this or 'out_annotation'
- __out_annotation__: List of outputs labels for which of the outputs (in case of a multi-task model) the
predictions should be calculated.

__Returns__


Dictionary with three different entries:

- ref: Gradient * input at the mutation position using the reference sequence.
Forward or reverse-complement sequence is chose based on sequence direction caused
the bigger absolute difference ('diff')
- alt: Gradient * input at the mutation position using the alternative sequence. Forward or
reverse-complement sequence is chose based on sequence direction caused the bigger
absolute difference ('diff')
- diff: 'alt' - 'ref'. Forward or reverse-complement sequence is chose based on sequence
direction caused the bigger absolute difference.

----

### dropout_pred


```python
dropout_pred(model, ref, ref_rc, alt, alt_rc, mutation_positions, out_annotation_all_outputs, output_filter_mask=None, out_annotation=None, dropout_iterations=30)
```


Dropout-based variant effect prediction

This method is based on the ideas in [Gal et al.](https://arxiv.org/pdf/1506.02142.pdf) where dropout
layers are also actived in the model prediction phase in order to estimate model uncertainty. The
advantage of this method is that instead of a point estimate of the model output the distribution of
the model output is estimated.

__Arguments__

- __model__: Keras model
- __ref__: Input sequence with the reference genotype in the mutation position
- __ref_rc__: Reverse complement of the 'ref' argument
- __alt__: Input sequence with the alternative genotype in the mutation position
- __alt_rc__: Reverse complement of the 'alt' argument
- __mutation_positions__: Position on which the mutation was placed in the forward sequences
- __out_annotation_all_outputs__: Output labels of the model.
- __output_filter_mask__: Mask of boolean values indicating which model outputs should be used.
	Use this or 'out_annotation'
- __out_annotation__: List of outputs labels for which of the outputs (in case of a multi-task model) the
	predictions should be calculated.
- __dropout_iterations__: Number of prediction iterations to be performed in order to estimate the
	output distribution. Values greater than 30 are recommended to get a reliable p-value.

__Returns__


Dictionary with a set of measures of the model uncertainty in the variant position. The ones of interest are:

- do_{ref, alt}_mean: Mean of the model predictions given the respective input sequence and dropout.
	- Forward or reverse-complement sequences are chosen as for 'do_pv'.
- do_{ref, alt}_var: Variance of the model predictions given the respective input sequence and dropout.
	- Forward or reverse-complement sequences are chosen as for 'do_pv'.
- do_diff: 'do_alt_mean' - 'do_alt_mean', which is an estimate similar to ISM using diff_type "diff".
- do_pv: P-value of a paired t-test, comparing the predictions of ref with the ones of alt. Forward or
	- reverse-complement sequences are chosen based on which pair has the lower p-value.

----

### ism


```python
ism(model, ref, ref_rc, alt, alt_rc, mutation_positions, out_annotation_all_outputs, output_filter_mask=None, out_annotation=None, diff_type='log_odds', rc_handling='maximum')
```


In-silico mutagenesis

Using ISM in with diff_type 'log_odds' and rc_handling 'maximum' will produce predictions as used
in [DeepSEA](http://www.nature.com/nmeth/journal/v12/n10/full/nmeth.3547.html). ISM offers two ways to
calculate the difference between the outputs created by reference and alternative sequence and two
different methods to select whether to use the output generated from the forward or from the
reverse-complement sequences. To calculate "e-values" as mentioned in DeepSEA the same ISM prediction
has to be performed on a randomised set of 1 million 1000genomes, MAF-matched variants to get a
background of predicted effects of random SNPs.

__Arguments__

- __model__: Keras model
- __ref__: Input sequence with the reference genotype in the mutation position
- __ref_rc__: Reverse complement of the 'ref' argument
- __alt__: Input sequence with the alternative genotype in the mutation position
- __alt_rc__: Reverse complement of the 'alt' argument
- __mutation_positions__: Position on which the mutation was placed in the forward sequences
- __out_annotation_all_outputs__: Output labels of the model.
- __output_filter_mask__: Mask of boolean values indicating which model outputs should be used.
Use this or 'out_annotation'
- __out_annotation__: List of outputs labels for which of the outputs (in case of a multi-task model) the
predictions should be calculated.
- __diff_type__: "log_odds" or "diff". When set to 'log_odds' calculate scores based on log_odds, which assumes
the model output is a probability. When set to 'diff' the model output for 'ref' is subtracted
from 'alt'. Using 'log_odds' with outputs that are not in the range [0,1] nan will be returned.
- __rc_handling__: "average" or "maximum". Either average over the predictions derived from forward and
reverse-complement predictions ('average') or pick the prediction with the bigger absolute
value ('maximum').

__Returns__

Dictionary with the key `ism` which contains a pandas DataFrame containing the calculated values
for each (selected) model output and input sequence

