import spacy
from _util_fnc import *
from spacy import displacy

nlp = spacy.load("en_core_web_lg")
# nlp.add_pipe("merge_noun_chunks")
# nlp.add_pipe("merge_entities")

handled_pos = ["ADV", "NOUN", "PRON", "PROPN", "ADJ", "DET"]

# load source text data
with open('sample.txt') as f:
# with open('data/tests/aux_verbs.txt') as f:
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
s_counter = 1

def find_root_of_sentence(doc):
    # print('--> find_root_of_sentence')
    root_token = None
    for w in doc:
        # print(w.i, w, w.pos_, w.dep_, w.dep_, spacy.explain(w.dep_))
        # print("\tsubtree", list(w.subtree))
        # print("\tchildren", list(w.children))
        # print("\tancestors", list(w.ancestors))
        if (w.dep_ == "ROOT"):
            root_token = w
    return root_token


def rewrite_root_subtree(root_token, sentence):
    # print('--> rewrite_root_subtree')
    new_sentence = []
    verbs = []
    collected_tokens_i_all = []
    for w in list(root_token.subtree):
        if(config['show_token_info']):
            print(w.i, w, w.pos_, w.dep_, w.lemma_)
        # check for types and apply conversions

        if (w.pos_ == "VERB"):
            # check for verb tense

            tense_result = find_verb_tense(w, sentence, w.i)
            # print("tense_result: ", tense_result)
            verb_is_negated = isNegated(w)

            # find adverbs
            result = find_adverbs_for_verb(w)
            subject = result[0]
            verb_adv = result[1]
            collected_tokens_i = result[2]
            # print("verb_adv: ", w, "\t", verb_adv)
            # rewrite tense + verb + adverbs structure

            new_verb_advs = "[" + tense_result['tense'] + "]" + "["+subject + \
                "]" + "" + tense_result['verb'] + "" + " ".join(verb_adv) + "]"

            # add to sentence chunk to new_sentence array
            new_sentence.append(new_verb_advs)

            # add collected token ids
            for new_added_i in collected_tokens_i:
                collected_tokens_i_all.append(new_added_i)

        elif (w.pos_ == "NOUN" or w.pos_ == "PROPN" or w.pos_ == "PRON"):
            result = get_noun_adj_from_subtree(w)
            # print("--> result", result)
            noun_chunk = result[0]
            collected_tokens_i = result[1]
            # print('noun_chunk', noun_chunk)
            # print('collected_tokens_i', collected_tokens_i)
            # print('noun_chunk', noun_chunk)
            # print('result NOUN', result)
            new_sentence.append(noun_chunk)

            for new_added_i in collected_tokens_i:
                collected_tokens_i_all.append(new_added_i)

        # TODO:exclude all other types of POD
        # add all other tokens not added by previous functions, and not ADV, NOUN, P
        elif (w.i not in collected_tokens_i_all and w.pos_ not in handled_pos):
            new_sentence.append(w)
    return new_sentence


def find_adverbs_for_verb(verb_token):
    # print('--> find_adverbs_for_verb:', verb_token)
    collected_tokens_i = []
    advs = []
    subject = ""
    for w in list(verb_token.subtree):
        ancestors = list(w.ancestors)
        # check if is and ADV or ADJ? and first ancestor is the target verb_token
        if (w.pos_ == "ADV" and ancestors[0] == verb_token):
            advs.append(str(w))
            collected_tokens_i.append(w.i)

        # not working for root
        elif (w.dep_ in SUBJECTS and verb_token.dep_ == "ROOT"):
            subject = w.text
            # print("FOUND SUBJECT in ROOT VERB", w)
        # check if token is a subject and its first ancestor is the target verb, for non ROOT verb
        elif (w.dep_ in SUBJECTS and ancestors[0] == w):
            subject = w.text
            # print("FOUND SUBJECT in VERB", w)
    return subject, advs, collected_tokens_i


