# Import the spaCy library into Python
import spacy
from spacy.morphology import Morphology
# Import the Matcher class
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')

# text_filename = 'sample_control.txt'
# text_filename = 'sample_single.txt'
text_filename = 'sample.txt'
with open(file=text_filename, mode='r', encoding='utf-8') as file:
    
    # Use the read() method to read the contents of the file; assign result under 
    # the variable 'text'
    text = file.read()

# with open('sample.txt') as f:
# # with open('data/tests/aux_verbs.txt') as f:
#     text = f.readlines()

# Feed the string object to the language model
doc = nlp(text)

negations = ["no", "not", "n't", "never", "none"]

###########################################
def check_aux_verbs(sentence):
    print('==> check_aux_verbs()')
    print(sentence)
    # Create a Matcher and provide model vocabulary; assign result under the variable 'matcher'
    matcher = Matcher(vocab=nlp.vocab)

    # no use of aux verbs with adverbs before or after the verb
    # e.g. "I slowly walk" or "I walk slowly"
    pronoun_verb_adv = [
        # OP = '*'-> zero or more. OP = '+' -> one or more
        {'POS': 'PRON'}, 
        {'POS': 'ADV', 'OP': '*'}, 
        {'POS': 'VERB', 'OP': '+'}, 
        {'POS': 'ADV', 'OP': '*'}, 
    ]

    # add matcher
    matcher.add('pronoun_verb_adv', patterns=[pronoun_verb_adv])

    # making patters more specific for a particular use of AUX + verb
    # testing AUX DO + verb
    pronoun_aux_verb_adv = [
        {'POS': {"IN": ['PRON', "NOUN", "PROPN",]}, 'OP': '+'}, # at least one time is noun, pronoun or propper name
        {'POS': 'ADV', 'OP': '*'}, # followed by at least an adv
        {'POS': 'AUX', 'OP': '+'}, 
        {'POS': 'ADV', 'OP': '*'}, 
        {'POS': 'VERB', 'OP': '+'},
        {'POS': 'ADV', 'OP': '*'}, 
    ]
    # add matcher
    matcher.add('pronoun_aux_verb_adv', patterns=[pronoun_aux_verb_adv])

    # Apply the Matcher to the sentence; 
    # provide the argument 'as_spans' and set its value to True to get Spans as output. 
    results = matcher(sentence, as_spans=True)
    print('=======')
    print(results)
    print('=======')

    # counters for each pattern
    no_aux = 0
    with_aux = 0

    print("==> matches")
    # Loop over each Span object in the list 'results'
    for result in results:
        pattern_name = nlp.vocab[result.label].text
        print('===> result: ', result)
        if(pattern_name == "pronoun_verb_adv"):
            print("pronoun_verb_adv", "\t", result)
            no_aux = no_aux + 1
        
        elif(pattern_name == "pronoun_aux_verb_adv"):
            print("pronoun_aux_verb_adv", "\t", result)
            with_aux = with_aux + 1
        
        # Print out the the name of the pattern rule, a tabulator character, and the matching Span
        # print(nlp.vocab[result.label].text, '\t', result)
        if(no_aux > 0 and with_aux > 0):
            return 'mix'
        elif(no_aux > 0 and with_aux == 0):
            return 'no_aux'
        elif(no_aux == 0 and with_aux > 0):
            return 'aux'


# test function

has_aux_verb = check_aux_verbs(doc)
print("-----------------")
print('has_aux_verb: ', has_aux_verb)





