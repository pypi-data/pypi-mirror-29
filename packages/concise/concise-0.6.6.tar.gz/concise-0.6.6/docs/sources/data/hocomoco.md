Module for retrieving transcription factor PWM's from HOCOMOCO database.

- **URL**: <http://hocomoco.autosome.ru/>
- **Paper**: Kulakovskiy *et al* 2015, HOCOMOCO: expansion and enhancement of the collection of transcription factor binding sites models: [doi:10.1093/nar/gkv1249](https://doi.org/10.1093/nar/gkv1249)


### get_metadata


```python
get_metadata()
```



Get pandas.DataFrame with metadata about the PWM's. Columns:

- PWM_id (id of the PWM - pass to get_pwm_list() for getting the pwm
- TF
- Organism
- DB
- Info
- consensus

----

### get_pwm_list


```python
get_pwm_list(pwm_id_list, pseudocountProb=0.0001)
```


Get a list of HOCOMOCO PWM's.

__Arguments__

- __pwm_id_list__: List of id's from the `PWM_id` column in `get_metadata()` table
- __pseudocountProb__: Added pseudocount probabilities to the PWM

__Returns__

List of `concise.utils.pwm.PWM` instances.

