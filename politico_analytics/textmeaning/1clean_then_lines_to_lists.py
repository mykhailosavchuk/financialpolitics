import glob
import sys
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
import re
import heapq
import numpy as np
import pandas as pd
import sys

from datetime import datetime as dt


def main():
    files = glob.glob("./test_folder/*.txt")

    print(files)

    for file in files:

      # Get the intent of the paragraph

      # Get the cleaned list of sentences to rephrase
      with open(file) as f:
        paragraph = f.read()
        paragraph = paragraph.strip() # Read and remove trailing and beginning newlines
        sentences = paragraph.split('\n')[1:]

      title = './articles_clean/article' + str(dt.now())  + '.txt'
      sentences = list(filter(None, sentences)) # remove empty strings
      print("=========Start===========")
      # print(sentences)
      for sentence in sentences:
        # print(sentence)
        sentence = re.sub('\n', '', sentence)
        sentence = re.sub("\\\.", '.', sentence)

        # print(sentence)
      # # Write cleaned list to file
        with open(title, 'a+') as f:
          f.write(sentence + '\n\n')


        # print(sentences)
        # sys.exit()

#     file_name = input('1. Enter text file name: ')
#     output_location = input('2. Enter output file name (e.g. summary.txt): ')
#     sent_word_length = input('3. Enter max sentence word length (choose between 25 - 30): ')
#     top_n = input('4. Enter number of sentences you want in summary (choose between 3 - 5): ')

#     def read_text(file_name):
#         """
#         Read text from file
#         INPUT:
#         file_name - Text file containing original text.
#         OUTPUT:
#         text - str. Text with reference number, i.e. [1], [10] replaced with space, if any...
#         clean_text - str. Lowercase characters with digits & one or more spaces replaced with single space.
#         """
#         with open(file_name, 'r') as f:
#             file_data = f.read()

#         text = file_data
#         text = re.sub(r'\[[0-9]*\]',' ',text)
#         text = re.sub(r'\s+',' ',text)

#         clean_text = text.lower()

#         # replace characters other than [a-zA-Z0-9], digits & one or more spaces with single space
#         regex_patterns = [r'\W',r'\d',r'\s+']
#         for regex in regex_patterns:
#             clean_text = re.sub(regex,' ',clean_text)

#         return text, clean_text

#     def rank_sentence(text, clean_text, sent_word_length):
#         """
#         Rank each sentence and return sentence score
#         INPUT:
#         text - str. Text with reference numbers, i.e. [1], [10] removed, if any...
#         clean_text - str. Clean lowercase characters with digits and additional spaces removed.
#         sent_word_length - int. Maximum number of words in a sentence.
#         OUTPUT:
#         sentence_score - dict. Sentence score
#         """
#         sentences = nltk.sent_tokenize(text)
#         stop_words = nltk.corpus.stopwords.words('english')

#         word_count = {}
#         for word in nltk.word_tokenize(clean_text):
#             if word not in stop_words:
#                 if word not in word_count.keys():
#                     word_count[word] = 1
#                 else:
#                     word_count[word] += 1

#         sentence_score = {}
#         for sentence in sentences:
#             for word in nltk.word_tokenize(sentence.lower()):
#                 if word in word_count.keys():
#                     if len(sentence.split(' ')) < int(sent_word_length):
#                         if sentence not in sentence_score.keys():
#                             sentence_score[sentence] = word_count[word]
#                         else:
#                             sentence_score[sentence] += word_count[word]

#         return sentence_score

#     def generate_summary(file_name, sent_word_length, top_n):
#         """
#         Generate summary
#         INPUT:
#         file_name - Text file containing original text.
#         sent_word_length - int. Maximum number of words in a sentence.
#         top_n - int. Top n sentences to display.
#         OUTPUT:
#         summarized_text - str. Summarized text with each sentence on each line.
#         """
#         text, clean_text = read_text(file_name)

#         sentence_score = rank_sentence(text, clean_text, sent_word_length)

#         best_sentences = heapq.nlargest(int(top_n), sentence_score, key=sentence_score.get)

#         summarized_text = []

#         sentences = nltk.sent_tokenize(text)

#         for sentence in sentences:
#             if sentence in best_sentences:
#                 summarized_text.append(sentence)

#         summarized_text = "\n".join(summarized_text)

#         return summarized_text

#     # generate summary
#     summary = generate_summary(file_name, sent_word_length, top_n)

#     # save summary to txt file
#     text_file = open(output_location, "w")
#     text_file.write(summary)
#     text_file.close()
#     print('Summarization task completed. Please check your output file.')
if __name__ == '__main__':
  main()
    # main( *sys.argv[1:] )



