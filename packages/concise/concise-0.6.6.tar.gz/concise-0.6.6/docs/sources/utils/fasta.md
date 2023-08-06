### read_fasta


```python
read_fasta(file_path)
```


Read the fasta file as `OrderedDict`

----

### iter_fasta


```python
iter_fasta(file_path)
```


Returns an iterator over the fasta file

Given a fasta file. yield tuples of header, sequence

Code modified from Brent Pedersen's:
"Correct Way To Parse A Fasta File In Python"


__Example__


```python
fasta = fasta_iter("hg19.fa")
for header, seq in fasta:
   print(header)
```

----

### write_fasta


```python
write_fasta(file_path, seq_list, name_list=None)
```


Write a fasta file

__Arguments__

  - __file_path__: file path
  - __seq_list__: List of strings
  - __name_list__: List of names corresponding to the sequences.
If not None, it should have the same length as `seq_list`
