from typing import List, Dict, Tuple
from collections import Counter

class Sentence:
  """
  Represents sentences.
  
  Attributes
  ----------
  text: List[str]
    list of tokens forming sentence
  ngrams_list: List[int]
    tuple of integers representing n-grams to maintain
  counters: Dict[int, Counter]
    dictionary of Counter objects for each n-gram (key).
  
  Example
  -------
  sent = Sentence(["I", "spent", "all", "my", "day", "watching", "netflix"], (1,2,))
  """
  def __init__(self, text: List[str], ngrams_list: Tuple[int, ...]):
    """
    :param text: list of tokens forming sentence
    :param ngrams_list: list of integers representing n-grams to maintain
    """
    self.tokens = [w.lower() for w in text]
    self.counters: Dict[int, Counter] = dict()
    
    self.__generateCounters(ngrams_list)
  
  @property
  def text(self):
    """
    :return: returns joined text
    """
    return ' '.join(self.tokens)
  
  @staticmethod
  def __getNgram(tokens: List[str], n: int) -> List[Tuple[str]]:
    """
    Generates n-gram from list of tokens.
    :param tokens: list of tokens
    :param n:
    :return: list of n-grams
    """
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]
  
  def __generateCounters(self, ngrams_list: Tuple[int, ...]):
    """
    Generates counters
    :param ngrams_list: tuple of integers representing n-grams to maintain
    :return:
    """
    for n in ngrams_list:
      self.counters[n] = Counter(Sentence.__getNgram(self.tokens, n))
  
  def __str__(self):
    return str(self.tokens)
  
  def __len__(self):
    return len(self.tokens)
  
  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.tokens == other.tokens
