
import wikipedia
import re

# Get the first 6 sentences from a wiki article
def wiki_content(search_term, n_sentences=7):
  page = wikipedia.page(search_term)
  paragraphs = page.content
  paragraphs = re.sub("[\(\[].*?[\)\]]", "", paragraphs) # Remove brackets from content
  paragraphs = re.sub("  ", " ", paragraphs) # Remove Double Space
  paragraphs = re.sub(" \.", ".", paragraphs) # Remove brackets from content
  paragraphs = re.sub("-", " ", paragraphs) # Remove dash from content
  paragraphs = ' '.join(re.split(r'(?<=[.:;])\s', paragraphs)[:n_sentences]) # Take the first ~6 sentences
  return paragraphs

content = wiki_content('Michael C Burgess')
print(content)
