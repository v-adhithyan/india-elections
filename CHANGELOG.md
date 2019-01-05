# Changelog

## 01.01.2019
- Storing tweet text along with cleaned text, sentiment and search term as a record in db.
- /index/ path shows sentiment analysis of upa and nda along with count of tweets.

## 04.01.2019
- Changed the code to store generated wordcloud path in db. This is to make sure that we 
do not generate wordcloud again and again which is compute intensive and unnecessary for a
same query. So from now if wordcloud does not exists for a query it will be 
generated and path will be saved to db along with query.