# include all functions and imports
from _util_fnc import *

'''
Define or load TEXT data
'''
text = (

    # Complex
    # "Antonio always loves his beautiful undefinable amazingly smart cat very much and he keeps trying to discover what she thinks is best. he explores AI's possibilities. He worships equity. "

    # SVO examples
    "Antonio loves his lovely happy kitten."
    "His cat is loved by Antonio."
    "The cat is loved by Antonio."
    "A cat is loved by Antonio."
    "Camila dropped a ball."
    "Camila dropped the ball."
    "Jane carries the bag."
    "He watches four blue big moons."

    # NOT SVO examples
    "Jose danced all night."
    "Antonio is thinking about the lovely summer."
    "She is thinking."
    "She calls her friend."

    # Hannes Sample Reference
    "Many moons ago, there was something in the river. Was it something big or something small? Nobody knew what it was. Everyone thought about the thing in the river. One day Little Feather walked near the river. He thought about the scary thing in the river. Was it something fat or was it something thin? Or maybe it was nothing at all? He approached the edge of the little river and heard a loud noise. Wow! What was that? Little Feather stood still and looked across the little river. The something big or something small swam down the little river. Wow! Was it black or was it white? Was it open or was it closed? Little Feather decided to walk in the cool river water. He sang a song while he kicked rocks playfully up and down with his feet. Then suddenly something touched his toe. Was it something big or something small, or was it nothing at all? Poor Little Feather was scared. The something big or something small held onto his toe! He screamed and jumped, he begged and prayed, but nothing helped at all. The something big or something small flew through the air and fell near him. He laughed so loud, tears began to flow down his cheeks! The something big or something small was an old shoe, after all."

    # PRESENT PAST AND FUTURE SVO SENTENCES
    "She bakes cookies.They swim in the pool.He writes a letter.We eat pizza.I watch TV.She sings a song.They dance at the party.He paints a picture.We play guitar.I drive a car.She studies math.They cook dinner.He mows the lawn.We read a book.I drink coffee.She walks the dog.They play chess.He takes photographs.We clean the house.I answer the phone.She teaches English.They work in the office.He fixes the computer.We visit the museum.I travel to Paris.She calls her friend.They ride bicycles.He plays the piano.We plant flowers.I do my homework.She baked cookies.They swam in the pool.He wrote a letter.We ate pizza.I watched TV.She sang a song.They danced at the party.He painted a picture.We played guitar.I drove a car.She studied math.They cooked dinner.He mowed the lawn.We read a book.I drank coffee.She walked the dog.They played chess.He took photographs.We cleaned the house.I answered the phone.She taught English.They worked in the office.He fixed the computer.We visited the museum.I traveled to Paris.She called her friend.They rode bicycles.He played the piano.We planted flowers.I did my homework.She will bake cookies.They will swim in the pool.He will write a letter.We will eat pizza.I will watch TV.She will sing a song.They will dance at the party.He will paint a picture.We will play guitar.I will drive a car.She will study math.They will cook dinner.He will mow the lawn.We will read a book.I will drink coffee.She will walk the dog.They will play chess.He will take photographs.We will clean the house.I will answer the phone.She will teach English.They will work in the office.He will fix the computer.We will visit the museum.I will travel to Paris.She will call her friend.They will ride bicycles.He will play the piano.We will plant flowers.I will do my homework."


)

'''
Control variables
'''
tot_s = 0   # total of sentences found: spacy
tot_svo = 0  # total of SVO matches found: textacy
tot_other = 0  # total of sentences proccesed by (ANTO-analysis)
tot_not = 0  # total of sentences NOT accounted for = excluded from dataset
c_bliss_result = {}
sentence_error = {}
s_counter = 1
'''
Initialize spaCy NLP 
'''
doc = nlp(text)

# split sentences. Note that furhter analysis is required when using conjunctions
sentences = list(doc.sents)

tot_s = len(sentences)

# loop each sentence
for sentence in sentences:

    # check if SVO type of sentence
    sen_SVOTriple = extract_SVO(sentence)

    if (sen_SVOTriple):
        tot_svo = tot_svo + 1
        # print('-------------------')
        # print(sentence)
        s_result = analyze_SVO(sen_SVOTriple, sentence)
        # print('------------ALL---> s_result', s_result)
        c_bliss_result[str(s_counter)] = s_result
        # print(sen_SVOTriple)
    else:
        tot_other = tot_other + 1
        sentence_result = analyze_sentence(sentence)
        c_bliss_result[str(s_counter)] = sentence_result

        '''

        # print("---> NOT SVO detected:\n", sentence)
        # try removing prepositions and try again SVO detection
        # TODO: use Matcher to improuve detection of patterns
        sentence_str = str(sentence)
        for prep in prepositions:
            sentence_str = sentence_str.replace(prep+" ", '')
        # print("  ", sentence_str)
        # re create nlp with new sentence
        new_nlp_doc = nlp(str(sentence_str))
        new_sentences = list(new_nlp_doc.sents)
        is_svo_sen = extract_SVO(new_sentences[0])

        if (is_svo_sen):

            # print("\t ---> new is_svo_sen: ", is_svo_sen)
            if (is_svo_sen):
                tot_svo = tot_svo + 1
                # print("   ---> detected")
                s_result = analyze_SVO(sen_SVOTriple, is_svo_sen)
                # check for empty results
                print(sentence)
                print(sentence_str)
                print(s_result, type(s_result))

                if (s_result == ""):
                    print("ERROR: ", is_svo_sen)
                else:
                    c_bliss_result[str(s_counter)] = s_result
        else:
            sentence_error[str(s_counter)] = {
                "original": sentence, "new_sentence": sentence_str}
            print("\n\n\n   ---> NOT detected STILL", )
            print(sentence)
            print(sentence_str)
            print()
        
        '''

        # process NOT svo sentence
        # analyze_sentence(sentence)

        # print(sentence)

    # print("ELEM[0]", sentence[0])
    # print(sentence[0], sentence[1], sentence[2])
    # print()
    s_counter = s_counter + 1


# print(c_bliss_result)
print()
print("----------------------------------")
print("  Total Sentences:", tot_s)
print("  Total SVO:", tot_svo)
print("  Total Other:", tot_other)
print("  Total Skipped:", int(tot_s-tot_other-tot_svo))
print("----------------------------------")
time_str = str(round(time.time()))
file_name = "C-Bliss-data-" + time_str + ".json"
file_name_error = "errors-" + time_str + ".json"

if (save_json):

    # with open(file_name_error, "w") as file:
    #     json.dump(c_bliss_result, file)
    #     print('Errors saved: ', file_name_error)
    #     print("----------------------------------")

    if (tot_svo == 0):
        print('NO data to save.')
    else:
        with open(file_name, "w") as file:
            json.dump(c_bliss_result, file)
            print('Data saved: ', file_name)
            print("----------------------------------")
