# tested on python 2.7
import sys
import os
import itertools
import codecs
import movieutils
import json

arguments = sys.argv[1:]

for p in itertools.permutations([arg.title() for arg in arguments]):
    dbpediaurl = 'http://dbpedia.org/page/'+'_'.join(p)
    startingdir = os.getcwd()
    os.chdir(startingdir+"/movies/movies")
    os.popen("echo zarko > dbpedia.json")
    os.popen("rm dbpedia.json")
    os.popen("scrapy crawl dbpedia -o dbpedia.json -a start_url=" + dbpediaurl)
    os.popen("cp dbpedia.json ../../")
    os.chdir(startingdir)

    with open("dbpedia.json", "r") as f:
        if f.read().strip() != "[":
            break


for p in itertools.permutations([arg.lower() for arg in arguments]):   
    imdburl = 'http://www.imdb.com/search/name?name='+'%20'.join(p) 
    print(imdburl)
    startingdir = os.getcwd()   
    os.chdir(startingdir+"/movies/movies")
    os.popen("echo zarko > imdb.json")
    os.popen("rm imdb.json")
    os.popen("scrapy crawl imdb -o imdb.json -a start_url=" + imdburl)
    os.popen("cp imdb.json ../../")
    os.chdir(startingdir)

    with open("imdb.json", "r") as f:
        if f.read().strip() != "[":
            break
    

res = movieutils.mixer(masterjson="dbpedia.json", slavejson="imdb.json")

with open("result.json", "w") as fw:
    json.dump(res, fw, indent=4)
        