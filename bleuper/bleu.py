import math
import warnings
from typing import List, Tuple
import sys

from .sentence import Sentence

class BLEU:
  """
  BLEU class takes multiple reference statements and construct a class to check and
  to compute scores for multiple different translated statements. Currently, only
  supports till 4-gram.
  
  Attributes
  ----------
  refs: List[Sentence]
    list of reference sentences
  weights: Tuple[float, float, float, float]
    tuple of weights, ith value represents weight for i-gram
  suppress_warnings: bool
    Whenever a specified n-gram's overlaps are not found, score turns to zero
    and generates a warning. This can be suppressed if this is set to True.

  Example
  -------
  ref1 = ['love', 'can', 'always', 'find', 'a', 'way']
  ref2 = ['love', 'makes', 'anything', 'possible']
  tran1 = ['the', 'love', 'can', 'always', 'do']
  tran2 = ['love', 'can', 'make', 'anything', 'possible']
  b = BLEU([ref1, ref2], (0.4, 0.35, 0.25, 0, ))
  score1 = b.compute_score(tran1)
  score2 = b.compute_score(tran2)
  """
  
  default_wt = (0.25, 0.25, 0.25, 0.25,)
  __MAX_NGRAM = 4
  __EPSILON = 1e-6
  
  def __init__(self, refs: List[List[str]], weights: Tuple[float, float, float, float] = default_wt,
               suppress_warnings: bool = False):
    """
    :param refs: List of list of tokens of reference translations.
    :param weights: tuple of weights, ith value represents weight for i-gram. Sum of weights must be 1.
                    Default: (0.25, 0.25, 0.25, 0.25,)
    :param suppress_warnings: Whenever a specified n-gram's overlaps are not found, score turns to zero
                              and generates a warning. This can be suppressed if this is set to True.
    """
    assert len(refs) > 1, "Must pass at least one reference sentence"
    assert sum(weights) - 1 < BLEU.__EPSILON, "All weights should sum to 1"
    self.ngrams = tuple((i+1) for i in range(BLEU.__MAX_NGRAM) if not (weights[i] < BLEU.__EPSILON))
    self.weights = (0.0,) + weights   # for n-gram consistent indices, wt[1] is for 1-gram, etc.
    self.refs = [Sentence(ref, self.ngrams) for ref in refs]
    self.suppress_warnings = suppress_warnings
  
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
  
  def compute_precision(self, source: Sentence) -> List[float]:
    """
    Computes modified precision. Optimizes by only computing it for useful n-grams,
    that is, n-grams with significant weights.
    :param source: source sentence
    :return: list of precision scores with nth index corresponding to n-gram, provided it is useful, else None.
    """
    precision = [sys.float_info.min] * (BLEU.__MAX_NGRAM + 1)
  
    # computing modified n-gram precision values
    for n in self.ngrams:  # iterating over n-grams
      denom = sum(source.counters[n].values())
    
      numer = sum(
        min(max(r_i.counters[n][gram] for r_i in self.refs), source.counters[n][gram]) for gram in
        source.counters[n].keys())
      if numer == 0:
        numer = sys.float_info.min
        if not self.suppress_warnings:
          warnings.warn(f"No {n}-gram overlaps found. No contribution towards score.")
      
      precision[n] = numer / denom
    
    return precision
  
  def compute_score(self, c: List[str]) -> float:
    """
    Computes BLEU score for translated sentence c with respect
    to the reference sentences and specified weight.
    :param c: List of tokens of translated sentence.
    :return: BLEU score for the translated sentence.
    """
    
    source = Sentence(c, self.ngrams)
    precision = self.compute_precision(source)
    
    # finding closest reference
    len_closest_ref = len(self.find_closest_ref(source))
    
    brevity_penalty = 1 if len(source) >= len_closest_ref else math.exp(1 - len_closest_ref / len(source))
    
    return brevity_penalty * math.exp(sum(self.weights[i] * math.log(p_i)
                                          for (i, p_i) in enumerate(precision[1:], start=1)))


if __name__ == '__main__':
  refs = ["love can always find a way".split(), "love makes anything possible".split()]
  c1 = "the love can always do".split()
  c2 = "love can make anything possible".split()
  bleu = BLEU(refs, weights=(0.5, 0.5, 0, 0,))
  print(bleu.compute_score(c1))
  print(bleu.compute_score(c2))
