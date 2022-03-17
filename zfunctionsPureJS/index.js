const functions = require("firebase-functions");

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//   functions.logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });
exports.builRSS = functions.https.onRequest((request, response) => {

  let rssHeader = "<?xml version='1.0' encoding='UTF-8'?><rss version='2.0'><channel>";

  let title = "<title>Erik Martín Jordán</title>";

  let link = "<link>https://erikmartinjordan.com</link>";

  let description = "<description>Code, web development, tech and off-topic</description>";

  // You can also generate the posts dinamically using a loop and Firebase's database
  let posts = "<item><title><![CDATA[ Quick way to transform a number into a string using JavaScript ]]></title><link>https://erikmartinjordan.com/quick-way-number-string-javascript</link><description><![CDATA[ Quick way to transform a number into a string using JavaScript. ]]></description></item><item><title><![CDATA[ onBlur prevents onClick to execute ]]></title><link>https://erikmartinjordan.com/onblur-prevents-onclick-react</link><description><![CDATA[ Two solutions on how to prevent the onBlur event cancelling the onClick. ]]></description></item>";

  let rssFooter = "</channel></rss>";

  let rssString = rssHeader + title + link + description + posts + rssFooter;

  response.set('Content-Type', 'text/xml');
  response.status(200).send(rssString);

})
