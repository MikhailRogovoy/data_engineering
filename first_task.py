import re

def read_text(filepath):
    with open(filepath) as file:
        text = file.read()
        return text

def get_words_frequency():
    text = read_text("first_task.txt")
    textlist = re.sub(r'[,.?!\']', '', text).replace('-', ' ').replace('\n', ' ').split(' ')    
    words_frequency = {}

    for word in textlist:
        if (words_frequency.get(word) == None):
            words_frequency[word] = 1
        else:
            words_frequency[word] = words_frequency[word] + 1
    
    with open('first_task_result.txt', 'w+') as file:
        for key in dict(sorted(words_frequency.items(), key = lambda item: item[1], reverse=True)):
            file.write(key + ':' + str(words_frequency[key]) + '\n')

def get_mean_count():
    text = read_text("first_task.txt")
    paragraphs = text.split('\n')
    sentences_list = []
    sentence_count = 0
    
    for sentence in paragraphs:        
        char_count = 0
        for char in sentence:            
            if (char == '.' or char == '?' or char == '!'):
                char_count = char_count + 1
        sentences_list.append(char_count)
        sentence_count = sentence_count + 1

    mean_count = sum(sentences_list)/sentence_count

    with open('first_task_result_variant20.txt', 'w+') as file:
        file.write('Sentences_mean_count: ' + str(mean_count))

get_words_frequency()
get_mean_count()