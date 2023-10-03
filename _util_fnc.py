'''
pip install spacy
pip install textacy
'''

# set to True to save json file in current directory
import spacy
import textacy
from spacy.morphology import Morphology
from spacy.matcher import Matcher
from spacy import displacy
import json
import time
from subject_object_extraction import *

# Set to True to save results in json file
save_json = True

# set to True see detailed logs
debug_on = False

# set to True to add brackets to group nested entities. e.g. "[ the river ] blue"
add_brackets = True

if (add_brackets):
    left_b = "["
    right_b = "] "
else:
    left_b = ""
    right_b = ""

'''
Select a model. "en_core_web_sm" should be ok for now
'''
#
################
# nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_lg')
# nlp = spacy.load('en_core_web_trf')
################


'''
Add pipe for merging noun_chunks and entities. Important for merging nouns and adj
'''
nlp.add_pipe("merge_noun_chunks")
nlp.add_pipe("merge_entities")

# most common prepositions and other words braking SVO detection
prepositions = ['aboard', 'above', 'across', 'against', 'alongside', 'amid', 'among', 'apart from', 'astride', 'at', 'atop', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'by', 'close to', 'far', 'far from', 'forward of', 'from', 'in', 'in between', 'in front of', 'inside', 'into', 'minus', 'near', 'near to', 'next to', 'of', 'off', 'on', 'on board', 'on top of', 'onto', 'upon', 'opposite', 'out', 'out of', 'outside', 'outside of', 'over', 'round', 'through', 'throughout', 'to', 'together with', 'toward', 'towards', 'under', 'underneath', 'up against', 'with', 'within', 'without', 'above', 'across', 'against', 'ahead', 'along', 'along with', 'amid', 'around', 'away', 'away from', 'behind', 'below', 'beneath', 'by means of', 'down', 'further to', 'in between', 'into', 'off', 'off of', 'on', 'onto', 'over', 'out of', 'past',
                'round', 'through', 'toward/towards', 'under', 'up', 'via', 'about', 'according to', 'anti', 'as', 'as for', 'as per', 'as to', 'as well as', 'aside from', 'bar', 'barring', 'because of', 'besides', 'but for', 'by', 'but', 'concerning', 'considering', 'contrary to', 'counting', 'cum', 'depending on', 'despite', 'due to', 'except', 'except for', 'excepting', 'excluding', 'given', 'in addition to', 'in case of', 'in face of', 'in favor of/in favour of', 'in light of', 'in spite of', 'in view of', 'including', 'instead of', 'less', 'like', 'notwithstanding', 'of', 'on account of', 'on behalf of', 'other than', 'owing to', 'pending', 'per', 'plus', 'preparatory to', 'pro', 're', 'regarding', 'regardless of', 'save', 'save for', 'saving', 'than', 'thanks to', 'unlike', 'versus', 'with', 'with reference to', 'with regard to', 'worth', 'all']

negations = {"no", "not", "n't", "never", "none"}


def extract_SVO(text):
    '''
    Extract SVO sentences. Note that all adverbs are removed and many more complex sentences are not recognized as SVOs
    '''
    tuples = textacy.extract.subject_verb_object_triples(text)
    if tuples:
        return list(tuples)
    else:
        return 0


def find_root_elem(sentence):
    '''
    finds the root element of a sentence and returns its token index
    '''
    c = 0
    # print('find_root_elem', sentence)
    for w in sentence:
        # print(w, w.pos_, w.dep_, c)
        if (w.dep_ == "ROOT"):
            return c
        c = c+1


