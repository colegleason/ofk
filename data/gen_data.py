import nltk
import json
import re
from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader,stopwords
GROUP_LENGTH = 80
NUM_WORDS = 20
wordlist = PlaintextCorpusReader('', 'ofk(_chap_[1234])?\.txt')

def clean_words(words):
    #convert everything to lower case
    words = [w.lower() for w in words]
    #remove period from end of sentences
    words =  [re.sub('\.','',w) for w in words]
    #only keep alphabetic strings
    words = [w for w in words if w.isalpha()]
    words = [w for w in words if not w in stopwords.words('english')]
    #do stemming "goes" => "go"
    words = [nltk.PorterStemmer().stem(w) for w in words]
    return words

paras = [sum(para, []) for para in wordlist.paras('ofk.txt')]
words = clean_words(wordlist.words('ofk.txt'))
groups = []
for i in range(0, len(paras), GROUP_LENGTH):
    group = sum(paras[i : min(i + GROUP_LENGTH, len(paras))], [])
    groups.append(group)

freqs = []
for group in groups:
    freq = FreqDist(clean_words(group))
    table = {w:freq[w] for w in freq}
    freqs.append(table)

top_words = [w for w in FreqDist(words)][:NUM_WORDS]
def get_word_freqs(word):
    return {'word':word, 'values':[{'x':i, 'y':freqs[i].get(word, 0)} for i in range(len(freqs))]}

output = map(get_word_freqs, top_words)

with open('data.json', 'w') as outfile:
      json.dump(output, outfile, sort_keys = True, indent = 4,
                ensure_ascii=False)
