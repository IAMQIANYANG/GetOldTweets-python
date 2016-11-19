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
                
        outputFile.flush()
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


#hashtag_list = ["happy", "happiness", "happily", "happier", "happiest", "feelinghappy", 'joy', 'joyful', 'joyfully', 'joyfulness', 'joyous', 'joyously', 'joyousness', "cheerful", "cheery", "jovial", "jolly", "jocular", "gleeful", "carefree", "delighted", "smiling", "grinning", "ingoodspirits", "inagoodmood", "lighthearted", "pleased", "satisfied", "gratified", "buoyant", "feelingsunny", "blithe", "beatific", "exhilarated", "blissful"]
#hashtag_list = ['trust', 'trustable', 'trusty', 'trustability', 'trustful', 'trusting','trusties', 'trustier', 'trustiest', 'trusted', 'trustily', 'trustiness', "belief", "faith", "certainty", "assurance", "credence", "reliance"]
#hashtag_list = ['fear', 'fearsome', 'fearful', 'fearfully', 'fearfulness', "panic", "agitation", "dismay", "givemethecreeps", "givesmethecreeps", "phobia", "bugbear", "nightmare", "neurosis", "scared", "scaredstiff", "scaredtodeath", "petrified", "alarmed", "panicky", "trembling", "quaking", "cowed", "daunted", "timid", "timorous", "fainthearted", "twitchy", "trepidatious", "inacoldsweat", "abundleofnerves","spooked", "creepy", "scary"]
#hashtag_list = ['anticipated', 'anticipating', 'anticipatable', 'anticipator',"expectation", "expectance", "expectancy", "prospect", "lookingforwardto", "lookforwardto", "await", "awaiting","countingthedays", "lickingmylips", "cantwait", "can'twait", "cannotwait"]
#hashtag_list = ['anger', 'angry', 'angered', 'angrily', 'angriness', 'angrier', 'angriest', "displeasure", "crossness", "irascibility", "illtempered", "slowburn", "irate", "mad","irked", "infuriated", "inatemper","choleric","upinarms", "inhighdudgeon", "foamingatthemouth", "doingaslowburn", "inalather", "fittobetied", "seeingred","bentoutofshape", "tickedoff", "teedoff", "pissedoff","badtempered", "acrimonious","pissed"]
#hashtag_list = ['disgust', 'disgusting', 'disgusted', 'disgustedly', "sickening", "nauseating", "nauseatic", "repulsive", "turnmystomach", "gross", "pukeable", "discust", "discusting", "discusted"]
#hashtag_list = ['sad', 'sadness', 'sadden', 'sadly', 'sadder', 'saddest', 'saddeningly', "unhappiness", "depression", "despondency","wretchedness", "gloom", "gloominess","unhappy", "dejected", "depressed", "downcast", "feelingdown", "despondent", "disconsolate", "wretched", "glum", "gloomy", "dismal", "forlorn", "crestfallen", "inconsolable", "feelingblue", "downinthemouth" "downatthemouth", "downinthedumps", "tragic", "heartbreaking"]
hashtag_list = ['surprise', 'surprising', 'surprised', 'surpriser', 'surprisedly', 'astonished', 'astonish', 'astonishedly', 'astonisher','astonishment', 'astonishing', 'astonishingly', "shock", "boltfromtheblue", "bombshell", "eyeopener", "wakeupcall","shocker", "startled", "shocked", "takenaback", "stupefied", "dumbfounded", "dumbstruck", "bowledover", "flabbergasted", "astounding", "staggering", "eyeopening"]

for i in xrange(len(hashtag_list)):
    hashtag_list[i] = ("#" + hashtag_list[i])
    
hashtag_query = ' OR '.join(hashtag_list)

main(hashtag_query, "2015-09-01", "2016-03-01", 10, "surprise")
