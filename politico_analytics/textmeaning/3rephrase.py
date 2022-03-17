# !pip install SentencePiece
# !pip install sentence-splitter

#importing the PEGASUS Transformer model
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
# Takes the input paragraph and splits it into a list of sentences
from sentence_splitter import SentenceSplitter, split_text_into_sentences

model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

# TODO FIX THIS IS ALL WRONG - PULLED FROM THE INTERNET
# IT CONVERTS THE LISTS TO STRING LITERALS OF THE LISTS AND REMOVES THE SQUARE BRACKETS
# SWITCH TO APPENDING LIST OF STRINGS AS SENTENCES INTO A PARAGRAPH

#setting up the model
def get_response(input_text,num_return_sequences):
  batch = tokenizer.prepare_seq2seq_batch([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(torch_device)
  translated = model.generate(**batch,max_length=60,num_beams=10, num_return_sequences=num_return_sequences, temperature=1.5)
  tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
  return tgt_text


#test input sentence
text = "I will be showing you how to build a web application in Python using the SweetViz and its dependent library."
# Paragraph of text
context = "I will be showing you how to build a web application in Python using the SweetViz and its dependent library. Data science combines multiple fields, including statistics, scientific methods, artificial intelligence (AI), and data analysis, to extract value from data. Those who practice data science are called data scientists, and they combine a range of skills to analyze data collected from the web, smartphones, customers, sensors, and other sources to derive actionable insights."
print(context)

# Takes the input paragraph and splits it into a list of sentences
from sentence_splitter import SentenceSplitter, split_text_into_sentences

splitter = SentenceSplitter(language='en')

sentence_list = splitter.split(context)
print("Before: ", sentence_list)
# Do a for loop to iterate through the list of sentences and paraphrase each sentence in the iteration
paraphrase = []

for i in sentence_list:
  a = get_response(i,1)
  paraphrase.append(a)
print("After: ", paraphrase)

#creating the second split
paraphrase2 = [' '.join(x) for x in paraphrase]


# Combine the above splitted lists into a paragraph
paraphrase3 = [' '.join(x for x in paraphrase2) ]
paraphrased_text = str(paraphrase3).strip('[]').strip("'")
# paraphrased_text

# Comparison of the original (context variable) and the paraphrased version (paraphrase3 variable)

print("input: ", context)
print("output: ", paraphrased_text)

# Get individual sentence with 5 options
#printing response
# res = get_response(text, 5)
# print(res)