def get_noun_adj(noun_chunk_str, keep_det=True, keep_prep=True):
    '''
    formats noun + adj.
    if keep_det = True keeps the noun determiner e.g "the" cat. "A" dog
    if keep_prep = True keeps the preceding preposition e.g "Across" the blue river
    '''
    # print('----> get_noun_adj', noun_chunk_str, type(noun_chunk_str))

    # remove pipe so we can iterate each  "det" "adj" "noun" tokens
    nlp.remove_pipe("merge_noun_chunks")
    # extract tokens from noun_chunk
    det_adj_noun = nlp(noun_chunk_str)
    # print('det_adj_noun:',det_adj_noun)
    preposition = ""
    determiner = ""
    adjectives = ""
    noun = ""
    # print('---> det_adj_noun: ', det_adj_noun)
    # check for the type of word used before ADJ
    for w in det_adj_noun:
        # print("\t get_noun_adj ---> token: " + w.text, w.dep_, w.pos_, w.head)
        if (w.pos_ == "ADP"):
            preposition = w.text
        elif (w.pos_ == "ADJ"):
            adjectives = adjectives + w.text + " "  # grap the ADJ
        elif (w.pos_ == "DET" or w.pos_ == "PRON"):  # e.g. "the", "a" or "his", "her"
            determiner = w.text
        elif (w.pos_ == "NOUN" or w.pos_ == 'PROPN'):  # TODO: need to check for other cases
            noun = w.text

    # remove start and end spaces
    adjectives = adjectives.strip()
    # add det
    if (keep_det):
        noun_adj = left_b + determiner + " " + noun + right_b + adjectives
    else:
        noun_adj = left_b + noun + right_b + adjectives
    if (keep_prep):
        noun_adj = preposition + " " + noun_adj

    # add pipe again for next analysis of next sentence
    nlp.add_pipe("merge_noun_chunks")
    # print('noun_adj -- ', noun_adj)
    return noun_adj


def get_verb_adv(sentence, verb_token):
    '''
    find adverbs for a given verb using Matcher
    '''
    # print(sentence)
    # print(list(verb_token.subtree))
    # print('\t\t get_verb_adv - verb_token', verb_token.text)
    # return
    matcher = Matcher(nlp.vocab)
    # find adverbs AFTER and BEFORE the verb
    patterns = [
        # ADV + VERB
        [{'POS': 'ADV'}, {'LEMMA': verb_token.lemma_}],
        # ADV + "and" + ADV + VERB
        [{'POS': 'ADV'}, {'TEXT': 'and'}, {
            'POS': 'ADV'}, {'LEMMA': verb_token.lemma_}],
        # VERB + ADV
        [{'LEMMA': verb_token.lemma_}, {'POS': 'ADV'}],
        # VERB + ADV + "and" + VERB
        [{'LEMMA': verb_token.lemma_}, {'POS': 'ADV'},
            {'TEXT': 'and'}, {'POS': 'ADV'}],
        # VERB + ADV + "," + ADV + "," + ADV
        [{'LEMMA': verb_token.lemma_}, {'POS': 'ADV'}, {'TEXT': ','},
            {'POS': 'ADV'}, {'TEXT': ','}, {'POS': 'ADV'}],
        # VERB + ADV + "and" + ADV + "and" + ADV
        [{'LEMMA': verb_token.lemma_}, {'POS': 'ADV'}, {'TEXT': 'and'},
            {'POS': 'ADV'}, {'TEXT': 'and'}, {'POS': 'ADV'}],
        # VERB + ADV + "," + ADV + ", and" + ADV
        [{'LEMMA': verb_token.lemma_}, {'POS': 'ADV'}, {'TEXT': ','},
            {'POS': 'ADV'}, {'TEXT': ', and'}, {'POS': 'ADV'}],
    ]
    # search for patters
    matcher.add("verb-adverb", patterns)
    matches = matcher(sentence)
    selected_match = ""
    match_c = 0
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = sentence[start:end]  # The matched span
        # print(match_id, string_id, start, end, span.text, len(span.text))
        match_len = len(span.text)
        # get the longest patterf found
        if (match_len > match_c):
            match_c = match_len
            selected_match = span.text
    # remove the verb in the match
    selected_match = selected_match.replace(verb_token.text, '')
    # remove start and end spaces
    selected_match = selected_match.strip()
    # re organize the verb + adverbs after the verb in infinitive form
    verb_adv = verb_token.lemma_ + selected_match
    return verb_adv


