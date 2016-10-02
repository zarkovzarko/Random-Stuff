# -*- coding: utf-8 -*-
import scrapy
#from scrapy_splash import SplashRequest
import os
import re


class DbpediaSpider(scrapy.Spider):
    name = "dbpedia"
    allowed_domains = ["dbpedia.org"]
    start_urls = (
        'http://dbpedia.org/page/Catherine_Zeta_Jones', #Tom_Hanks Morgan_Freeman Catherine_Zeta_Jones
    )
    yearpattern = re.compile("\(.*([0-9]{4,4}).*\)")
    
    def __init__(self, *args, **kwargs):
        super(DbpediaSpider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('start_url')] 

    def start_requests(self):
        for url in self.start_urls:
            os.system("curl 'http://localhost:8050/render.html?url="+url+"&timeout=10&wait=0.5' > temp.html")
#        for url in self.start_urls:
#            yield SplashRequest(url=url, callback=self.parse,
#                endpoint='render.html',
#                args={'wait': 5},
#            )
            yield scrapy.Request("file:///home/zarko/Desktop/random_staff/movies/movies/temp.html", callback=self.parse)
            
    def parse_movie_page(self, response):
        moviename = response.xpath('//span[@property="dbp:name"]/text()').extract_first()
        if not moviename:
            moviename = response.xpath('//span[@property="foaf:name"]/text()').extract_first()
        movieyear = response.xpath('//span[contains(@property, ":release")]/text()').extract_first()
        
        if movieyear:
            if re.search("([\d]{4,4})", movieyear):
                movieyear = re.search("([\d]{4,4})", movieyear).group(1)
        else:
            movieyear = response.xpath('//title/text()').extract_first()
            if self.yearpattern.search(movieyear):
                movieyear = self.yearpattern.search(movieyear).group(1)
            else:
                movieyear = "NONE"
                
        moviename = moviename.replace("!", "").replace("&", "and").upper()
        yield {'moviename':moviename, 
               'movieyear':movieyear,
               'movieuri':response.url}

    def parse(self, response):
        for movie in response.xpath('//a[@rev="dbo:starring"]'):
            linkstomoviepage = movie.xpath("@href").extract()
            print(linkstomoviepage)
            for link in linkstomoviepage:
                yield scrapy.Request(link, callback=self.parse_movie_page, headers={'Referer': self.start_urls[0]+"/"})
            
