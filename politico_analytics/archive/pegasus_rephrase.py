import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import time

start = time.time()

end = time.time()
print(end - start)

s = "Michael Clifton Burgess is an American physician and politician representing Texas's 26th congressional district in the United States House of Representatives. The district is anchored in Denton County, a suburban county north of Dallas and Fort Worth. In 2002, Burgess defeated Scott Armey, the son of House Majority Leader and then U.S. Representative Dick Armey, in a primary runoff election. Before his election, he practiced as a doctor of obstetrics and gynecology. Burgess is a member of the congressional Tea Party Caucus, and has been involved in the debates over health care reform and energy policy. He opposes abortion, is unsure of the extent of the contribution of human activity to global warming, supported President Donald Trump's restrictions on travel from Muslim majority countries and refugee immigration, and supports the repeal of the Affordable Care Act."
phrases = s.split(". ")
print(phrases)
end = time.time()
print(end - start)
print(4)



model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

def get_response(input_text,num_return_sequences,num_beams):
  batch = tokenizer([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(torch_device)
  translated = model.generate(**batch,max_length=60,num_beams=num_beams, num_return_sequences=num_return_sequences, temperature=1.5)
  tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
  return tgt_text


num_beams = 10
num_return_sequences = 10
# context = "The ultimate test of your knowledge is your capacity to convey it to another."
# k = get_response(context,num_return_sequences,num_beams)
# print(k)

# Rephrase and recombine
for phrase in phrases:
  print(5)
  end = time.time()
  print(end - start)
  print("-"*100)
  print("Input_phrase: ", phrase)
  print("-"*100)
  num_beams = 10
  num_return_sequences = 10

  # para_phrases = parrot.augment(input_phrase=phrase, do_diverse = False)
  para_phrases = get_response(phrase,num_return_sequences,num_beams)
  time.sleep(3)
  print("Sleep 3 ..")

  print(para_phrases)
  # import sys
  # sys.exit()
end = time.time()
print(end - start)
print(6)
# Preserve and re-apply capital letters


# ['The test of your knowledge is your ability to convey it.
#'The ability to convey your knowledge is the ultimate test of your knowledge.
#'The ability to convey your knowledge is the most important test of your knowledge.
#'Your capacity to convey your knowledge is the ultimate test of it.
#'The test of your knowledge is your ability to communicate it.
#'Your capacity to convey your knowledge is the ultimate test of your knowledge.
#'Your capacity to convey your knowledge to another is the ultimate test of your knowledge.
#'Your capacity to convey your knowledge is the most important test of your knowledge.
#'The test of your knowledge is how well you can convey it.
#'Your capacity to convey your knowledge is the ultimate test.']