def analyze_SVO(SVOTriple_arr, sentence):
    '''
    Analyze an array of SVOTriple objects
    '''
    # print('analyze_SVO ()')
    # print(SVOTriple_arr)

    # TODO: need to check if there are more than SVO elements
    # e.g. conjunctions: and, or, but, because, for, if, when.
    # To prevent this we can do additional separation in the original data

    # tot_SVOs=len(SVOTriple_arr)
    # print('tot_SVOs', tot_SVOs)
    # print('---> svo1: ', SVOTriple_arr[0])

    result = {
        "original": str(sentence),
        "CBliss": ""
    }

    # process each SVOTriple
    for SVOTriple in SVOTriple_arr:
        # print(SVOTriple)
        subject = SVOTriple[0]
        verb = SVOTriple[1]
        object = SVOTriple[2]

        if (debug_on):
            print("\tsubject: ", subject)
            print("\tverb: ", verb)
            print("\tobject: ", object, object[0], type(object[0]))

        # print("object type", type(object))
        root_elem_i = find_root_elem(sentence)
        # print('root_elem_i', root_elem_i)
        # print('test root_elem_i', sentence[root_elem_i])

        # apply noun-adj(s) structure to the object (noun_chunk)
        obj_adj = get_noun_adj(str(object[0]))
        # print('obj_adj "', obj_adj, obj_adj[0], type(obj_adj), '"')
        try:
            # get verb tense structure, e.g. [past] + VERB + ADV(s)
            verb_tense_adv = get_verb_adv(sentence, sentence[root_elem_i])
            # print("---> verb_tense_adv", verb_tense_adv)
        except Exception as e:
            print(f"\n---> analyze_SVO An exception occurred: {str(e)}\n")

        # get verb tense
        verb_tense_values = get_verb_tense(sentence, root_elem_i)

        # build new sentence in Conceptual-Bliss structure
        c_bliss = "[" + str(verb_tense_values['tense']) + "]" + \
            " [" + str(subject[0]) + "]" + \
            " [" + str(verb_tense_adv) + "]" + \
            " [" + str(obj_adj) + "]"

        # add sentence to CBliss array
        result['CBliss'] = result['CBliss'] + "" + str(c_bliss)
    return result


