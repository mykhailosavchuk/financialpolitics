import time
import random

start = time.time()
print(1)
from parrot import Parrot
import torch
import warnings
warnings.filterwarnings("ignore")
import sys
# pip install git+https://github.com/PrithivirajDamodaran/Parrot.git

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

def add_nlp_sentence_kicker(title_start):
  post_title_kicker = [
    'are they the next big buys?',
    'are they going to rocket?',
    'how soon will they move?',
    'are they the next big buys?',
    'do they know something about these stocks?',
    'is there something special to know?',
    'why?',
    "nobody's saying insider trading",
    "is the bull run to begin?",
    "what's the secret?",
    "what does this mean?",
    'is there a secret?',
    'what they traded',
    'are they going to blow up?',
    'are they going to explode?']
  kicker = random.choice(post_title_kicker)
  para_phrases = parrot.augment(input_phrase=kicker, do_diverse = True)

  nkicker = random.choice(para_phrases)
  while 'illegal' in nkicker[0]:
    nkicker = random.choice(para_phrases)
  title_start +=nkicker[0]
  return title_start


s =  'US rep. Michael C. Burgess traded Cigna Corporation, Stryker Corporation, Microsoft Corporation, Walt Disney Company, Abbott Laboratories - '
k = add_nlp_sentence_kicker(s)
print(k)
# run through algorithm
# sys.exit()


# print(phrases)
end = time.time()
print(end - start)
print(4)

# sys.exit()
# Rephrase and recombine
# for phrase in phrases:
#   print(5)
#   end = time.time()
#   print(end - start)
#   print("-"*100)
#   print("Input_phrase: ", phrase)
#   print("-"*100)
#   para_phrases = parrot.augment(input_phrase=phrase, do_diverse = False)
#   print(para_phrases)
  # import sys
#   # sys.exit()
# end = time.time()
# print(end - start)
# print(6)
# Preserve and re-apply capital letters


# Pegusas ['The test of your knowledge is your ability to convey it.', 'The ability to convey your knowledge is the ultimate test of your knowledge.', 'The ability to convey your knowledge is the most important test of your knowledge.', 'Your capacity to convey your knowledge is the ultimate test of it.', 'The test of your knowledge is your ability to communicate it.', 'Your capacity to convey your knowledge is the ultimate test of your knowledge.', 'Your capacity to convey your knowledge to another is the ultimate test of your knowledge.', 'Your capacity to convey your knowledge is the most important test of your knowledge.', 'The test of your knowledge is how well you can convey it.', 'Your capacity to convey your knowledge is the ultimate test.']
# [('the test of knowledge is your ability to communicate it to another', 39), ('the ultimate test of knowledge is its ability to communicate with another', 37), ('the most crucial test of knowledge is your ability to communicate it to another', 37), ('the test of knowledge is your ability to convey it to another', 31), ('the ultimate test of your knowledge is your ability to transmit it to another', 24), ('the ultimate test of your knowledge is your ability to transfer it to another', 23), ('the ultimate test of knowledge is your ability to convey it to another', 22), ('the ultimate test of your knowledge is your ability to convey it to another', 17)]
