import sys
from collections import defaultdict
import numpy as np
import json
from ast import literal_eval as make_tuple

def open_model_file(file_name):
    with open(file_name) as data_file:
        model = json.load(data_file)
    print 'read model!'
    model = {make_tuple(str(key)): value for key, value in model.iteritems()}
    print 'convert model!'
    return model

def generate_sentence(model):
    sentence = ''
    token1, token2 = '$', '$'
    while True:
        third_tokens_and_frequency = map(list, zip(*model[token1, token2]))
        third_tokens = third_tokens_and_frequency[0]
        frequency = third_tokens_and_frequency[1]
        token1, token2 = token2, np.random.choice(third_tokens, 1, frequency)
        token2 = token2[0]
        if token2 == '$':
            break
        if token2 in '!?.,:;' or token1 == '$' or token2.startswith('\''):
            sentence += token2
        else:
            sentence += ' ' + token2
    return sentence

def generate_random_text(model, min_size):
    random_text = []
    current_size = 0
    current_paragraph_size = int(10 + 10 * np.random.randn())
    while current_size < min_size:
        print current_size, min_size
        if current_paragraph_size == 0:
            random_text.append('\n\n')
            current_paragraph_size = int(10 + 10 * np.random.randn())
            if current_paragraph_size < 1:
                current_paragraph_size = 1
        current_sentence = generate_sentence(model)
        current_size += len(current_sentence.split())
        random_text.append(current_sentence)
        current_paragraph_size -= 1
    random_text = ' '.join(random_text)
    return random_text

def main():
    assert len(sys.argv) == 3,  'Usage:  python {} model_filename min_size_of_text'.format(sys.argv[0])
    
    model_filename = sys.argv[1]
    min_size = sys.argv[2]
    
    model = open_model_file(model_filename)
    print 'model is read!'
    print generate_random_text(model, min_size)

    
if __name__ == '__main__':
    main()
    
    
    
    
    
    