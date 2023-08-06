Module for retrieving RNA-binding protein (RBP) PWM's from ATtRACT A daTabase of RNA binding proteins and AssoCiated moTifs.

- **URL**: [https://attract.cnic.es/](https://attract.cnic.es/)
- **Paper**: Giudice *et al* 2016: ATtRACT-a database of RNA-binding proteins and associated motifs. [doi:10.1093/database/baw035](https://doi.org/10.1093/database/baw035)


### get_metadata


```python
get_metadata()
```



Get pandas.DataFrame with metadata about the Attract PWM's. Columns:

- PWM_id (id of the PWM - pass to get_pwm_list() for getting the pwm
- Gene_name
- Gene_id
- Mutated	(if the target gene is mutated)
- Organism
- Motif (concsensus motif)
- Len	(lenght of the motif)
- Experiment_description(when available)
- Database (Database from where the motifs were extracted PDB: Protein data bank, C: Cisbp-RNA, R:RBPDB, S: Spliceaid-F, AEDB:ASD)
- Pubmed (pubmed ID)
- Experiment (type of experiment; short description)
- Family (domain)
- Score (Qscore refer to the paper)

----

### get_pwm_list


```python
get_pwm_list(pwm_id_list, pseudocountProb=0.0001)
```


Get a list of Attract PWM's.

__Arguments__

- __pwm_id_list__: List of id's from the `PWM_id` column in `get_metadata()` table
- __pseudocountProb__: Added pseudocount probabilities to the PWM

__Returns__

List of `concise.utils.pwm.PWM` instances.

