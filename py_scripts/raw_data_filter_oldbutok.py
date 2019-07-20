# import libraries
import json
import glob, os
import fileinput
import re
from langdetect import detect

#read files
#data = open("data/timelines/test1/63299591","r")
#data = open("data/timelines/test1/3578166252","r")
#data = "data/timelines/test1/3578166252"
data = "data/timelines/test1/133684052"

#ToDo
#iterate through all files
#stop writing file at a certain size, create new and continue writing there

def entry_check(tweet,collection_data):
    # tweet is a variable for the full_text in the raw_file
    # collection_data is the file with the manipulated full_text for collection
    rawfile = open(collection_data,'r')
    for lines in rawfile:
        print(lines)
        if tweet+"\n" == lines:
            return True

def raw_data_collect(rawdata,collection):
    with open(rawdata,"r") as data:
        for lines in data:

            #ToDo
            #Remove all links, @usernames

            # remove empty spaces and unwanted line breaks
            json_lines = json.loads(lines)
            tweet = json_lines["full_text"]
            tweet = tweet.replace("\n","")
            tweet = tweet.replace("\r","")
            tweet = re.sub('@[^\s]+','',tweet)       # removes all the usernames
            tweet = re.sub(r"http\S+", "", tweet)    # removes all the links

            # check whether tweet is japanese
            if detect(tweet) != "ja":
                lang = detect(tweet)
                print(lang)
                continue

            # exclude sentences shorter than 5 characters
            elif len(tweet) < 5:
                print("deleted: ",tweet)
                continue
            else:
                f = open(collection,"a")
                if entry_check(tweet,collection) == True:
                    continue
                f.write(tweet+"\n")
                f.close()

raw_data_collect(data,"raw")
