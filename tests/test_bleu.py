import pytest
import json
from typing import List
from bleuper import BLEU, Sentence

with open('tests/dataset/refs.en.json', encoding='utf-8') as file:
  pytest.refs = json.load(file)

with open('tests/dataset/trans.en.json', encoding='utf-8') as file:
  pytest.trans = json.load(file)

with open('tests/dataset/weights.json', encoding='utf-8') as file:
  pytest.weights = json.load(file)

with open('tests/dataset/core.en.json', encoding='utf-8') as file:
  pytest.core = json.load(file)

class TestBLEU:

  @staticmethod
  def helper_get_tokens(text: str) -> List[str]:
    return [word for word in text.lower().split()]
  
  def test_refs_length_constraints(self):
    with pytest.raises(AssertionError):
      BLEU([], (0.5, 0.5, 0, 0,))
  
  def test_ngrams_constraints(self):
    with pytest.raises(AssertionError):
      BLEU([["hello", "world"]], (0.25, 0.25, 0.15, 0.15, 0.2,))
  
  def test_weights_constraints(self):
    with pytest.raises(AssertionError):
      BLEU([["hello", "world"]], (0.5, 0, 0.6, 0,))
  
  def test_refs(self):
    b = BLEU(refs=[TestBLEU.helper_get_tokens(pytest.refs[12]['text']), TestBLEU.helper_get_tokens(pytest.refs[13]['text'])],
             weights=(0.25, 0.25, 0.25, 0.25,), suppress_warnings=True)
    assert type(b.refs[0]) == Sentence
  
  def test_closest_ref(self):
    b = BLEU(refs=[TestBLEU.helper_get_tokens(pytest.refs[12]['text']),
                   TestBLEU.helper_get_tokens(pytest.refs[13]['text'])],
                   weights=(0.25, 0.25, 0.25,0.25,), suppress_warnings=True)
    src = Sentence(TestBLEU.helper_get_tokens(pytest.trans[13]['text']), (1,))
    assert b.find_closest_ref(src).text == pytest.refs[13]['text']
  
  @pytest.mark.parametrize("case", pytest.core)
  def test_compute_score(self, case):
    refs = [TestBLEU.helper_get_tokens(pytest.refs[idx]['text']) for idx in case['ref']]
    weights = tuple(pytest.weights[case['weight']]['weight'])
    b = BLEU(refs, weights, suppress_warnings=True)
    
    src = TestBLEU.helper_get_tokens(pytest.trans[case['trans']]['text'])
    
    program_score = b.compute_score(src)
    
    assert abs(program_score - case['bleu']) < 1e-6
