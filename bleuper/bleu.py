import math
from typing import List, Dict

from .sentence import Sentence

class BLEU:
  def __init__(self, refs: List[List[str]], weights: Dict[int, float]):
    """
    :param refs: List of list of tokens of reference translations.
    :param weights: Dict of ngram-to-weight. Ngram domain: [1,2,3,4]. Sum of weights must be 1.
    """
    assert len(refs) > 1, "Must pass at least one reference sentence"
    assert False not in (True if 1 <= n <= 4 else False for n in weights), "Only 1, 2, 3, 4-grams supported"
    assert sum(weights.values()) == 1, "All weights should sum to 1"
    
    self.refs = [Sentence(ref, list(weights.keys())) for ref in refs]
    self.weights = {k: v for (k, v) in weights.items() if v > 1e-6}
  
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
    precision = dict()
    
    # computing modified n-gram precision values
    for n in self.weights.keys():  # iterating over n-grams
      denom = sum(source.counters[n].values())
      
      numer = sum(
        min(max(r_i.counters[n][gram] for r_i in self.refs), source.counters[n][gram]) for gram in
        source.counters[n].keys())
      precision[n] = numer / denom
    
    # finding closest reference
    len_closest_ref = len(self.find_closest_ref(source))
    
    brevity_penalty = 1 if len(source) >= len_closest_ref else math.exp(1 - len_closest_ref / len(source))
    
    # check for 0-precisions
    zero_overlap = False
    for (k, v) in precision.items():
      if precision[k] < 1e-6:
        zero_overlap = True
        print(f"Warning: No {k}-gram overlaps found. No contribution towards score.")
    
    if zero_overlap:
      return 0.0
    
    return brevity_penalty * math.exp(sum(self.weights[n] * math.log(p_i) for (n, p_i) in precision.items()))


if __name__ == '__main__':
  refs = ["love can always find a way".split(), "love makes anything possible".split()]
  c1 = "the love can always do".split()
  c2 = "love can make anything possible".split()
  bleu = BLEU(refs, weights={1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25})
  print(bleu.compute_score(c1))
  print(bleu.compute_score(c2))
