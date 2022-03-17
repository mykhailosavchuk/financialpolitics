from unittest import result
from GoogleNews import GoogleNews



googlenews = GoogleNews(period='7d', region='US', lang='en')
print(googlenews.getVersion())

def stock_headlines(stock_name):

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

  content_dict = {'news_link' : [], 'news_img' : []}
  first_image_url_counter = 0
  for link in l:
    # print(link)
    content_dict['news_link'].append('<a target="_blank" href='+ link['url'] +'>'+ link['title'] +'</a>')
    content_dict['img_url'].append(link['img'])

    print(link['title'])
    print(link['link'])
    print(link['img'])
    first_image_url_counter +=1
    print(59595959955)

    if first_image_url_counter == 6:
      first_image_url_counter = 0
      break
  return content_dict



  # TODO APPREND TOP FIVE LINKS< TITLES AND IMAGES TO A STRING AS HTML
# m = googlenews.get_texts()
# print(m)
# print(11111)
# n = googlenews.get_links()
# print(n)
# print("opopopop")
# googlenews.clear()

