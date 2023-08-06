<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/utils/pwm.py#L16)</span>
### PWM

```python
concise.utils.pwm.PWM(pwm, name=None)
```

Class holding the position-weight matrix (PWM)

__Arguments__

   - __pwm__: PWM matrix of shape `(seq_len, 4)`. All elements need to be larger or equal to 0.
   - __name__: str, optional name argument

__Attributes__

- __pwm__: np.array of shape `(seq_len, 4)`. All rows sum to 1
- __name__: PWM name

__Methods__

- **plotPWM(figsize=(10, 2))** - Make a sequence logo plot from the pwm.
	Letter height corresponds to the probability.
- **plotPWMInfo(figsize=(10, 2))** - Make the sequence logo plot with information content
	corresponding to the letter height.
- **get_pssm(background_probs=DEFAULT_BASE_BACKGROUND)** - Get the position-specific scoring matrix (PSSM)
	cumputed as `np.log(pwm / b)`, where b are the background base probabilities..
- **plotPWMInfo(background_probs=DEFAULT_BASE_BACKGROUND, figsize=(10, 2))** - Make the sequence logo plot with
	letter height corresponding to the position-specific scoring matrix (PSSM).
- **normalize()** - force all rows to sum to 1.
- **get_consensus()** - returns the consensus sequence

__Class methods__

- **from_consensus(consensus_seq, background_proportion=0.1, name=None)** - Construct PWM from a consensus sequence
	   - **consensus_seq**: string representing the consensus sequence (ex: ACTGTAT)
	   - **background_proportion**: Let's denote it with a. The row in the resulting PWM
will be: `'C' -> [a/3, a/3, 1-a, a/3]`
	   - **name** - PWM.name.
- **from_background(length=9, name=None, probs=DEFAULT_BASE_BACKGROUND)** - Create a background PWM.


----

### load_motif_db


```python
load_motif_db(filename, skipn_matrix=0)
```


Read the motif file in the following format

```
>motif_name
<skip n>0.1<delim>0.2<delim>0.5<delim>0.6
...
>motif_name2
....
```

Delim can be anything supported by np.loadtxt

__Arguments__

- __filename__: str, file path
- __skipn_matrix__: integer, number of characters to skip when reading
the numeric matrix (for Encode = 2)

__Returns__

Dictionary of numpy arrays

