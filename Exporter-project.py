# -*- coding: utf-8 -*-

import sys, getopt, got, datetime, codecs


def main(keyword, start, end, max, filename):

    tweetCriteria = got.manager.TweetCriteria()

    tweetCriteria.since = start
    tweetCriteria.until = end
    tweetCriteria.querySearch = keyword
    tweetCriteria.maxTweets = int(max)
    tweetCriteria.topTweets = False

    exportedFileName = "output_" + filename + ".csv"

    outputFile = codecs.open(exportedFileName, "w+", "utf-8")

    outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

    print 'Searching...\n'

    def receiveBuffer(tweets):
        for t in tweets:
            outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (
                t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions,
                t.hashtags, t.id, t.permalink)))
        outputFile.flush()
        print 'More %d saved on file...\n' % len(tweets)

    got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    print 'Done. Output file generated.'


main("#anger OR #happy OR #surprise", "2015-09-10", "2015-09-15", 10, "happy")



