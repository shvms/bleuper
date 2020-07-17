import math
import warnings
from typing import List, Dict

from .sentence import Sentence
from .function import Function

class BLEU:
  """
  BLEU class takes multiple reference statements and construct a class to check
  to compute scores for multiple different translated statements.
  
  Attributes
  ----------
  refs: List[Sentence]
    list of reference sentences
  weights: Dict[int, float]
    dictionary of (n-gram, weight)
  suppress_warnings: bool
    Whenever a specified n-gram's overlaps are not found, score turns to zero
    and generates a warning. This can be suppressed if this is set to True.

  Example
  -------
  ref1 = ['love', 'can', 'always', 'find', 'a', 'way']
  ref2 = ['love', 'makes', 'anything', 'possible']
  tran1 = ['the', 'love', 'can', 'always', 'do']
  tran2 = ['love', 'can', 'make', 'anything', 'possible']
  b = BLEU([ref1, ref2], {1: 0.4, 2: 0.35, 3: 0.25})
  score1 = b.compute_score(tran1)
  score2 = b.compute_score(tran2)
  """
  
  default_wt = {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25}
  
  def __init__(self, refs: List[List[str]], weights: Dict[int, float] = None, suppress_warnings: bool = False):
    """
    :param refs: List of list of tokens of reference translations.
    :param weights: Dict of ngram-to-weight. Ngram domain: [1,2,3,4]. Sum of weights must be 1.
                    Default: {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25}
    :param suppress_warnings: Whenever a specified n-gram's overlaps are not found, score turns to zero
                              and generates a warning. This can be suppressed if this is set to True.
    """
    if weights is None:
      weights = self.default_wt
    assert len(refs) >= 1, "Must pass at least one reference sentence"
    assert False not in (True if 1 <= n <= 4 else False for n in weights), "Only 1, 2, 3, 4-grams supported"
    assert sum(weights.values()) == 1, "All weights should sum to 1"
    
    self.refs = [Sentence(ref, list(weights.keys())) for ref in refs]
    self.weights = {k: v for (k, v) in weights.items() if v > 1e-6}
    self.suppress_warnings = suppress_warnings
  
  def compute_precision(self, source: Sentence, smoothing: Function = None) -> Dict[int, float]:
    precision = dict()
  
    # computing modified n-gram precision values
    for n in self.weights.keys():  # iterating over n-grams
      denom = sum(source.counters[n].values())
    
      numer = sum(
        min(max(r_i.counters[n][gram] for r_i in self.refs), source.counters[n][gram]) for gram in
        source.counters[n].keys())
      precision[n] = numer / denom
    
    return precision
  
  def find_closest_ref(self, src: Sentence):
    min_dist = abs(len(src) - len(self.refs[0]))
    closest_ref = self.refs[0]
    
    for ref in self.refs:
      curr_dist = abs(len(src) - len(ref))
      
      if curr_dist < min_dist:
        min_dist = curr_dist
        closest_ref = ref
      elif curr_dist == min_dist and len(closest_ref) > len(ref):
        closest_ref = ref
    
    return closest_ref
  
  def compute_score(self, c: List[str]) -> float:
    """
    Computes BLEU score for translated sentence c with respect
    to the reference sentences and specified weight.
    :param c: List of tokens of translated sentence.
    :return: BLEU score for the translated sentence.
    """
    
    source = Sentence(c, list(self.weights.keys()))
    
    precision = self.compute_precision(source)
    
    # finding closest reference
    len_closest_ref = len(self.find_closest_ref(source))
    
    brevity_penalty = 1 if len(source) >= len_closest_ref else math.exp(1 - len_closest_ref / len(source))
    
    # check for 0-precisions
    zero_overlap = False
    for (k, v) in precision.items():
      if precision[k] < 1e-6:
        zero_overlap = True
        if not self.suppress_warnings:
          warnings.warn(f"No {k}-gram overlaps found. No contribution towards score.", UserWarning)
    
    if zero_overlap:
      return 0.0
    
    return brevity_penalty * math.exp(sum(self.weights[n] * math.log(p_i) for (n, p_i) in precision.items()))


if __name__ == '__main__':
  refs = ["love can always find a way".split(), "love makes anything possible".split()]
  c1 = "the love can always do".split()
  c2 = "love can make anything possible".split()
  bleu = BLEU(refs, weights={1: 0.5, 2: 0.5})
  print(bleu.compute_score(c1))
  print(bleu.compute_score(c2))
