### encodeSequence


```python
encodeSequence(seq_vec, vocab, neutral_vocab, maxlen=None, seq_align='start', pad_value='N', encode_type='one_hot')
```


Convert a list of genetic sequences into one-hot-encoded array.

__Arguments__

   - __seq_vec__: list of strings (genetic sequences)
   - __vocab__: list of chars: List of "words" to use as the vocabulary. Can be strings of length>0,
but all need to have the same length. For DNA, this is: ["A", "C", "G", "T"].
   - __neutral_vocab__: list of chars: Values used to pad the sequence or represent unknown-values. For DNA, this is: ["N"].
   - __maxlen__: int or None,
Should we trim (subset) the resulting sequence. If None don't trim.
Note that trims wrt the align parameter.
It should be smaller than the longest sequence.
   - __seq_align__: character; 'end' or 'start'
To which end should we align sequences?
   - __encode_type__: "one_hot" or "token". "token" represents each vocab element as a positive integer from 1 to len(vocab) + 1.
	  neutral_vocab is represented with 0.

__Returns__

Array with shape for encode_type:

- "one_hot": `(len(seq_vec), maxlen, len(vocab))`
- "token": `(len(seq_vec), maxlen)`

If `maxlen=None`, it gets the value of the longest sequence length from `seq_vec`.

----

### pad_sequences


```python
pad_sequences(sequence_vec, maxlen=None, align='end', value='N')
```


Pad and/or trim a list of sequences to have common length. Procedure:

1. Pad the sequence with N's or any other string or list element (`value`)
2. Subset the sequence

__Note__

See also: https://keras.io/preprocessing/sequence/
Aplicable also for lists of characters

__Arguments__

- __sequence_vec__: list of chars or lists
List of sequences that can have various lengths
- __value__: Neutral element to pad the sequence with. Can be `str` or `list`.
- __maxlen__: int or None; Final lenght of sequences.
 If None, maxlen is set to the longest sequence length.
- __align__: character; 'start', 'end' or 'center'
To which end to align the sequences when triming/padding. See examples bellow.

__Returns__

List of sequences of the same class as sequence_vec

__Example__


```python
>>> sequence_vec = ['CTTACTCAGA', 'TCTTTA']
>>> pad_sequences(sequence_vec, 10, align="start", value="N")
['CTTACTCAGA', 'TCTTTANNNN']
>>> pad_sequences(sequence_vec, 10, align="end", value="N")
['CTTACTCAGA', 'NNNNTCTTTA']
>>> pad_sequences(sequence_vec, 4, align="center", value="N")
['ACTC', 'CTTT']
```

----

### encodeDNA


```python
encodeDNA(seq_vec, maxlen=None, seq_align='start')
```


Convert the DNA sequence into 1-hot-encoding numpy array

__Arguments__

- __seq_vec__: list of chars
List of sequences that can have different lengths

- __maxlen__: int or None,
Should we trim (subset) the resulting sequence. If None don't trim.
Note that trims wrt the align parameter.
It should be smaller than the longest sequence.

- __seq_align__: character; 'end' or 'start'
To which end should we align sequences?

__Returns__

3D numpy array of shape (len(seq_vec), trim_seq_len(or maximal sequence length if None), 4)

__Example__


```python
>>> sequence_vec = ['CTTACTCAGA', 'TCTTTA']
>>> X_seq = encodeDNA(sequence_vec, seq_align="end", maxlen=8)
>>> X_seq.shape
(2, 8, 4)

>>> print(X_seq)
[[[0 0 0 1]
  [1 0 0 0]
  [0 1 0 0]
  [0 0 0 1]
  [0 1 0 0]
  [1 0 0 0]
  [0 0 1 0]
  [1 0 0 0]]

 [[0 0 0 0]
  [0 0 0 0]
  [0 0 0 1]
  [0 1 0 0]
  [0 0 0 1]
  [0 0 0 1]
  [0 0 0 1]
  [1 0 0 0]]]
```

----

### encodeRNA


```python
encodeRNA(seq_vec, maxlen=None, seq_align='start')
```


Convert the RNA sequence into 1-hot-encoding numpy array as for encodeDNA

----

### encodeCodon


```python
encodeCodon(seq_vec, ignore_stop_codons=True, maxlen=None, seq_align='start', encode_type='one_hot')
```


Convert the Codon sequence into 1-hot-encoding numpy array

__Arguments__

- __seq_vec__: List of strings/DNA sequences
- __ignore_stop_codons__: boolean; if True, STOP_CODONS are omitted from one-hot encoding.
- __maxlen__: Maximum sequence length. See `pad_sequences` for more detail
- __seq_align__: How to align the sequences of variable lengths. See `pad_sequences` for more detail
- __encode_type__: can be `"one_hot"` or `token` for token encoding of codons (incremental integer ).

__Returns__

numpy.ndarray of shape `(len(seq_vec), maxlen / 3, 61 if ignore_stop_codons else 64)`

----

### encodeAA


```python
encodeAA(seq_vec, maxlen=None, seq_align='start', encode_type='one_hot')
```


Convert the Amino-acid sequence into 1-hot-encoding numpy array

__Arguments__

- __seq_vec__: List of strings/amino-acid sequences
- __maxlen__: Maximum sequence length. See `pad_sequences` for more detail
- __seq_align__: How to align the sequences of variable lengths. See `pad_sequences` for more detail
- __encode_type__: can be `"one_hot"` or `token` for token encoding of codons (incremental integer ).

__Returns__

numpy.ndarray of shape `(len(seq_vec), maxlen, 22)`
