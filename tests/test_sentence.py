from bleuper import Sentence

class TestSentence:
  text1 = "five am trains broken chains i called you every afternoon"
  text2 = "forrest gump and hurricane trails though we never followed through"
  sent1 = Sentence(text1.split(), ngrams=[1, 2])
  sent2 = Sentence(text2.split(), ngrams=[1, 2, 3, 4])
  
  def test_tokens(self):
    assert self.sent1.tokens == self.text1.split()
    assert self.sent2.tokens == self.text2.split()
  
  def test_text(self):
    assert self.sent1.text == self.text1
    assert self.sent2.text == self.text2
  
  def test_ngrams1(self):
    assert type(self.sent1.ngrams[1][0]) == tuple
    
    assert self.sent1.ngrams[1] == [(word,) for word in self.text1.split(" ")]
    
    assert self.sent1.ngrams[2][3] == ('broken', 'chains', )
    assert self.sent1.ngrams[2][-1] == ('every', 'afternoon',)
    assert self.sent1.ngrams[2][0] == ('five', 'am',)
    
    assert self.sent1.ngrams.get(3, 0) == 0
  
  def test_ngrams2(self):
    assert self.sent2.ngrams[1] == [(word,) for word in self.text2.split(" ")]

    assert self.sent2.ngrams[2][0] == ('forrest', 'gump',)
    assert self.sent2.ngrams[2][3] == ('hurricane', 'trails',)
    assert self.sent2.ngrams[2][-1] == ('followed', 'through',)
    
    assert self.sent2.ngrams[3][0] == ('forrest', 'gump', 'and',)
    assert self.sent2.ngrams[3][4] == ('trails', 'though', 'we',)
    assert self.sent2.ngrams[3][-1] == ('never', 'followed', 'through',)
    
    assert self.sent2.ngrams[4][0] == ('forrest', 'gump', 'and', 'hurricane',)
    assert self.sent2.ngrams[4][4] == ('trails', 'though', 'we', 'never',)
    assert self.sent2.ngrams[4][-1] == ('we', 'never', 'followed', 'through',)
    
    assert self.sent2.ngrams.get(-1, 0) == 0
