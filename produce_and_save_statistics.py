import os
import sys
from collections import defaultdict
import re
from string import maketrans
import json

ABBREVIATION_WORDS = ['St', 'Rd', 'Mr', 'Mrs', 'Ms', 'Dr', 'Prof', 
                      'Sr', 'pp', 'etc', 'Jan', 'Feb', 'Apr', 'Aug', 
                      'Sept', 'Oct', 'Nov', 'Dec', 'Mon', 'Tues', 'Wed',
                      'Thurs', 'Fri', 'Sat', 'Sun', 'sec', 'gm', 'cm', 
                      'kg', 'ft', 'lb', 'oz', 'Tel', 'No', 'no']

GRAMMATIC_ABBREVIATIONS = ['m', 're', 'd', 't', 've', 'll', 's', ]

def normalize_text(text):
    text = text.translate(None, '"$@#%^&*()[]{}')
    return text

def get_texts(directory):
    for subdirectory in os.listdir(directory):
        if not subdirectory.startswith('.'):
            current_directory = directory + '/' + subdirectory
            for doc in os.listdir(current_directory):
                if not doc.startswith('.'):
                    with open(current_directory + '/' + doc) as content:
                        yield normalize_text(content.read())

def get_tokens(text, regex_alphabet):
    there_was_abbreviation = False
    for token in regex_alphabet.findall(text):
        if there_was_abbreviation:
            there_was_abbreviation = False
            continue
        if token in GRAMMATIC_ABBREVIATIONS:
            token = '\'' + token
        if token in ABBREVIATION_WORDS:
            token += '.'
            there_was_abbreviation = True
        yield token
            
def get_trigrams(tokens):
    first_token, second_token = '$', '$'
    for third_token in tokens:
        yield first_token, second_token, third_token
        if third_token in '.?!':
            yield second_token, third_token, '$'
            yield third_token, '$', '$'
            first_token, second_token = '$', '$'
        else:
            first_token, second_token = second_token, third_token

def to_str_defauldict(counter):
    str_defauldict = defaultdict(list)
    for key, value in counter.iteritems():
        str_defauldict[str(key)] = value
    return str_defauldict

def build_model(bigrams, trigrams):
    model = defaultdict(list)
    
    for (token1, token2, token3), frequency in trigrams.iteritems():
        model[token1, token2].append((token3, 1.* frequency / bigrams[token1, token2]))
    return model

def count_words(trigrams, trigram_count, bigram_count):
    for token1, token2, token3 in trigrams:
        bigram_count[token1, token2] += 1
        trigram_count[token1, token2, token3] += 1
        
def produce_statistics(directory, file_for_model):
    pattern = '[a-zA-Z0-9]+|[!]+|[?]+|[.]+|[,]+|[:]+|[;]+'
    regex_alphabet = re.compile(pattern)
    
    trigram_count = defaultdict(int)
    bigram_count = defaultdict(int)
    for text in get_texts(directory):
        count_words(get_trigrams(get_tokens(text, regex_alphabet)), trigram_count, bigram_count)
        
    model = build_model(bigram_count, trigram_count)
    return model
        
def main(directory, file_for_model):
    model = produce_statistics(directory, file_for_model)
    str_model = to_str_defauldict(model)
    
    with open(file_for_model, 'w') as outfile:
        json.dump(str_model, outfile)
        
def main():
    assert len(sys.argv) == 3,  'Usage:  python {} directoryname filename_for_model'.format(sys.argv[0])
    
    directory = sys.argv[1]
    file_for_model = sys.argv[2]
    
    model = produce_statistics(directory, file_for_model)
    str_model = to_str_defauldict(model)
    
    with open(file_for_model, 'w') as outfile:
        json.dump(str_model, outfile)
    
if __name__ == '__main__':
    main()


    
    
    
    
    
    
    