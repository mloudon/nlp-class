import math, collections

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      
      for i in range(0,len(sentence.data)):  
        datum = sentence.get(i)
        token = datum.word
        self.unigramCounts[token] = self.unigramCounts[token] + 1
        self.total += 1
        
        if i > 0:
            bigram_token = '%s:%s'% (sentence.get(i-1).word, sentence.get(i).word)
            self.bigramCounts[bigram_token] += 1
        

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0 
    for i in range(1,len(sentence)):
      token = sentence[i-1]
      count_unigram = self.unigramCounts[token]
      
      bigram_token = '%s:%s'% (sentence[i-1], sentence[i])
      count_bigram = self.bigramCounts[bigram_token]
      
      
      num = count_bigram + 1
      denom = len(self.unigramCounts) + count_unigram
      
      score += math.log(num)
      score -= math.log(denom)
      
    return score

