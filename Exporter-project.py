# -*- coding: utf-8 -*-

import sys, getopt, got, datetime, codecs, langid
from datetime import datetime, timedelta, date

total_count = 0

def main(keyword, start, end, max_per_day, filename):
    
    tweetCriteria = got.manager.TweetCriteria()
    tweetCriteria.querySearch = keyword
    tweetCriteria.maxTweets = int(max_per_day)
    tweetCriteria.topTweets = False
    
    exportedFileName = "output_" + filename + ".csv"

    outputFile = codecs.open(exportedFileName, "w+", "utf-8")

    outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
    
    global total_count
    total_count = 0
    print 'Searching...\n'
    
    def receiveBuffer(tweets):
        global total_count
        counter = 0
        for t in tweets:
            lang = langid.classify(t.rawtext)[0]
            if (lang == 'en'):
                counter += 1
                total_count += 1
                outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (
                    t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions,
                    t.hashtags, t.id, t.permalink)))
                
        outputFile.flush();
        print ' - ' + str(counter) + ' tweets saved on file.\n'
        
    def daterange(start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)
            
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    
    for single_date in daterange(start_date, end_date):
        str_date = single_date.strftime("%Y-%m-%d")
        tweetCriteria.since = str_date
        tweetCriteria.until = (single_date + timedelta(days=1)).strftime("%Y-%m-%d")
        print 'Crawling tweets posted on ' + str_date + '...'
        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
    
    outputFile.close()
    print 'Done. Output file generated. A total of ' + str(total_count) + ' tweets have been crawled.'

main("#anger OR #happy OR #surprise", "2016-06-20", "2016-06-25", 20, "happy")

