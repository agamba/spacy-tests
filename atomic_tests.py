# include all functions and imports
from _util_fnc import *

# load source text data
with open('sample.txt') as f:
    text = f.readlines()

'''
Control variables
'''
tot_s = 0   # total of sentences found: spacy
tot_svo = 0  # total of SVO matches found: textacy
tot_other = 0  # total of sentences proccesed by (ANTO-analysis)
tot_not = 0  # total of sentences NOT accounted for = excluded from dataset
c_bliss_result = {}
c_bliss_text = ""
sentence_error = {}
s_counter = 1

'''
Extract sentences in each paragraph
'''
for paragraph in text:

    '''
    Initialize spaCy NLP 
    '''
    doc = nlp(paragraph)

    # split sentences. Note that furhter analysis is required when using conjunctions
    sentences = list(doc.sents)

    tot_s = len(sentences)

    for sentence in sentences:
        # exclude empty lines
        if (str(sentence) != "\n"):
            print(sentence)
            # check if SVO type of sentence
            sen_SVOTriple = extract_SVO(sentence)

            if (sen_SVOTriple):
                tot_svo = tot_svo + 1
                s_result = analyze_SVO(sen_SVOTriple, sentence)
                print('1. sen_SVOTriple', s_result['CBliss'])
                print("-----")
            else:
                print('1. not sen_SVOTriple')
                print("-----")

            # root_ix = find_root_elem(sentence)
            # if (isNegated(sentence[root_ix])):
            #     print("Is negated !", sentence[root_ix])
            # else:
            #     print(sentence[root_ix])

            svos = findSVOs(sentence)
            print('2. findSVOs', svos)
            # printDeps(sentence)
            print("-----")
            sentence_result = analyze_sentence(sentence)
            print('3. sentence_result', sentence_result['CBliss'])
            # print("-----")
            print("----------")

            # subs = getAllSubs(sentence[root_ix])
            # print('subs: ', subs)
