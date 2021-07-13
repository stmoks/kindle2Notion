
# developed with the help of the following site
# https://realpython.com/nltk-nlp-python/


# import nltk
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')


# from main import KindleClippings
import nltk

from nltk.util import pr
import numpy as np, matplotlib as mpl
from settings import CLIPPINGS_FILE


from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

pos_dict = {'Noun':'NN','Verb':'VB','Pronoun':'NNP','Adjective':'JJ','Adverb':'VBP','Preposition':'VBG','Conjuction':'RB','Intejection':'NNS'}


# ch = KindleClippings(CLIPPINGS_FILE)
corpus =  """
Muad'Dib learned rapidly because his first training was in how to learn.
And the first lesson of all was the basic trust that he could learn.
It's shocking to find how many people do not believe they can learn,
and how many more believe learning to be difficult."""

# for i in range(len(ch.clippings)):
#     corpus += ch.clippings[i]['Clipping'] + "\n"

# tokenizing is a way to split up the sentence into meaningful units that can be analysed
st = sent_tokenize(corpus)
wt = word_tokenize(corpus)

# stop words are removed
stop_words = set(stopwords.words("english"))
filtered_list = [word for word in wt if word.casefold() not in stop_words]
# filtered_list = [word for word in st if word.casefold() not in stop_words]
print(filtered_list)

# next, we employ stemming - the process of reducing words to their roots
stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in filtered_list]
print(stemmed_words)

# tagging the parts of speech to make more sense of the words
tagged_words = nltk.pos_tag(filtered_list)
print(tagged_words)



