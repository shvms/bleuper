# bleuper
A simple lightweight library to help you easily compute BLEU scores.
## Usage
```python
from bleuper import BLEU
ref1 = ['love', 'can', 'always', 'find', 'a', 'way']
ref2 = ['love', 'makes', 'anything', 'possible']
tran1 = ['the', 'love', 'can', 'always', 'do']
tran2 = ['love', 'can', 'make', 'anything', 'possible']
b = BLEU([ref1, ref2], (0.4, 0.35, 0.25, 0, ))
score1 = b.compute_score(tran1)
score2 = b.compute_score(tran2)
```
