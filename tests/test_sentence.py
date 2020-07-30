from bleuper import Sentence

class TestSentence:
  text1 = "five am trains broken chains i called you every afternoon"
  text2 = "forrest gump and hurricane trails though we never followed through"
  sent1 = Sentence(text1.split(), (1, 2,))
  sent2 = Sentence(text2.split(), (1, 2, 3, 4,))
  
  def test_tokens(self):
    assert self.sent1.tokens == self.text1.split()
    assert self.sent2.tokens == self.text2.split()
  
  def test_text(self):
    assert self.sent1.text == self.text1
    assert self.sent2.text == self.text2
  
  def test_ngrams1(self):
    assert type(list(self.sent1.counters[1].keys())[0]) == tuple
    
    assert list(self.sent1.counters[1].keys()) == [(word,) for word in self.text1.split(" ")]
    
    assert self.sent1.counters[2][('broken', 'chains',)] == 1
    assert self.sent1.counters[2][('every', 'afternoon',)] == 1
    assert self.sent1.counters[2][('five', 'am',)] == 1
    
    assert self.sent1.counters[2][('hurricane', 'though',)] == 0
  
  def test_ngrams2(self):
    assert self.sent2.counters[3][('forrest', 'gump', 'and',)] == 1
    assert self.sent2.counters[3][('never', 'followed', 'through',)] == 1
    
    assert self.sent2.counters[4][('forrest', 'gump', 'and', 'hurricane',)] == 1
