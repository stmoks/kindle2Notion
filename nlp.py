
# developed with the help of the following site
# https://realpython.com/nltk-nlp-python/



# nltk.download('stopwords') -- download stopwords
# nltk.download('averaged_perceptron_tagger') - download parts of speech taggers
# nltk.download('tagsets') - download part of speech tagger descriptions
# nltk.download("maxent_ne_chunker") - download named entities list
# nltk.download("words")

# from main import KindleClippings
import nltk


import numpy as np, matplotlib as mpl
from settings import CLIPPINGS_FILE

from nltk.util import pr
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk import FreqDist


pos_dict = {'CC':'Conjuection','DT':'Determiner','IN':'Prepopsition','JJ':'Ordinal adjective','JJR':'Comparative adjective','JJS':'Superlative adjective','NN':'Singular/Mass common noun','NNP':'Singular proper noun','NNPS':'Plural proper noun','NNS':'Plural common noun','PRP':'Personal pronoun','PRP$':'Personal pronoun','RB':'Adverb','RBR':'Comaprative adverb','RBS':'Superlative adverb','RP':'Participle','UH':'Interjection','VB':'Verb','VBD':'Verb past tense','VBG':'Verb, present participle or gerund','VBP':'Present tense verb','VBZ':'Present tense verb'}


# ch = KindleClippings(CLIPPINGS_FILE)
corpus =  '''
Muad'Dib learned rapidly because his first training was in how to learn.
And the first lesson of all was the basic trust that he could learn.
It's shocking to find how many people do not believe they can learn,
and how many more believe learning to be difficult Frodo, Michael Jackson, Apple, Elon Musk.'''

# for i in range(len(ch.clippings)):
#     corpus += ch.clippings[i]['Clipping'] + "\n"

# tokenizing is a way to split up the sentence into meaningful units that can be analysed
st = sent_tokenize(corpus)
wt = word_tokenize(corpus)

# stop words are removed
stop_words = set(stopwords.words('english'))
filtered_list = [word for word in wt if word.casefold() not in stop_words]
# filtered_list = [word for word in st if word.casefold() not in stop_words]
print(filtered_list)

# next, we employ stemming - the process of reducing words to their roots
stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in filtered_list]
print(stemmed_words)

# tagging the parts of speech to make more sense of the words
tagged_words = nltk.pos_tag(filtered_list)

# next, pull out named entities
#todo named entities change, need to find a way to refresh using a dynamic source
def extract_ne(tags):
     tree = nltk.ne_chunk(tags, binary=True)
     print(tree)
     print(type(tree))
     return set(' '.join(i[0] for i in t)
         for t in tree
         if hasattr(t, 'label') and t.label() == 'NE'
     )

# def extract_ne(tags):
#      tree = nltk.ne_chunk(tags, binary=True)
#      return set(" ".join(i[0] for i in ['sadf','frodo'])
#      )

named_entities_list = extract_ne(tagged_words)
print(f'The named entities: {named_entities_list}')

# a frequency distribution to determine which words appear the most
frequency_distribution = FreqDist(filtered_list)
print(frequency_distribution)
print(frequency_distribution.most_common(20))
frequency_distribution.plot(20, cumulative=False)


#todo
# add collocations
# deconstruct return comprehension thing






