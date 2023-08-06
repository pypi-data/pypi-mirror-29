Module for retrieving transcription factor PWM's from ENCODE ChiP-seq datasets.

- **URL**: [http://compbio.mit.edu/encode-motifs/](http://compbio.mit.edu/encode-motifs/)
- **Paper**: Pouya Kheradpour and Manolis Kellis; Nucleic Acids Research, 2013 December 13, [doi:10.1093/nar/gkt1249](http://dx.doi.org/10.1093/nar/gkt1249)


### get_metadata


```python
get_metadata()
```


Get pandas.DataFrame with metadata about the PWM's. Columns:

- PWM_id (id of the PWM - pass to get_pwm_list() for getting the pwm
- info1 - additional information about the motifs
- info2
- consensus: PWM consensus sequence

----

### get_pwm_list


```python
get_pwm_list(motif_name_list, pseudocountProb=0.0001)
```


Get a list of ENCODE PWM's.

__Arguments__

- __pwm_id_list__: List of id's from the `PWM_id` column in `get_metadata()` table
- __pseudocountProb__: Added pseudocount probabilities to the PWM

__Returns__

List of `concise.utils.pwm.PWM` instances.

