# Convert site

# o.co/download/550da43f2e0e3c6fcbcb406862eb7c108d8d3a/

from datetime import datetime as dt

with open('The-Hacker-and-the-State-Cyber-Attacks-and-the-New-Normal-of-Geopolitics-by-Ben-Buchanan-_z-lib.txt') as f:
 book = f.read()

articles = book.split('\n\n\n\n\n\n')

for article in articles:
  with open('./articles/article' + str(dt.now())  + '.txt', 'w') as f:
    f.write(article)

print('Done')
