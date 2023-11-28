# Import the spaCy library into Python
import spacy
from spacy.morphology import Morphology
# Import the Matcher class
from spacy.matcher import Matcher


# Load a small language model for English; assign the result under 'nlp'
nlp = spacy.load('en_core_web_sm')

# Use the open() function with the 'with' statement to open the file for reading
with open(file='sample.txt', mode='r', encoding='utf-8') as file:
    
    # Use the read() method to read the contents of the file; assign result under 
    # the variable 'text'
    text = file.read()

# with open('sample.txt') as f:
# # with open('data/tests/aux_verbs.txt') as f:
#     text = f.readlines()


# Feed the string object to the language model
doc = nlp(text)

# print(len(doc), doc)
# print("-----------------")

# for w in doc:
#     print(w.i, w.text, w.pos_, w.dep_, " - " + w.tag_ + ": " + spacy.explain(w.tag_),)
#     print("\t", "head: ", w.head)
#     # print("\t", "subtree: ", list(w.subtree))
#     print("\t", "ancestors: ", list(w.ancestors))
#     print("\t", "children: ", list(w.children))
#     if(w.pos_ in ["VERB", "AUX"]):
#         verb_morph = Morphology.feats_to_dict(str(w.morph))
#         print("\tverb_morph: ", verb_morph)

    


# Use the len() function to check length of the Doc object to count 
# how many Tokens are contained within the Doc.


# Create a Matcher and provide model vocabulary; assign result under the variable 'matcher'
matcher = Matcher(vocab=nlp.vocab)

# Call the variable to examine the object
# print(matcher)

negations = ["no", "not", "n't", "never", "none"]

# Define a list with nested dictionaries that contains the pattern to be matched
# # generic
# pronoun_verb = [
#         {'POS': 'PRON'}, {'POS': 'VERB'}
#     ]


# pronoun_verb = [
#                 {'POS': 'PRON'}, 
#                 {'POS': 'VERB', "OP": "+"} # at least one
#                ]

# no aux with adverbs before or after the verb
# e.g. "I slowly walk" or "I walk slowly"
pronoun_adv_verb_adv = [{'POS': 'PRON'}, 
                    {'POS': 'ADV', 'OP': '*'}, 
                    {'POS': 'VERB', 'OP': '+'}, # at least one
                    {'POS': 'ADV', 'OP': '*'}, 
                ]

# Add the pattern to the matcher under the name 'pronoun+verb'
matcher.add("pronoun+adv+verb+adv", patterns=[pronoun_adv_verb_adv])


# Apply the Matcher to the Doc object under 'doc'; provide the argument
# 'as_spans' and set its value to True to get Spans as output

    # result = matcher(doc, as_spans=True)

# Call the variable to examine the output
# print('result: ', result)
# print('===========================')

# print(result[0])
# print(result[0].start, result[0].end)
# print(result[0].label)

# Access the model vocabulary using brackets; provide the value under 'result[0].label' as key.
# Then get the 'text' attribute for the Lexeme object, which contains the lexeme in a human-readable form.

# print(nlp.vocab[result[0].label].text)

# exit()

######################################
# testing new patten
######################################

# e.g. 'They have been walking' to the game.
# Define a list with nested dictionaries that contains the pattern to be matched
# pronoun_aux_verb = [{'POS': 'PRON'}, {'POS': 'AUX', 'OP': '+'}, {'POS': 'VERB'}]


# e.g. 'They slowly have been walking to the game'.
# e.g. 'They have been slowly walking to the game'.
# e.g. 'They have been walking slowly to the game'.
# pronoun_aux_verb = [{'POS': 'PRON'}, 
#                     {'POS': 'AVD', 'OP': '+'}, 
#                     {'POS': 'AUX', 'OP': '+'}, 
#                     {'POS': 'AVD', 'OP': '+'}, 
#                     {'POS': 'VERB'},
#                     {'POS': 'AVD', 'OP': '+'}, 
#                 ]

# e.g. 'They slowly have been walking to the game'.
# pronoun_aux_verb = [{'POS': 'PRON'}, 
#                     {'POS': 'ADV', 'OP': '+'}, 
#                     {'POS': 'AUX', 'OP': '+'}, 
#                     {'POS': 'VERB'},
#                 ]

# e.g. 'They slowly have been walking to the game'.
# OR
# e.g. 'They have been slowly walking to the game'.
# OR
# e.g. 'They have been walking slowly to the game'.

'''
--ok AUX
She is walking.
They slowly have been walking to the game.
They have been slowly walking to the game.
They have been walking slowly to the game.

--ok AUX 
They will like the game.
They should like the game.
They must like the game.
They must like very much the game.
'''
pronoun_aux_verb = [{'POS': 'PRON'}, 
                    {'POS': 'ADV', 'OP': '*'}, 
                    {'POS': 'AUX', 'OP': '+'}, 
                    {'POS': 'ADV', 'OP': '*'}, 
                    {'POS': 'VERB', 'OP': '+'},
                    {'POS': 'ADV', 'OP': '*'}, 
                ]


# making patters more specific for a particular use of AUX + verb
# testing AUX DO + verb
pronoun_aux_adv_verb = [
                    # {'POS': 'PRON', 'OP': '?'}, # optional. e.g. his/her/thier (pronoun)
                    {'POS': {"IN": ['PRON', "NOUN", "PROPN",]}, 'OP': '+'}, # at least one time is noun, pronoun or propper name
                    {'POS': 'ADV', 'OP': '*'}, # followed by at least an adv
                    {'POS': 'AUX', 'OP': '+'}, 
                    {'POS': 'ADV', 'OP': '*'}, 
                    {'POS': 'VERB', 'OP': '+'},
                    {'POS': 'ADV', 'OP': '*'}, 
                ]

'''
    !: Negate the pattern; the pattern can occur exactly zero times.
    ?: Make the pattern optional; the pattern may occur zero or one times.
    +: Require the pattern to occur one or more times.
    *: Allow the pattern to match zero or more times.
    '''
# Add the pattern to the matcher under the name 'pronoun+aux+verb'
matcher.add('pronoun+adv+aux+adv+verb+adv', patterns=[pronoun_aux_adv_verb])

# Apply the Matcher to the Doc object under 'doc'; provide the argument 'as_spans'
# and set its value to True to get Spans as output. Overwrite previous matches by
# storing the result under the variable 'results'.
results1 = matcher(doc, as_spans=True)
print('=======')
print(results1)
print('=======')

# Loop over each Span object in the list 'results'
for result in results1:
    pattern_name = nlp.vocab[result.label].text

    if(pattern_name == "pronoun+adv+verb+adv"):
        print("pronoun+adv+verb+adv", "\t", result)
    
    elif(pattern_name == "pronoun+adv+aux+adv+verb+adv"):
        print("pronoun+adv+aux+adv+verb+adv", "\t", result)
    
    # Print out the the name of the pattern rule, a tabulator character, and the matching Span
    # print(nlp.vocab[result.label].text, '\t', result)

    
    


