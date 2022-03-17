import time

start = time.time()
print(1)
from parrot import Parrot
import torch
import warnings
warnings.filterwarnings("ignore")
import sys


'''
Rephrase Unit

Take a paragraph, snapshot the capitals,
Rephrase the paragraph from a list of the paragraph sentences
Rebuild the paragraph.
Re-apply capital letters.
TODO: Apply auto punctuation. Apply truecase (correct potentially incorrect capital letters)
'''

# Replace sentences in string with a list of capitalised substitutes
def recapitalise_from_cap_list(wcaps, recombine_list):
  for caps in wcaps:
    recombine_list = recombine_list.replace(" " + caps.lower(), " " + caps)
  first_char = recombine_list[:1].upper()
  recombine_list = recombine_list[1:]
  recombine_list = first_char + recombine_list
  recombine_list += ". "
  return recombine_list


end = time.time()
print(end - start)


#Init models (make sure you init ONLY once if you integrate this to your code)
print(2)
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
end = time.time()
print(end - start)
print(3)

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
end = time.time()
print(end - start, "   4")


def generate_rephrased_sentence(st):
  phrases = st.split(". ")
  recombine_list = []
  # sys.exit()
  # Rephrase and recombine
  wcaps = []
  for phrase in phrases:

    wcaps = get_words_with_capitals(phrase)
    para_phrases = parrot.augment(input_phrase=phrase, do_diverse = True)

    if len(para_phrases) > 1:
      fixed_string = recapitalise_from_cap_list(wcaps, para_phrases[1][0])
    else:
        fixed_string = recapitalise_from_cap_list(wcaps, para_phrases[0][0])

    recombine_list.append(fixed_string)

  recombined_text = ''
  for sentence in recombine_list:
    recombined_text += sentence
  return recombined_text

# s = "Michael Clifton Burgess is an American physician and politician representing Texas's 26th congressional district in the United States House of Representatives. The district is anchored in Denton County, a suburban county north of Dallas and Fort Worth. In 2002, Burgess defeated Scott Armey, the son of House Majority Leader and then U.S. Representative Dick Armey, in a primary runoff election. Before his election, he practiced as a doctor of obstetrics and gynecology. Burgess is a member of the congressional Tea Party Caucus, and has been involved in the debates over health care reform and energy policy. He opposes abortion, is unsure of the extent of the contribution of human activity to global warming, supported President Donald Trump's restrictions on travel from Muslim majority countries and refugee immigration, and supports the repeal of the Affordable Care Act."

rephrased_text = generate_rephrased_sentence(s)
print(rephrased_text)

