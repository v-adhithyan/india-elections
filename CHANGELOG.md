# Changelog

## 01.01.2019
- Storing tweet text along with cleaned text, sentiment and search term (hereafter will be referred as query) as a record in db.
- /index/ path shows sentiment analysis of upa and nda along with count of tweets.

## 04.01.2019
- Changed the code to store generated wordcloud path in db. This is to make sure that we 
do not generate wordcloud again and again which is compute intensive and unnecessary for a
same query. So from now if wordcloud does not exists for a query it will be 
generated and path will be saved to db along with query.

## 14.01.2019
- Previously full tweets are stored. This adds space. So to save space,
the table was renamed to Tweetstats and only count of tweets,
sentiment for a particular query will be stored. The tokens from tweets will be stored along
with the count to generate wordcloud.


## 26.01.2019
- Modified Tweetstats table to store gender (male, female columns) count.


## 31.01.2019
- Added timeseries plot to show each day tweet count for both upa and nda.


## 02.01.2019
- Production memory leak in matplot which is used to generate word cloud. 500 error. Matplot keeps
references to all plots generated until it is explicitly closed. I forgot to close
the handle. So today raised a pr to close the matplot reference after writing the image.

- Also, optimized the code to remove exisiting wordclouds for a query whenever wordcloud for a query is updated.
