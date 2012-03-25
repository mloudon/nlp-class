import math, collections

class CustomLanguageModel:
    
  GT_MAX=30

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    
    self.unigramFreqs = collections.defaultdict(lambda: 0)
    self.bigramFreqs = collections.defaultdict(lambda: 0)
    
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
            
    for val in self.unigramCounts.values():
        self.unigramFreqs[val] = self.unigramFreqs[val] + 1
    
    for val in self.bigramCounts.values():
        self.bigramFreqs[val] = self.unigramFreqs[val] + 1
        
 

  def gt_cstar(self, k, freq):

      if (k==0):
          return 0.0000270
      
      nk = freq[k]
      if nk == 0:
          return 0.75*k
      
      nkplusone= freq [k+1]
      
      if nkplusone == 0:
          nkplusone = 0.75*(k+1)
    
      kstar = ((k+1)*nkplusone)/float(nk)
      
      if (kstar > k):
        return 0.75*k
      else:
        return kstar


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0 
    for i in range(0,len(sentence)):
      
      bigram_token = '%s:%s'% (sentence[i-1], sentence[i])
      count_bigram = self.bigramCounts[bigram_token]
      
      if i > 0 and count_bigram > 0:
          num = self.gt_cstar(count_bigram, self.bigramFreqs)
          denom = self.gt_cstar(self.unigramCounts[sentence[i-1]], self.unigramFreqs)
      else:
          num = 0.4 *  self.gt_cstar(self.unigramCounts[sentence[i-1]], self.unigramFreqs)
          denom = len(self.unigramCounts) + self.total
      
      score += math.log(num)
      score -= math.log(denom)
      
    return score


