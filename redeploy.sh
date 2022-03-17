# Redeploy to the website

# Remove prior prod build, create new build, and deploy to firebase

rm -rf ./dist
rm -rf ./public
npm run prod
cp -r ./dist ./public
firebase deploy
