import glob
import re
import sys
import sys

import numpy as np
import pandas as pd

from datetime import datetime as dt


# Set the model for Text Summary
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")

from parrot import Parrot
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)

def main():
    files = glob.glob("./articles_clean/*.txt")

    for file in files:
      print("Filename: ", file)
      # Generate a potential title
      # title = generate_title(file)
      # print(title)
      sys.exit()


def generate_title(file_name):
  '''Generate Title of text from a file location
    input: location of file, i.e ./articles_clean/article1.txt
    output: title for article
  '''
  # Get the cleaned list of sentences to rephrase
  with open(file_name) as f:
    paragraph = f.read()
    paragraph = paragraph.strip() # Read and remove trailing and beginning newlines

  inputs = tokenizer(paragraph, max_length=1024, return_tensors="pt")

  # Generate Summary
  summary_ids = model.generate(inputs["input_ids"])
  title = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
  return title

if __name__ == '__main__':
  main()
    # main( *sys.argv[1:] )