def analyze_sentence(sentence):
    '''
    Analyze sentence not identified as SVO
    '''
    # print('\n\n--->analyze_sentence () ')
    # print(sentence, type(sentence))

    result = {
        "original": str(sentence),
        "CBliss": ""
    }

    parts = {'tense': '', 'verb': '', 'lema': '',
             'subject': '', 'object': '', 'isNegated': False}
    counter_tok = 0  # token counter in sentence

    # process each token
    for w in sentence:
        # if (debug_on):
        #     print(w.text)
        #     print(
        #         "\t",
        #         " dep_=", w.dep_,
        #         " dep_ EXP=", spacy.explain(w.dep_),
        #         " pos_=", w.pos_,
        #         " lemma_=", w.lemma_,
        #         " morph=", w.morph,
        #         " shape_=", w.shape_,
        #         " ent_type_=", w.ent_type_
        #     )
        #     print("\t tag_=", w.tag_, "tag_ EXP", spacy.explain(w.tag_))
        #     print("\t head.head:", w.head.head, "head:", w.head)
        #     print("\tSUBTREE:", list(w.subtree))
        #     print("-----------")

        # subject = ""
        # verb = ""
        # object = ""

        # find subject of the sentence
        # check first for dep_ nsubj (nominal subject) and pos = PROPN or PROPN
        # and (w.pos_ == 'PROPN' or w.pos_ == 'PROPN')):
        # if (w.dep == 'nsubj'):
        #     parts['subject'] = w.lemma_

        # check for the subject of the sentence
        # not acurate for TO BE + VERB (present and past progressive)
        # elif ("subj" in w.dep_):
        #     subtree = list(w.subtree)
        #     start = subtree[0].i
        #     end = subtree[-1].i + 1
        #     parts['subject'] = sentence[start:end]

        # if ("dobj" in w.dep_):
        #     subtree = list(w.subtree)
        #     start = subtree[0].i
        #     end = subtree[-1].i + 1

        # # if preposition found, followed by a pobj (object of preposition)
        # # get the object of the preposition
        # if (w.dep_ == 'prep' and sentence[counter_tok+1].dep_ == 'pobj'):
        #     # parts['object'] = opbj

        #     pobj = w.text + " " + sentence[counter_tok+1].text
        #     pobj = get_noun_adj(pobj)
        #     parts['object'] = pobj
        #     print("PREP + OBJ PREP: ", pobj)

        # # noun phrase as adverbial modifier
        # elif (w.dep_ == 'npadvmod'):
        #     parts['object'] = w.text
        #     print("noun phrase: ",  w.text)

        # opbj = str(get_prepositional_phrase_objs(sentence))
        # opbj = get_noun_adj(opbj)
        # parts['object'] = opbj
        # if (debug_on):
        #     print('get_prepositional_phrase_objs', opbj)
        # print("----> parts['object']", parts['object'])

        # Analyze root element dependencies
        if (w.dep_ == "ROOT"):
            parts['isNegated'] = isNegated(w)
            # testing for each verb
            # if (w.pos_ == "VERB"):
            subtree_c = 0  # subtree counter
            subtree = list(w.subtree)  # access subtree as a list
            # itereate root's subtree
            # print("---> Itereate root's subtree: ", w.text, subtree)
            for sub in subtree:
                # print(sub.text)
                # print(
                #     "\t",
                #     " dep_=", sub.dep_,
                #     " dep_ EXP=", spacy.explain(sub.dep_),
                #     " pos_=", sub.pos_,
                #     " lemma_=", sub.lemma_,
                #     " morph=", sub.morph,
                #     " shape_=", sub.shape_,
                #     " ent_type_=", sub.ent_type_
                # )
                # print("\t tag_=", sub.tag_, "tag_ EXP",
                #       spacy.explain(sub.tag_))
                # print("\t head.head:", sub.head.head, "head:", sub.head)
                # print("\tSUBTREE:", list(sub.subtree))
                # print("-----------")

                # find subject of the sentence. dep_ == nsubj (nominal subject)
                if (sub.dep_ == 'nsubj'):
                    parts['subject'] = sub.text

                # find the object of the sentence
                # if preposition found, followed by a pobj (object of preposition)
                # get the object of the preposition
                if (sub.dep_ == 'prep' and subtree[subtree_c+1].dep_ == 'pobj'):
                    pobj = sub.text + " " + subtree[subtree_c+1].text
                    # print("PREP + OBJ of PREP: ", pobj)
                    pobj = get_noun_adj(pobj)
                    # parts['object'] = sub.text + " " + pobj
                    parts['object'] = pobj
                    # print("PREP + OBJ of PREP noun_adj: ", pobj)
                    # Note another will be to find the pobj and all its .lefts

                # noun phrase as adverbial modifier
                elif (sub.dep_ == 'npadvmod'):
                    parts['object'] = sub.text
                    # print("npadvmod (noun phrase): ",  sub.text)
                subtree_c = subtree_c+1

            # convert morphology string to a dict
            verb_morph = Morphology.feats_to_dict(str(w.morph))
            # print(verb_morph)
            try:
                # check for present and past progressive
                # verb to be before root verb
                # TODO: need to check for "TO BE + NOT + VERB"
                # TODO: need to check for "NOT + VERB"
                if (
                    sentence[counter_tok-1].dep_ == "aux" and
                    (sentence[counter_tok-1].text == "am" or
                     sentence[counter_tok-1].text == "is" or
                     sentence[counter_tok-1].text == "are" or
                     sentence[counter_tok-1].text == "was" or
                     sentence[counter_tok-1].text == "were")):
                    # print("---> TO BE + " + w.text)
                    # to_be = sentence[counter_tok-1].text
                    verb_inf = w.lemma_
                    tobe_morph_value = sentence[counter_tok-1].morph
                    tobe_morph = Morphology.feats_to_dict(
                        str(tobe_morph_value))
                    tense_to_be_verb = get_to_be_tense_type(
                        tobe_morph, verb_inf, verb_morph)
                    # print('tense_to_be_verb --> ', tense_to_be_verb)
                    parts['tense'] = tense_to_be_verb['tense']
                    parts['verb'] = "[TO BE] ["+w.lemma_+"]"

                # Check for Future: "WILL + TO BE + VERB"
                elif (sentence[counter_tok-2].dep_ == "aux" and
                        sentence[counter_tok-2].text == "will" and
                        sentence[counter_tok-1].dep_ == "aux" and
                        sentence[counter_tok-1].text == "be" and
                        ('VerbForm' in verb_morph and
                         verb_morph['Aspect'] == 'Prog')):
                    # parts['tense'] = "future continuous"
                    parts['tense'] = "future"
                    parts['verb'] = "" + "["+w.lemma_+"]"

                # Check for Future: "WILL + VERB".
                elif (sentence[counter_tok-1].dep_ == "aux" and
                        sentence[counter_tok-1].text == "will" and
                        ('VerbForm' in verb_morph and
                         verb_morph['VerbForm'] == 'Inf')):
                    parts['tense'] = "future"
                    parts['verb'] = "" + "["+w.lemma_+"]"

                elif ('Tense' in verb_morph and verb_morph['Tense'] == 'Past'):
                    parts['tense'] = "past"
                    parts['verb'] = "["+w.lemma_+"]"
                elif ('Tense' in verb_morph and verb_morph['Tense'] == 'Pres'):
                    parts['tense'] = "present"
                    parts['verb'] = "" + "["+w.lemma_+"]"

                else:
                    parts['tense'] = "NOT FOUND"
                    parts['verb'] = w.lemma_

            except Exception as e:
                print(f"\nAn exception occurred: {str(e)}\n")

        counter_tok = counter_tok + 1

        # build new sentence in Conceptual-Bliss structure
        if (parts['isNegated']):
            c_bliss = "[" + str(parts['tense']) + "]" + \
                " [" + "NOT" + "]" + \
                " [" + str(parts['subject']) + "]" + \
                " [" + str(parts['verb']) + "]" + \
                " [" + str(parts['object']) + "]"

        else:
            c_bliss = "[" + str(parts['tense']) + "]" + \
                " [" + str(parts['subject']) + "]" + \
                " [" + str(parts['verb']) + "]" + \
                " [" + str(parts['object']) + "]"

    # add sentence to CBliss array
    result['CBliss'] = result['CBliss'] + "" + str(c_bliss)
    # print('======')
    # print(result)
    # print('======')
    return result


