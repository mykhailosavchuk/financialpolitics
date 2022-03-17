import time

start = time.time()
print(1)
from parrot import Parrot
import torch
import warnings
warnings.filterwarnings("ignore")
import sys

s = "Michael Clifton Burgess is an American physician and politician representing the 26th congressional district of Texas in the United States House of Representatives. Located in Denton County The district is in a suburban County north of Dallas and Fort Worth. In 2002 Burgess Defeated Scott Armey the son of the House Majority Leader and then US senator. Representative Dick Armey Lost in a primary runoff election. He Practiced as a doctor of obstetrics and gynecology Before his election. A Member of the congressional Tea Party Caucus Burgess has been involved in the debates over health care reform and energy policy for several years. He opposes abortion, is unsure of the extent of the contribution of human Activity to global warming. supported President Donald Trump's restrictions on travel from Muslim majority countries and refugee immigration and supports repeal of the Affordable Care Act."
# Replace sentences in string with a list of capitalised substitutes
def recapitalise_from_cap_list(wcaps, recombine_list):
  for caps in wcaps:
    recombine_list = recombine_list.replace(" " + caps.lower(), " " + caps)
  first_char = recombine_list[:1].upper()
  recombine_list = recombine_list[1:]
  recombine_list = first_char + recombine_list
  recombine_list += ". "
  return recombine_list

'''
TODO Implement
Rephrase Unit

Take a paragraph, snapshot the capitals,
Rephrase the paragraph from a list of the paragraph sentences
Rebuild the paragraph.
Re-apply capital letters.

'''

end = time.time()
print(end - start)

'''
uncomment to get reproducable paraphrase generations
def random_state(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

random_state(1234)
'''

#Init models (make sure you init ONLY once if you integrate this to your code)
print(2)
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
end = time.time()
print(end - start)
print(3)
# phrases = ["Can you recommed some upscale restaurants in Rome?",
#            "What are the famous places we should not miss in Russia?"
# ]

# for phrase in phrases:
#   print("-"*100)
#   print("Input_phrase: ", phrase)
#   print("-"*100)
#   para_phrases = parrot.augment(input_phrase=phrase)
#   for para_phrase in para_phrases:
#    print(para_phrase)

# s = "The ultimate test of your knowledge is your capacity to convey it to another."


# return the words with capital letters from the string
def get_words_with_capitals(s):
  words = s.split(" ")
  words_with_capitals = []
  for word in words:
    for letter in word:
      if letter.isupper():
        words_with_capitals.append(word)

  # Include the word before an apostraphie (ie. Kissenger's includes [Kissenger, Kissenger's])
  for i in words_with_capitals:
    # print(i)
    if "'" in i:
      single = i.split("'")
      words_with_capitals.append(single[0])

  # Clean the list of duplicates and filter unwanted characters
  words_with_capitals = list(set(words_with_capitals))
  words_with_capitals = [word.replace(".", "") for word in words_with_capitals]
  words_with_capitals = [word.replace(",", "") for word in words_with_capitals]

  return words_with_capitals

s = "Michael Clifton Burgess is an American physician and politician representing Texas's 26th congressional district in the United States House of Representatives. The district is anchored in Denton County, a suburban county north of Dallas and Fort Worth. In 2002, Burgess defeated Scott Armey, the son of House Majority Leader and then U.S. Representative Dick Armey, in a primary runoff election. Before his election, he practiced as a doctor of obstetrics and gynecology. Burgess is a member of the congressional Tea Party Caucus, and has been involved in the debates over health care reform and energy policy. He opposes abortion, is unsure of the extent of the contribution of human activity to global warming, supported President Donald Trump's restrictions on travel from Muslim majority countries and refugee immigration, and supports the repeal of the Affordable Care Act."
# s = "Apple banana Trump's"

end = time.time()
print(end - start, "   4")


# p = ["Texas's", 'United', 'Michael', 'Clifton', 'American', 'Representatives', 'Burgess', 'States', 'House']


# n = ['michael clifton burgess is an american physician and politician who represents the 26th congressional district of texas in the united states house of representatives']

# for i in p:
#   if "'" in i:
#     single = i.split("'")
#     p.append(single[0])

# print(p)
# sys.exit()

# wcaps = get_words_with_capitals(s)
# print(wcaps)

