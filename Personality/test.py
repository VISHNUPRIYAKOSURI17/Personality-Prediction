import json
import os
import re
from scipy.stats import pearsonr


mrc = []
liwc = []
emotion = []
global openness
global agreeable
global conscientious
global extroversion
global neuroticism
global open_count
global agree_count
global ext_count
global neu_count
global cons_count

with open("LIWC.dic", "r") as file:
    for line in file:
        line = line.strip('\n')
        line = line.strip()
        liwc.append(line.lower())
    print(liwc)

        
with open("MRC.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        line = line.strip()
        mrc.append(line.lower())
    print(mrc)

with open("emotions.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        line = line.strip()
        emotion.append(line.lower())
    print(emotion)    

def opennessFunction(words):
    count = 0.0
    for i in range(len(liwc)):
        if words.find(liwc[i]) != -1:
            count = count + 1
    if count > 0:
        count = count/float(len(liwc))
    return count

def agreeableFunction(words):
    count = 0.0
    for i in range(len(mrc)):
        if words.find(mrc[i]) != -1:
            count = count + 1
    if count > 0:
        count = count/float(len(mrc))            
    return count

def neuroticismFunction(words):
    count = 0.0
    for i in range(len(emotion)):
        if words.find(emotion[i]) != -1:
            count = count + 1
    if count > 0:
        count = count/float(len(emotion))            
    return count

def pearson(feature,retweet,followers,mention,hashtag,following):
    pearson_value = 0;
    x = [feature,retweet,followers]
    y = [mention,hashtag,following]
    pearson_value, _ = pearsonr(x, y)
    return pearson_value
    
open_count = 0
agree_count = 0
ext_count = 0
neu_count = 0
cons_count = 0
for root, dirs, files in os.walk('tweets'):
    for fdata in files:
        with open(root+"/"+fdata, "r") as file:
            data = json.load(file)
            textdata = data['text'].strip('\n')
            textdata = textdata.replace("\n"," ")
            textdata = re.sub('\W+',' ', textdata)
            retweet = data['retweet_count']
            followers = data['user']['followers_count']
            density = data['user']['listed_count']
            following = data['user']['friends_count']
            replies = data['user']['favourites_count']
            hashtag = data['user']['statuses_count']
            username = data['user']['screen_name']
            words = textdata.split(" ")
            openness = opennessFunction(textdata.lower())#use open swear words in tweets
            agreeable = agreeableFunction(textdata.lower()) #use agreeable words in tweets
            neuroticism = neuroticismFunction(textdata.lower()) #sentiment
            extroversion = following/hashtag    #friendly
            conscientious = followers/hashtag  #hardwork and reliable
            openness = pearson(openness,retweet,hashtag,followers,hashtag,following)
            agreeable = pearson(agreeable,retweet,following,followers,hashtag,following)
            neuroticism = pearson(neuroticism,retweet,density,followers,hashtag,following)
            extroversion = pearson(extroversion,retweet,replies,followers,hashtag,following)
            conscientious = pearson(conscientious,retweet,retweet,followers,hashtag,following)
            if openness > 0.1:
                open_count = open_count + 1
            if agreeable > 0.1:
                agree_count = agree_count + 1
            if neuroticism > 0.1:
                neu_count = neu_count + 1
            if extroversion > 0.1:
                ext_count = ext_count + 1
            if conscientious > 0.1:
                cons_count = cons_count + 1    
            #print('Pearsons correlation: %.3f' % corr) 
            
            print(username+" "+str(openness)+" "+str(agreeable)+" "+str(neuroticism)+" "+str(extroversion)+" "+str(conscientious))
            print(str(open_count)+" "+str(agree_count)+" "+str(neu_count)+" "+str(ext_count)+" "+str(cons_count))

         
