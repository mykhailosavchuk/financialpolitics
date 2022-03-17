from bs4 import BeautifulSoup
import requests
from datetime import timedelta, date
import datetime
import re
import wikipedia
from GoogleNews import GoogleNews
import time
import sys
import firebase_admin
from firebase_admin import credentials, firestore
import random
# news ap https://github.com/mattlisiv/newsapi-python
# grammar fixer
# https://pypi.org/project/gingerit/

import wikipedia
import requests
import json
import time
import random
import torch
import warnings
warnings.filterwarnings("ignore")
import sys
start = time.time()
import re
earlier_days = 6

end = time.time()
print(end - start)


#Init models (make sure you init ONLY once if you integrate this to your code)
print(2)
print(1)
from parrot import Parrot
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
end = time.time()
print(end - start)
print(3)


WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

# Get the first 6 sentences from a wiki article
def wiki_content(search_term, n_sentences=8):
  try:
    page = wikipedia.page('Representative ' + search_term)
  except:
    page = wikipedia.page(search_term)

  paragraphs = page.content
  paragraphs = re.sub("[\(\[].*?[\)\]]", "", paragraphs) # Remove brackets from content
  paragraphs = re.sub("  ", " ", paragraphs) # Remove Double Space
  paragraphs = re.sub(" \.", ".", paragraphs) # Remove brackets from content
  paragraphs = re.sub("-", " ", paragraphs) # Remove dash from content
  paragraphs = re.sub(r'==.*==', "", paragraphs) # Remove headings, contained in double equals '== =='
  paragraphs = ' '.join(re.split(r'(?<=[.:;])\s', paragraphs)[:n_sentences]) # Take the first ~6 sentences
  
  return paragraphs

def get_wiki_image(search_term):
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)

        # Filter for jpeg's and png's from total wiki image list
        wiki_images = []
        for media in wkpage.images:
          if '.jpeg' in media or '.jpg' in media or '.png' in media:
            wiki_images.append(media)

        # Try three times to get a more casual than their official photo
        img = random.choice(wiki_images)
        lim = 0
        while 'official' in img.lower():
          img = random.choice(wiki_images)
          lim +=1
          if lim == 3:
            break

        # img = wiki_images
        return img
    except:
        return 0
# wiki_image = get_wiki_image('Nancy Pelosi')
# print(wiki_image)
# import sys

# sys.exit()

def stock_headlines(stock_name):
  googlenews = GoogleNews(period='7d', region='US', lang='en')

  j = googlenews.get_news(stock_name)
  # print(j)
  print(181818)
  k = googlenews.search(stock_name)
  # print(k)
  # print(959595)
  l = googlenews.results(sort=True)
  print(l)
  print(44848484)
  print("Total countr: " + str(googlenews.total_count()))

  content_dict = {'news_link' : [], 'img_url' : []}
  first_image_url_counter = 0
  for link in l:
    # print(link)
    content_dict['news_link'].append('<a target="_blank" href='+ 'https://' + link['link'] +'>'+ link['title'] +'</a>')
    content_dict['img_url'].append(link['img'])

    print(link['title'])
    print(link['link'])
    print(link['img'])
    first_image_url_counter +=1
    print(59595959955)

    if first_image_url_counter == 5:
      googlenews.clear()
      first_image_url_counter = 0
      break
  return content_dict


# https://housestockwatcher.com/api
#  WRITE TO FIRESTORE DB
# SET UP FORESTORE CLIENT
# cred = credentials.Certificate("/Users/julian/apps_node/politicostockpicker/politico_analytics/politicostockpicker-firebase-adminsdk-4afbl-504d6cea02.json")
cred = credentials.Certificate("/Users/julian/apps_node/politicostockpicker/politico_analytics/financialpolitics-4242f-firebase-adminsdk-59amv-c6e7882bfc.json")
firebase_admin.initialize_app(cred)

# initialize firestore instance
firestore_db = firestore.client()

# datetime string
dt = datetime.datetime.now()
dt_string = dt.strftime("%m-%d-%Y %H:%M")


# Get small image
# TODO Get larger images - uplift function
def get_image_URLS(google_query):
    theurl = "https://www.google.com/search?q=" + google_query + "&source=lnms&tbm=isch&sa=X&ved=2ahUKEwigpaasq7b1AhWsUGwGHbSwC3AQ_AUoAXoECAIQAw&biw=1374&bih=706&dpr=1"
    r = requests.get(theurl)
    soup = BeautifulSoup(r.text, "lxml")
    images = soup.findAll('img', src=True)
    return images

# Add a curious addition to the heading
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

# TODO: Weekend / Weekday logic
# No trades happen on the weekend, so weekday the check should be today / yesterday
# UPDATE Before Release
def earlier_day(number_days, string=False, frmt='%Y-%m-%d'):
    yesterday = datetime.datetime.now() - timedelta(number_days)
    if string:
        return yesterday.strftime(frmt)
    return yesterday

d = earlier_day(earlier_days,True, '%m_%d_%Y')

