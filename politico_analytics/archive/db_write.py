import firebase_admin
from firebase_admin import credentials, firestore
import datetime

#  WRITE TO FIRESTORE DB

cred = credentials.Certificate("/Users/julian/apps_node/politicostockpicker/politico_analytics/politicostockpicker-firebase-adminsdk-4afbl-504d6cea02.json")
firebase_admin.initialize_app(cred)

# initialize firestore instance
firestore_db = firestore.client()

# datetime string
dt = datetime.datetime.now()
dt_string = dt.strftime("%m-%d-%Y %H:%M")

# Get small image
# TODO Get larger images - uplift function
from bs4 import BeautifulSoup
import requests
def get_image_link():
    theurl = "https://www.google.com/search?q=paul+ryan&source=lnms&tbm=isch&sa=X&ved=2ahUKEwigpaasq7b1AhWsUGwGHbSwC3AQ_AUoAXoECAIQAw&biw=1374&bih=706&dpr=1"
    r = requests.get(theurl)
    soup = BeautifulSoup(r.text, "lxml")
    image = soup.findAll('img', src=True)
    return image
link = get_image_link()
print(link[1])

link = link[1]

# TODO Build up content, include auto image, merge with main.py
# Create the content to upload as HTML with inline CSS
content = '<p>This is a link</p><p>&nbsp;</p><p>This is a <a href="https://www.google.com">hyperlink</a>.<img style="float: right !important;" src=https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Official_photo_of_Speaker_Nancy_Pelosi_in_2019.jpg/220px-Official_photo_of_Speaker_Nancy_Pelosi_in_2019.jpg alt="Nancy Pelosi" width="200" height="200"></p><p>Follow on sentence1.</p>'
content += '''<table>
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
</table>'''

# add data
firestore_db.collection(u'newss').add(
    {
        'author': 'Data Informatics',
        'content': content,


        'title' : "Test 40",
        'createdDate' : dt_string
    })

# read data
# snapshots = list(firestore_db.collection(u'newss').get())
# for snapshot in snapshots:
#     print(snapshot.to_dict())
