from typing import List, Dict, Tuple
from collections import Counter

class Sentence:
  def __init__(self, text: List[str], ngrams: List[int]):
    self.tokens = [w.lower() for w in text]
    self.ngrams: Dict[int, List[Tuple[str]]] = dict()
    self.counters: Dict[int, Counter] = dict()
    
    self.__generateNgrams(ngrams)
    self.__generateCounters(ngrams)
  
  @property
  def text(self):
    return ' '.join(self.tokens)
  
  @staticmethod
  def __getNgram(tokens: List[str], n: int):
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]
  
  def __generateNgrams(self, ngrams_list: List[int]):
    for n in ngrams_list:
      self.ngrams[n] = Sentence.__getNgram(self.tokens, n)
  
  def __generateCounters(self, ngrams_list: List[int]):
    for n in ngrams_list:
      self.counters[n] = Counter(self.ngrams[n])
  
  def __str__(self):
    return str(self.tokens)
  
  def __len__(self):
    return len(self.tokens)
  
  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.tokens == other.tokens
