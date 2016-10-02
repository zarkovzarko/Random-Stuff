import scrapy

class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    start_urls = (
        'http://www.imdb.com/search/name?name=morgan%20freeman',
    )
    
    def __init__(self, *args, **kwargs):
        super(ImdbSpider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('start_url')]
    
    def parse_actor_page(self, response):
        for movie in response.xpath('//div[starts-with(@class, "filmo-row") and (starts-with(@id, "actress-tt") or starts-with(@id, "actor-tt"))]'):
            moviename = movie.xpath('b/a[starts-with(@href, "/title/tt")]/text()').extract_first()
            moviehref = movie.xpath('b/a[starts-with(@href, "/title/tt")]/@href').extract_first()
            if movie.xpath('span[@class="year_column"]/text()').re('([0-9]{4,4})'):
                movieyear = movie.xpath('span[@class="year_column"]/text()').re('([0-9]{4,4})')[0]
            moviename = moviename.replace("!", "").replace("&", "and").upper()
            yield {'moviename': moviename,
                   'movieyear': movieyear,
                   'movieuri': response.urljoin(moviehref)
                   }

    
    def parse(self, response):
        actorpage =  response.urljoin(response.xpath('//a[starts-with(@href, "/name/nm")]/@href').extract_first())
        yield scrapy.Request(actorpage, callback=self.parse_actor_page, headers={'Referer': self.start_urls[0]+"/"})

        
