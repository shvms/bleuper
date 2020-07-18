import abc
import math
from fractions import Fraction
from typing import Dict, Union, List
from .sentence import Sentence


class Function(metaclass=abc.ABCMeta):
  """
  An interface for all smoothing functions
  """
  
  @classmethod
  def __subclasshook__(cls, subclass):
    return hasattr(subclass, 'compute') and callable(subclass.compute)
  
  def __init__(self, epsilon):
    self.epsilon = epsilon
  
  @abc.abstractmethod
  def compute(self, precisions: Dict[int, Fraction]) -> Dict[int, Union[float, Fraction]]:
    return NotImplemented


class SmoothFunc1(Function):
  """
  if n-gram overlaps correspond to zero, it resets them to epsilon
  """
  
  def compute(self, precisions: Dict[int, Fraction]) -> Dict[int, Union[float, Fraction]]:
    return {
      k: (v.numerator + self.epsilon) / v.denominator
      for k, v in precisions.items()
    }


class SmoothFunc2(Function):
  def compute(self, precisions: Dict[int, Fraction]) -> Dict[int, Union[float, Fraction]]:
    return {
      k: Fraction(v.numerator + 1, v.denominator + 1)
      if k != 1 else v
      for k, v in precisions.items()
    }


class SmoothFunc3(Function):
  def compute(self, precisions: Dict[int, Fraction]) -> Dict[int, Union[float, Fraction]]:
    invcnt = 1
    newPrecisions = dict()
    for k, v in precisions.items():
      if v.numerator == 0:
        newPrecisions[k] = 1 / (v.denominator * (1 << invcnt))
        invcnt += 1
      else:
        newPrecisions[k] = v
    
    return newPrecisions


class SmoothFunc4(Function):
  def __init__(self, epsilon, k, trans: Sentence):
    super().__init__(epsilon)
    assert len(trans) == 0, "Provided translated sentence length has length 0."
    
    self.k = k
    self.trans = trans
  
  def compute(self, precisions: Dict[int, Fraction]) -> Dict[int, Union[float, Fraction]]:
    invcnt = 1
    factor = math.log(k / len(self.trans))
    newPrecisions = dict()
    
    for k, v in precisions.items():
      if v.numerator == 0:
        invcnt *= factor
        newPrecisions[k] = 1 / (v.denominator * invcnt)
      else:
        newPrecisions[k] = v
    
    return newPrecisions