# url = ("https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/transaction_report_for_12_31_2021.json")
url = ("https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/transaction_report_for_" + d +".json")
response = requests.get(url)
representative_list = response.json()
# representative_list = [{'prefix': 'Hon.', 'first_name': 'Michael C.', 'last_name': 'Burgess', 'suffix': None, 'name': 'Hon. Michael C. Burgess', 'filing_date': '12/31/2021', 'document_id': '20019995', 'year': 2021, 'district': 'TX26', 'source_ptr_link': 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2021/20019995.pdf', 'transactions': [{'owner': None, 'transaction_date': '2021-12-02', 'ticker': 'ABT', 'description': 'Abbott Laboratories', 'transaction_type': 'purchase', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}, {'owner': None, 'transaction_date': '2021-11-19', 'ticker': 'CI', 'description': 'Cigna Corporation', 'transaction_type': 'sale_partial', 'amount': '$15,001 - $50,000', 'cap_gains_over_200': False}, {'owner': None, 'transaction_date': '2021-12-02', 'ticker': 'MSFT', 'description': 'Microsoft Corporation', 'transaction_type': 'purchase', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}, {'owner': None, 'transaction_date': '2021-11-23', 'ticker': 'SYK', 'description': 'Stryker Corporation', 'transaction_type': 'sale_partial', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}, {'owner': None, 'transaction_date': '2021-12-21', 'ticker': 'SYK', 'description': 'Stryker Corporation', 'transaction_type': 'sale_partial', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}, {'owner': 'self', 'transaction_date': '2021-12-21', 'ticker': 'SYK', 'description': 'Stryker Corporation', 'transaction_type': 'sale_partial', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}, {'owner': None, 'transaction_date': '2021-12-02', 'ticker': 'DIS', 'description': 'Walt Disney Company', 'transaction_type': 'purchase', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}], 'transcribed_by': 'Timothy Carambat'}]