phrases = s.split(". ")
recombine_list = []
# sys.exit()
# Rephrase and recombine
wcaps = []
for phrase in phrases:
  # print(5)
  # end = time.time()
  # print(end - start)
  # print("-"*100)
  # print("Input_phrase: ", phrase)
  # print("-"*100)
  wcaps = get_words_with_capitals(phrase)

  para_phrases = parrot.augment(input_phrase=phrase, do_diverse = True)
  # print(para_phrases)
  # import sys
  # sys.exit()
  # print("phrase:")
  # print(phrase)
  # print("+++++++++++++++++++")
  # print(para_phrases)
  # print("-----------------------------")

  # Pick the third, then second then top list, depending on availability
  # TODO tidy to make an elif
  if len(para_phrases) > 1:
    fixed_string = recapitalise_from_cap_list(wcaps, para_phrases[1][0])
    # try:
    #   fixed_string = recapitalise_from_cap_list(wcaps, para_phrases[2][0])
    # except:
    #   fixed_string = recapitalise_from_cap_list(wcaps, para_phrases[1][0])
  else:
      fixed_string = recapitalise_from_cap_list(wcaps, para_phrases[0][0])

  recombine_list.append(fixed_string)
  # recapitalise_from_cap_list(wcaps, )

  # print(wcaps)
  print(1010101)
  # print(recombine_list)
  # break


print(55)
# print(recombine_list)

end = time.time()
print(end - start)
print(6)
# Preserve and re-apply capital letters

# k = ['Michael Clifton Burgess is an American physician and politician representing the 26th congressional district of Texas in the United States House of Representatives. ', 'Located in Denton County The district is in a suburban County north of Dallas and Fort Worth. ', 'In 2002 Burgess defeated Scott Armey the son of the House Majority Leader and then US senator. ', 'Representative Dick Armey lost in a primary runoff election. ', 'He practiced as a doctor of obstetrics and gynecology Before his election. ', 'A member of the congressional Tea Party Caucus Burgess has been involved in the debates over health care reform and energy policy for several years. ', "He opposes abortion is unsure of the extent of the contribution of human Activity to global warming supported President Donald Trump's restrictions on travel from Muslim majority countries and refugee immigration and supports repeal of the Affordable Care Act. "]
recombined_text = ''
for sentence in recombine_list:
  recombined_text += sentence
print(recombined_text)

print(33333)
sys.exit()
# import rpunct
from rpunct import RestorePuncts
print("NOTE TO GET THIS TO WORK YOU NEED TO GO IN THE SUB-DEPENDENCY AT THE RIGHT LOCATION AND SWITCH `use_cuda` to False")
rpunct = RestorePuncts(ner_args={"use_cuda": False})
punctuated_recombined_text = rpunct.punctuate(recombined_text)
print(2020202020)
print(punctuated_recombined_text)


# Remove incorrect full stops

# TODO Remove previous full stop after a lower case on a string split of '. '
# Check for lower, if lower remove the prior full stop.



# Pegusas ['The test of your knowledge is your ability to convey it.', 'The ability to convey your knowledge is the ultimate test of your knowledge.', 'The ability to convey your knowledge is the most important test of your knowledge.', 'Your capacity to convey your knowledge is the ultimate test of it.', 'The test of your knowledge is your ability to communicate it.', 'Your capacity to convey your knowledge is the ultimate test of your knowledge.', 'Your capacity to convey your knowledge to another is the ultimate test of your knowledge.', 'Your capacity to convey your knowledge is the most important test of your knowledge.', 'The test of your knowledge is how well you can convey it.', 'Your capacity to convey your knowledge is the ultimate test.']
# [('the test of knowledge is your ability to communicate it to another', 39), ('the ultimate test of knowledge is its ability to communicate with another', 37), ('the most crucial test of knowledge is your ability to communicate it to another', 37), ('the test of knowledge is your ability to convey it to another', 31), ('the ultimate test of your knowledge is your ability to transmit it to another', 24), ('the ultimate test of your knowledge is your ability to transfer it to another', 23), ('the ultimate test of knowledge is your ability to convey it to another', 22), ('the ultimate test of your knowledge is your ability to convey it to another', 17)]

post =  ['The test of your knowledge is your ability to convey it.', 'The ability to convey your knowledge is the ultimate test of your knowledge.', 'The ability to convey your knowledge is the most important test of your knowledge.', 'Your capacity to convey your knowledge is the ultimate test of it.', 'The test of your knowledge is your ability to communicate it.', 'Your capacity to convey your knowledge is the ultimate test of your knowledge.', 'Your capacity to convey your knowledge to another is the ultimate test of your knowledge.', 'Your capacity to convey your knowledge is the most important test of your knowledge.', 'The test of your knowledge is how well you can convey it.', 'Your capacity to convey your knowledge is the ultimate test.']
# save headings
s_words = post.split(" ")
words_with_capitals = []
for word in s_words:
  for letter in word:
    if letter.isupper():
      words_with_capitals.append(word)

words_with_capitals = list(set(words_with_capitals))
print(words_with_capitals)