def get_noun_adj_from_subtree(noun_token):
    # print("")
    # print('--> get_noun_adj_from_subtree:', noun_token)
    # print("")
    # print("\tsubtree", list(noun_token.subtree))
    # print("\tchildren", list(noun_token.children))
    # print("\tancestors", list(noun_token.ancestors))
    collected_tokens_i = []
    preposition = ""
    determiner = ""
    adjectives = []
    noun = ""
    n_is_negated = isNegated(noun_token)

    # print("noun_token", noun_token)
    # for w in list(noun_token.subtree):
    # better results extracting only fron children elements, prevents many errorss
    
    # for w in list(noun_token.children):
    for w in list(noun_token.subtree):
        # print(w, w.pos_)
        # print("\tsubtree", list(w.subtree))
        # print("\tchildren", list(w.children))
        # print("\tancestors", list(w.ancestors))

        case = 0
        # TEST: check if the element has the input noun token as first ancestor

        # if(w.ancestors[0] == noun_token):

        if (w.pos_ == "ADP"):
            preposition = w.text
            collected_tokens_i.append(w.i)
            case = 1
        elif (w.pos_ == "ADJ"):
            adjectives.append(str(w.text))
            collected_tokens_i.append(w.i)
            case = 2

        # exclude special case for negated det. e.g. "no milk", negation is collected in isNegated
        # e.g. "the", "a" or "his", "her"
        # elif ((w.pos_ == "DET" or w.pos_ == "PRON") and w.text != "no"):
        elif ((w.pos_ == "DET") and w.text != "no"):
            determiner = w.text
            collected_tokens_i.append(w.i)
            case = 3
        elif (w.pos_ == 'PROPN'):
            noun = w.text
            collected_tokens_i.append(w.i)
            case = 4
        elif (w.pos_ == "NOUN"):
            noun = w.text
            collected_tokens_i.append(w.i)
            case = 5
        # else:
        #     print("no noun case: ", noun_token)
        
        # print("case: ", case, noun_token)
        # print("")
        if (n_is_negated):
            new_noun_chunk = preposition + " " + determiner + \
                " [NOT] " + "" + noun_token.text + " " + " ".join(adjectives)
        else:
            new_noun_chunk = preposition + " " + determiner + \
                " " + noun_token.text + " " + " ".join(adjectives)
            
    # return new_noun_chunk, collected_tokens_i
    return new_noun_chunk, collected_tokens_i


def find_other_verbs(doc, root_token):
    other_verbs = []
    for token in doc:
        ancestors = list(token.ancestors)
        if (token.pos_ == "VERB" and len(ancestors) == 1 and
                    ancestors[0] == root_token
                ):
            other_verbs.append(token)
    return other_verbs


total_sentences = 0
'''
Extract sentences in each paragraph
'''
for paragraph in text:

    '''
    Initialize spaCy NLP 
    '''
    doc = nlp(paragraph)
    sentences = list(doc.sents)
    tot_s = len(sentences)
    total_sentences = total_sentences + tot_s
    # print("Total Sentences in paragraph:", tot_s)
    extraction_comparison = []

    for sentence in sentences:
        # print(sentence)
        # print('---------------')
        # exclude empty lines
        if (str(sentence) != "\n"):
            print('*********************')
            print(sentence)

            root_token = find_root_of_sentence(sentence)

            # print(root_token)
            # print(list(root_token.subtree))
            new_sentence = rewrite_root_subtree(root_token, sentence)
            new_sentence_str = ""
            for elem in new_sentence:
                new_sentence_str = new_sentence_str + " " + str(elem)
            # print('new_sentence', new_sentence)
            new_sentence_str = new_sentence_str.replace("  ", " ")
            # much more replacement for standarization
            print('======================')
            print(new_sentence_str)
        # add space as a sentence separator
    # add a new line as separator

'''
    json 
        paragraph:[
            sentences:[
            {   original: "",
                converted: ""
            }
            ]
        ]
'''