# Print the Congressmen who traded and what they traded
for rep in representative_list:
  # Get the list of stocks traded by name and ticker
  stock_list = []
  ticker_list = []
  for activity in rep['transactions']:
    print(activity)
    stock_list.append(activity['description'])
    ticker_list.append(activity['ticker'])
  stock_list = list(set(stock_list))
  ticker_list = list(set(ticker_list))
  ### Finish logic

  # Generate tags payload
  tag_generator = [ rep['first_name']+ " " +rep['last_name']]
  tag_generator.append('finance')
  for stock in stock_list:
    tag_generator.append(stock)
  for ticker in ticker_list:
    tag_generator.append(ticker)
  print(tag_generator)

  # Build the string
  tickers = ', '.join(ticker_list)
  stocks = ', '.join(stock_list)
  post_title = "US representative " + rep['first_name'] + " " + rep['last_name'] + " traded " + stocks + ", "
  post_title = add_nlp_sentence_kicker(post_title)
  # print(img_list[1])
  img = get_wiki_image(rep['first_name'] + " " + rep['last_name'])
  wiki_text = wiki_content(rep['first_name'] + " " + rep['last_name'])

  # Rephrase wiki text

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
    # Split the paragraph to sentences, rephrase, 
    # re-apply capital letters and recombine paragraph.
    phrases = st.split(". ")
    recombine_list = []
    # sys.exit()
    # Rephrase and recombine
    wcaps = []
    for phrase in phrases:

      wcaps = get_words_with_capitals(phrase)
      para_phrases = parrot.augment(input_phrase=phrase, do_diverse = True)

      # If there is paraphased text, take the 2nd most similar sentence, 
      # if the 2nd most similar is non-existant, then take the first.
      if para_phrases is not None:
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
  # print(wiki_text)
  # rephrased_text = generate_rephrased_sentence(wiki_text)
  # print(rephrased_text)

  try:
    print(wiki_text)
    rephrased_text = generate_rephrased_sentence(wiki_text)
    print(rephrased_text)
  except:
    print("Could not wiki search for details, skip this congressman..")
    print(wiki_text)
    continue


  # img = img_list[1]
  spoken_date = date(day=int(rep['filing_date'][3:5]), month=int(rep['filing_date'][:2]), year=int(rep['filing_date'][6:11])).strftime('%A %d %B %Y')

  content = "<h2 style='width: 200px; float: left;'>Representative " + rep['first_name'] + " " + rep['last_name'] + " traded " + tickers + " this week.\n\n</h2>"

  content += '<img style="margin-left: 30px !important; " src=' + str(img) + ' alt="'+ rep['first_name'] + ' ' + rep['last_name'] + '">'

  content += '<p>' +  rep['name'] + " filed a financial disclosure report on the " + spoken_date + " to trade " + stocks + ".</p>"
  # content += '<img style="float: right !important; display: inline-block; margin-left: 30px !important; " src=' + img['src'] + 'alt="'+ rep['first_name'] + ' ' + rep['last_name'] + '" width="180px" height="auto !important">'
  content +='<p>' + wiki_text + '</p>'

  content += '<p>' +  rep['name'] + " filed the following stock market transactions on the " + rep['filing_date'] + ':\n</p>'
  # '<p>This is a link</p><p>&nbsp;</p><p>This is a <a href="https://www.google.com">hyperlink</a>.<img style="float: right; !important; display: block; " src=https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Official_photo_of_Speaker_Nancy_Pelosi_in_2019.jpg/220px-Official_photo_of_Speaker_Nancy_Pelosi_in_2019.jpg alt="Nancy Pelosi" width="200" height="200"></p><p>Follow on sentence1.</p>'
  print(content)

  # BEGIN THE TABLE
  content += '<table id="trades"><tr><th>Stock</th><th>Ticker</th><th>Type</th><th>Amount</th><th>Transaction Date</th></tr>'
  ## Update the transaction type to "Sell" and "Purchase"
  for trans in rep['transactions']:
    if trans['transaction_type'] != "purchase":
      trans['transaction_type'] = "Sell"
    else: trans['transaction_type'] = "Purchase"

    content += "<tr><td>" + trans['description'] + "</td><td>" + trans['ticker'] + "</td><td>" + trans['transaction_type'] + "</td><td>" + trans["amount"]  + "</td><td>" + trans['transaction_date'] + "</td></tr>"
    # content +=  "Stock: " + trans['description'] + ", Ticker: " + trans['ticker'] + ", Transcaction Type: " + trans['transaction_type'] + ", Amount: " + trans["amount"] + ', Transaction Date: ' + trans['transaction_date']

    print(content)
  content +='</table><br><br>'
  # FINISH THE TABLE

  for s in stock_list:
    result = ''
    print('')
  #   items_to_remove = ['Company', 'Corporation']
  #   for i in items_to_remove:
  #       result = stock.replace(i,'')
    stock_news_bites = stock_headlines(s)
    print("news for " + s)
    print(stock_news_bites)
    # stock_news_bites = {'news_link': ['<a target="_blank" href=https://www.theverge.com/2022/1/25/22901755/halo-infinite-forza-horizon-5-player-numbers-microsoft-xbox-game-pass-free-to-play>Microsoft got a whole lot of people to play Halo and Forza</a>', '<a target="_blank" href=https://www.theverge.com/2022/1/25/22901676/call-of-duty-sony-playstation-microsoft-xbox-activision-acquisition-deal>Call of Duty’s next three games will hit PlayStation despite Microsoft’s Activision deal</a>', '<a target="_blank" href=https://www.theverge.com/2022/1/25/22901146/activision-blizzard-new-survival-game-announcement>Blizzard announces new survival game while still reeling from multiple controversies</a>', '<a target="_blank" href=https://www.wsj.com/articles/microsoft-msft-q2-earnings-report-2022-11643112605?mod=hp_lead_pos3>Microsoft Earnings Likely Grew Last Quarter With Demand for Cloud Services</a>'], 'img_url': ['https://cdn.vox-cdn.com/thumbor/E6ya3puqs0LB_Bii4NX367fsXh0=/0x0:2128x1114/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/20108409/halo_infinite_keyart_primary_horiz_9e788e276ba740e3af6451ef073fd3de.png', 'https://cdn.vox-cdn.com/thumbor/mHgRpjH7HdC_XjUCr0omCbn5syI=/0x39:2040x1107/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/22015304/vpavic_4278_20201030_0247.jpg', 'https://cdn.vox-cdn.com/thumbor/ZTF3Uy-gIOQmNvGxKdLU9pnh1Wk=/0x0:1198x627/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/23194259/FJ93_vCVQAgJldM.jpg', 'https://images.wsj.net/im-472721/social']}
    print("11222222")
    # print(stock_news_bites['img_url'][0])
    try:
      wikipage = wikipedia.page(s)

      stock_img_url = wikipage.images[1]
    except:
      print("failing to get a wikipedia image for " + s)
      print("performing google search  for image.. fix later to be high res " )
      g = get_image_URLS(stock_list[0])
      print(" g:" , g)
      print("g type : ", type(g))
      stock_img_url = g[0]['src']
      print("actually for the meantime pass on this congressman .. FIX SOON@!@!")
      continue
    print(stock_img_url)
    print("899999999")
    # print(stock_news_bites)
    print('Completed link gathering from Google, sleep for 5 seconds ..')
    time.sleep(5)

    # print(stock_news_bites)
    content +='<h3>Find out what the latest news about ' + s +' </h3>'
    content += '<img style="float: right !important; " src='+stock_img_url+ ' alt=' + s +' width="auto" height="140px !important">'
  #   # import sys
  #   # sys.exit()

    for link in stock_news_bites['news_link']:
      content += link
      content += '<br>'


  content += "<br><p>Don't believe it?<br>Check the source " + '<b><a target="_blank" rel="noopener noreferrer" href='+ rep["source_ptr_link"] +'>over here</a></b>' + " from the US House of Representatives financial disclosures.</p>"
  # k = get_source('https://mises.org/feed/rss.xml')
  # content += k.text
  print(content)
  post_title = post_title.replace('representative', 'Rep.')
  firestore_db.collection(u'newss').add(
    {
        'author': 'Data Informatics',
        'content': content,
        'title' : post_title,
        'createdDate' : dt_string,
        'img_url' : img,
        'tags' : tag_generator
    })
  tag_generator = []
