import numpy as np
import nltk
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer


def tokenize(sentence):
    #tach tu
    return nltk.word_tokenize(sentence)

def bag_of_words(tokenized_sentence, words):
    sentence_words = [(word) for word in tokenized_sentence]
    # chuyen tu thanh so 0-1
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1
    return bag
