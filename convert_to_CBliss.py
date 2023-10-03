# include all functions and imports
from _util_fnc import *

'''
Define or load TEXT data
'''
text = (
    #
    # questions
    # "Is this a question?"
    # "This is not a question"

    # Complex
    # "Antonio always loves his beautiful undefinable amazingly smart cat very much and he keeps trying to discover what she thinks is best. he explores AI's possibilities. He worships equity. "

    # SVO examples
    # "Antonio loves his lovely happy kitten."
    # "His cat is loved by Antonio."
    # "The cat is loved by Antonio."
    # "A cat is loved by Antonio."
    # "Camila dropped a ball."
    # "Camila dropped the ball."
    # "Jane carries the bag."
    # "He watches four blue big moons."
    #  "She calls her friend."

    # NOT SVO examples
    # "Jose danced all night."
    # "Antonio is thinking about the lovely summer."
    # "She is thinking."


    # Hannes Sample Reference
    # "Many moons ago, there was something in the river. Was it something big or something small? Nobody knew what it was. Everyone thought about the thing in the river. One day Little Feather walked near the river. He thought about the scary thing in the river. Was it something fat or was it something thin? Or maybe it was nothing at all? He approached the edge of the little river and heard a loud noise. Wow! What was that? Little Feather stood still and looked across the little river. The something big or something small swam down the little river. Wow! Was it black or was it white? Was it open or was it closed? Little Feather decided to walk in the cool river water. He sang a song while he kicked rocks playfully up and down with his feet. Then suddenly something touched his toe. Was it something big or something small, or was it nothing at all? Poor Little Feather was scared. The something big or something small held onto his toe! He screamed and jumped, he begged and prayed, but nothing helped at all. The something big or something small flew through the air and fell near him. He laughed so loud, tears began to flow down his cheeks! The something big or something small was an old shoe, after all."

    # PRESENT PAST AND FUTURE SVO SENTENCES
    # "She bakes cookies.They swim in the pool.He writes a letter.We eat pizza.I watch TV.She sings a song.They dance at the party.He paints a picture.We play guitar.I drive a car.She studies math.They cook dinner.He mows the lawn.We read a book.I drink coffee.She walks the dog.They play chess.He takes photographs.We clean the house.I answer the phone.She teaches English.They work in the office.He fixes the computer.We visit the museum.I travel to Paris.She calls her friend.They ride bicycles.He plays the piano.We plant flowers.I do my homework.She baked cookies.They swam in the pool.He wrote a letter.We ate pizza.I watched TV.She sang a song.They danced at the party.He painted a picture.We played guitar.I drove a car.She studied math.They cooked dinner.He mowed the lawn.We read a book.I drank coffee.She walked the dog.They played chess.He took photographs.We cleaned the house.I answered the phone.She taught English.They worked in the office.He fixed the computer.We visited the museum.I traveled to Paris.She called her friend.They rode bicycles.He played the piano.We planted flowers.I did my homework.She will bake cookies.They will swim in the pool.He will write a letter.We will eat pizza.I will watch TV.She will sing a song.They will dance at the party.He will paint a picture.We will play guitar.I will drive a car.She will study math.They will cook dinner.He will mow the lawn.We will read a book.I will drink coffee.She will walk the dog.They will play chess.He will take photographs.We will clean the house.I will answer the phone.She will teach English.They will work in the office.He will fix the computer.We will visit the museum.I will travel to Paris.She will call her friend.They will ride bicycles.He will play the piano.We will plant flowers.I will do my homework."

    # Aladdin story.
    "There once lived a poor tailor who had a son called Aladdin; a careless, idle boy who would do nothing but play all day long in the streets with little idle boys like himself. This so grieved the father that he died; yet, in spite of his mother’s tears and prayers, Aladdin did not mend his ways.  One day, when he was playing in the streets as usual, a stranger asked him his age, and if he was not the son of Mustapha the tailor.  “I am, sir,” replied Aladdin; “but he died a long while ago.”  On this the stranger, who was a famous African magician, fell on his neck and kissed him saying: “I am your uncle, and knew you from your likeness to my brother. Go to your mother and tell her I am coming.”  Aladdin ran home and told his mother of his newly found uncle.  “Indeed, child,” she said, “your father had a brother, but I always thought he was dead.”  However, she prepared supper, and bade Aladdin seek his uncle, who came laden with wine and fruit. He fell down and kissed the place where Mustapha used to sit, bidding Aladdin’s mother not to be surprised at not having seen him before, as he had been forty years out of the country. He then turned to Aladdin, and asked him his trade, at which the boy hung his head, while his mother burst into tears. On learning that Aladdin was idle and would learn no trade, he offered to take a shop for him and stock it with merchandise. Next day he bought Aladdin a fine suit of clothes and took him all over the city, showing him the sights, and brought him home at nightfall to his mother, who was overjoyed to see her son so fine.  Next day the magician led Aladdin into some beautiful gardens a long way outside the city gates. They sat down by a fountain and the magician pulled a cake from his girdle, which he divided between them. Then they journeyed onwards till they almost reached the mountains. Aladdin was so tired that he begged to go back, but the magician beguiled him with pleasant stories and lead him on in spite of himself.  At last they came to two mountains divided by a narrow valley.  “We will go no farther,” said his uncle. “I will show you something wonderful; only do you gather up sticks while I kindle a fire.”  When it was lit the magician threw on it a powder he had about him, at the same time saying some magical words. The earth trembled a little in front of them, disclosing a square flat stone with a brass ring in the middle to raise it by.  Aladdin tried to run away, but the magician caught him and gave him a blow that knocked him down.  “What have I done, uncle?” he said piteously; whereupon the magician said more kindly: “Fear nothing, but obey me. Beneath this stone lies a treasure which is to be yours, and no one else may touch it, so you must do exactly as I tell you.”  At the word treasure Aladdin forgot his fears, and grasped the ring as he was told, saying the names of his father and grandfather. The stone came up quite easily, and some steps appeared.  “Go down,” said the magician; “at the foot of those steps you will find an open door leading into three large halls. Tuck up your gown and go through them without touching anything, or you will die instantly. These halls lead into a garden of fine fruit trees. Walk on till you come to niche in a terrace where stands a lighted lamp. Pour out the oil it contains, and bring it me.” He drew a ring from his finger and gave it to Aladdin, bidding him prosper.  Aladdin found everything as the magician had said, gathered some fruit off the trees, and, having got the lamp, arrived at the mouth of the cave.  The magician cried out in a great hurry: “Make haste and give me the lamp.”  This Aladdin refused to do until he was out of the cave. The magician flew into a terrible passion, and throwing some more powder on to the fire, he said something, and the stone rolled back into its place.  The man left the country, which plainly showed that he was no uncle of Aladdin’s but a cunning magician, who had read in his magic books of a wonderful lamp, which would make him the most powerful man in the world. Though he alone knew where to find it, he could only receive it from the hand of another. He had picked out the foolish Aladdin for this purpose, intending to get the lamp and kill him afterwards.  For two days Aladdin remained in the dark, crying and lamenting. At last he clasped his hands in prayer, and in so doing rubbed the ring, which the magician had forgotten to take from him.  Immediately an enormous and frightful genie rose out of the earth, saying: “What would you like me to do for you? I am the Slave of the Ring, and will obey you in all things.”  Aladdin fearlessly replied, “Deliver me from this place!” whereupon the earth opened, and he found himself outside.  "

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
            sentence_str = sentence_str.replace(prep+" ", '. ')
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
    s_counter = s_counter + 1

if (debug_on):
    print(c_bliss_result)

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
