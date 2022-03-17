import requests
import json
from datetime import datetime, timedelta
yesterday = datetime.now() - timedelta(1)

# https://housestockwatcher.com/api


# TODO: Weekend / Weekday logic
# No trades happen on the weekend, so weekday the check should be today / yesterday
# UPDATE Before Release
def yesterday(string=False, frmt='%Y-%m-%d'):
    yesterday = datetime.now() - timedelta(5)
    if string:
        return yesterday.strftime(frmt)
    return yesterday

d = yesterday(True, '%m_%d_%Y')



#  WRITE TO FIRESTORE DB
# SET UP FORESTORE CLIENT
cred = credentials.Certificate("/Users/julian/apps_node/politicostockpicker/politico_analytics/politicostockpicker-firebase-adminsdk-4afbl-504d6cea02.json")
firebase_admin.initialize_app(cred)

# initialize firestore instance
firestore_db = firestore.client()

# datetime string
dt = datetime.datetime.now() 
dt_string = dt.strftime("%m-%d-%Y %H:%M")

#url = ("https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/transaction_report_for_12_31_2021.json")
url = ("https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/transaction_report_for_" + d +".json")
response = requests.get(url)
representative_list = response.json()
representative_list = [{'prefix': 'Hon.', 'first_name': 'Michael C.', 'last_name': 'Burgess', 'suffix': None, 'name': 'Hon. Michael C. Burgess', 'filing_date': '12/31/2021', 'document_id': '20019995', 'year': 2021, 'district': 'TX26', 'source_ptr_link': 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2021/20019995.pdf', 'transactions': [{'owner': None, 'transaction_date': '2021-12-02', 'ticker': 'ABT', 'description': 'Abbott Laboratories', 'transaction_type': 'purchase', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}, {'owner': None, 'transaction_date': '2021-11-19', 'ticker': 'CI', 'description': 'Cigna Corporation', 'transaction_type': 'sale_partial', 'amount': '$15,001 - $50,000', 'cap_gains_over_200': False}, {'owner': None, 'transaction_date': '2021-12-02', 'ticker': 'MSFT', 'description': 'Microsoft Corporation', 'transaction_type': 'purchase', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}, {'owner': None, 'transaction_date': '2021-11-23', 'ticker': 'SYK', 'description': 'Stryker Corporation', 'transaction_type': 'sale_partial', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}, {'owner': None, 'transaction_date': '2021-12-21', 'ticker': 'SYK', 'description': 'Stryker Corporation', 'transaction_type': 'sale_partial', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}, {'owner': 'self', 'transaction_date': '2021-12-21', 'ticker': 'SYK', 'description': 'Stryker Corporation', 'transaction_type': 'sale_partial', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}, {'owner': None, 'transaction_date': '2021-12-02', 'ticker': 'DIS', 'description': 'Walt Disney Company', 'transaction_type': 'purchase', 'amount': '$1,001 - $15,000', 'cap_gains_over_200': False}], 'transcribed_by': 'Timothy Carambat'}]

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

  # Build the string
  tickers = ', '.join(ticker_list)
  p = "Representative " + rep['first_name'] + " " + rep['last_name'] + " traded " + tickers + ". Are they the next big buy?\n\n"+ rep['name'] + " filed the following stock market transactions on the " + rep['filing_date'] + ": \n"
  print(p)

  ## Update the transaction type to "Sell" and "Purchase"
  for trans in rep['transactions']:
    if trans['transaction_type'] != "purchase":
      trans['transaction_type'] = "Sell"
    else: trans['transaction_type'] = "Purchase"

    l =  "Stock: " + trans['description'] + ", Ticker: " + trans['ticker'] + ", Transcaction Type: " + trans['transaction_type'] + ", Amount: " + trans["amount"] + ', Transaction Date: ' + trans['transaction_date']
    print(l)
  k = "\nDon't believe it?\nCheck the source: " + rep["source_ptr_link"]
  print(k)
  # import sys
  # sys.exit()

  # "<p>This is test 2</p><p>&nbsp;</p><p>&lt;href=www.google.com&gt;i wonfer how this will look&lt;/href&gt;</p><p>&nbsp;</p><p>I wonder how this will look with: <a href="https://www.google.com">this hyperlink</a></p><p>&lt;h1&gt;Test H1&lt;/h1&gt;</p>"
