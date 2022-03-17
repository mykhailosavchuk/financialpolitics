import * as functions from "firebase-functions";
import * as admin from "firebase-admin";

admin.initializeApp();
const db = admin.firestore();
db.settings({ timestampsInSnapshots: true });



export const getRSS = functions.https.onRequest(async (request, response) => {

  // get tweets from database
  let querySnapshot: FirebaseFirestore.QuerySnapshot;
  try {
    querySnapshot = await db
      .collection("newss")
      .orderBy("createdDate", "desc")
      .limit(100)
      .get();
  } catch (err) {
    console.error(err);
  }

  // loop thru each tweet
  querySnapshot.forEach((doc) => {
    const tweet = doc.data();
		// console.log(doc.id, " => ", doc.data());
    // console.log("55555555555555ff")
    // create feed item
    let url_title = `${tweet.title}`.split(' ').join('-').toLowerCase();
    url_title = url_title.replace('?', '%3f')
    console.log(url_title);
    // let url_link = encodeURIComponent(url_title.toLowerCase());


    console.log(4848484848488484848)
    // feed.item({
    //   title: `${tweet.title}`,
    //   description: tweet.content,
    //   url: `https://financial-politics.com/news/${doc.id}/` + url_title,
    //   guid: doc.id,
    //   date: tweet.createdDate,
    //   author: `${tweet.author}`,
    //   categories: tweet.tags,
    // });

  } );

  let rssHeader = "<?xml version='1.0' encoding='UTF-8'?><rss version='2.0'><channel>";

  let title = "<title>Financial Politics</title>";

  let link = "<link>https://financial-politics.com</link>";

  let description = "<description>Your source for Financial and Geopolitical news</description>";

  // You can also generate the posts dinamically using a loop and Firebase's database
  let posts = "<item><title><![CDATA[ US Rep. Michael Garcia traded Tesla Inc, no one's saying insider trading ]]></title><link>https://financial-politics.com/</link><description><![CDATA[ Geo-policies of politics. ]]></description></item><item><title><![CDATA[ onBlur prevents onClick to execute ]]></title><link>https://financial-politics.com/</link><description><![CDATA[ Two solutions. ]]></description></item>";

  let rssFooter = "</channel></rss>";

  let rssString = rssHeader + title + link + description + posts + rssFooter;

  // response.set('Content-Type', 'text/xml');
  // response.contentType("application/rss+xml");


  console.log("tweet122222222");
  response.contentType("application/rss+xml");
  // response.send(feed.xml());
  response.status(200).send(rssString);

});


export const getSitemap = functions.https.onRequest(async (request, response) => {

  let sitemap = `<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
  <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
    <url>
      <loc>https://financial-politics.com/</loc>
      <lastmod>2022-03-06T21:04:59+11:00</lastmod>
      <changefreq>weekly</changefreq>
    </url>
    <url>
      <loc>https://financial-politics.com/aboutus</loc>
      <lastmod>2022-03-06T21:04:59+11:00</lastmod>
      <changefreq>weekly</changefreq>
    </url>
    <url>
      <loc>https://financial-politics.com/news/qv2P2htODvUK6GPgNQ4F/us-rep.-lois-frankel-tradedcitigroup,-pfizer,-lockheed-martin,-medtronic,-pfizer,-and-nxp,-what-does-she-know%3F</loc>
      <lastmod>2022-03-06T21:04:59+11:00</lastmod>
      <changefreq>weekly</changefreq>
    </url>
    <url>
      <loc>https://financial-politics.com/news/tZCJQcR3hi7fl333hlgd/us-rep.-michael-garcia-traded-tesla-inc,-no-one's-saying-insider-trading</loc>
      <lastmod>2022-03-06T21:04:58+11:00</lastmod>
      <changefreq>weekly</changefreq>
    </url>
    <url>
      <loc>https://financial-politics.com/news/DTjmFKIMTWX42LqRYyUM/us-rep.-kathy-manning-traded-amazon.com-inc,-microsoft-corporation,-visa-inc,-match-group,-paypal,-nvidia,-are-they-gonna-explode%3F</loc>
      <lastmod>2022-03-06T21:04:59+11:00</lastmod>
      <changefreq>weekly</changefreq>
    </url>
  <url>
    <loc>https://financial-politics.com/news/SLThKg0JmrzWxbCKHnZQ/us-rep.-bill-keating-traded-general-motors,-is-there-a-secret-to-know%3F</loc>
    <lastmod>2022-03-06T21:06:57+11:00</lastmod>
    <changefreq>weekly</changefreq>
  </url>
  <url>
  <loc>https://financial-politics.com/news/K8CAs6YRJufCB2KtPbfk/nancy-pelosi-exercised-her-call-options-on-walt-disney,-american-express,-paypal-holdings-inc-and-apple,-what-could-this-mean%3F</loc>
    <lastmod>2022-03-06T21:06:59+11:00</lastmod>
    <changefreq>weekly</changefreq>
  </url>
  </urlset>`;

  console.log("tweet13333333333333");
  response.contentType("application/rss+xml");
  response.status(200).send(sitemap);

});


// // const functions = require('firebase-functions');
// const getRss = require('./getRss');
// const getSitemap = require('./getSitemap');

// // Note do below initialization tasks in index.js and
// // NOT in child functions:
// const admin1 = admin.initializeApp();
// // const database = admin.database();
// // admin.initializeApp();

// const db = admin.firestore();
// db.settings({ timestampsInSnapshots: true });


// // Pass database to child functions so they have access to it
// exports.getRss = functions.https.onRequest((req, res) => {
//   getRss.handler(req, res, db, admin1);
// });
// exports.getSitemap = functions.https.onRequest((req, res) => {
//   getSitemap.handler(req, res, db);
// });

// // exports.foo = functions.database.ref('/getRss').onWrite(getRssModule.handler);
// // exports.bar = functions.database.ref('/getSitemap').onWrite(getSitemapModule.handler);

// main must be before functions

// export * from "./getSitemap";