def get_prepositional_phrase_objs(doc):
    prep_spans = []
    for token in doc:
        if ("pobj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            prep_spans.append(doc[start:end])
    return prep_spans


def get_verb_tense(sentence, root_i):
    ''' 
    Get verb tense extracted from Morphology attribute
    '''
    # obj to return
    parts = {
        "tense": "",
        "verb": ""
    }
    # convert morphology string to a dict
    verb_morph = Morphology.feats_to_dict(str(sentence[root_i].morph))
    # print("---> verb_morph: ", sentence[root_i].morph)
    # print("---> sentence[root_i-1].dep_ ",sentence[root_i-1].dep_)
    # print("---> sentence[root_i-1].pos_ ",sentence[root_i-1].pos_)

    try:
        # Check for passive voice cases. e.g. "is loved", "was loved"
        if (sentence[root_i-1].dep_ == "auxpass"):
            # print("Pasive voice: verb TO BE + VERB (Past Participle)")
            if (sentence[root_i-1].text == "is" or sentence[root_i-1].text == "are"):
                parts['tense'] = "present - passive"
            elif (sentence[root_i-1].text == "was" or sentence[root_i-1].text == "were"):
                parts['tense'] = "past - passive"
        # Present and Past Progressive: verb to be before root verb. e.g. "I am playing", "I was playing"
        # look for aux role of verb to be before root verb
        elif (sentence[root_i-1].pos_ == "AUX" and
                (sentence[root_i-1].text == "am" or
                 sentence[root_i-1].text == "is" or
                 sentence[root_i-1].text == "are" or
                 sentence[root_i-1].text == "was" or
                 sentence[root_i-1].text == "were")
              ):
            # print("---> use of verb TO BE as AUX: " + sentence[root_i-1].text + " " + sentence[root_i].text)
            to_be = sentence[root_i-1].text
            verb_inf = sentence[root_i].lemma_
            tobe_morph_value = sentence[root_i-1].morph
            tobe_morph = Morphology.feats_to_dict(
                str(tobe_morph_value))
            tense_to_be_verb = get_to_be_tense_type(
                tobe_morph, verb_inf, verb_morph)
            # print('tense_to_be_verb --> ', tense_to_be_verb)
            parts['tense'] = tense_to_be_verb['tense']

        # Future "WILL + TO BE + VERB"
        elif (sentence[root_i-2].dep_ == "aux" and
                sentence[root_i-2].text == "will" and
                sentence[root_i-1].dep_ == "aux" and
                sentence[root_i-1].text == "be" and
                ('VerbForm' in verb_morph and
                 verb_morph['Aspect'] == 'Prog')):
            parts['tense'] = "future continuous"

        # Future "WILL + VERB".
        elif (sentence[root_i-1].dep_ == "aux" and
                sentence[root_i-1].text == "will" and
                ('VerbForm' in verb_morph and
                 verb_morph['VerbForm'] == 'Inf')):
            parts['tense'] = "future"

        # Past
        elif ('Tense' in verb_morph and verb_morph['Tense'] == 'Past'):
            parts['tense'] = "past"
        # Present
        elif ('Tense' in verb_morph and verb_morph['Tense'] == 'Pres'):
            parts['tense'] = "present"

        else:
            parts['tense'] = "TENSE NOT FOUND"
        parts['verb'] = sentence[root_i].lemma_

    except Exception as e:
        print(f"\n---> get_verb_tense - An exception occurred: {str(e)}\n")
    return parts


def get_to_be_tense_type(tobe_morph, verb_inf, verb_morph):
    """
    Determine if the use of verb TO BE + VERB is present or past progressive

    :param obj tobe_morph: morphology object of verb to be as aux verb
    :param str verb_inf: root verb in infinitive form used with preceding verb to be
    :param obj verb_morph: verb morphology object of root verb
    :return: a dictionary with verb tense and verb in infiritive form
    :rtype: dict
    """
    verb = {
        'tense': '',
        'verb_inf': verb_inf
    }
    if (tobe_morph['Tense'] == 'Past' and verb_morph['Tense'] == 'Pres' and verb_morph['Aspect'] == 'Prog'):
        verb['tense'] = "past progresive"
    elif (tobe_morph['Tense'] == 'Pres' and verb_morph['Tense'] == 'Pres' and verb_morph['Aspect'] == 'Prog'):
        verb['tense'] = "present progressive"
    else:
        verb['tense'] = "VERB TENSE NOT FOUND"
    return verb
