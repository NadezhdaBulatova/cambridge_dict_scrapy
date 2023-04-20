import scrapy

class CambridgeDictSpider(scrapy.Spider):
    name = "cambridge_dict_spider"
    handle_httpstatus_list = [302]

    def __init__(self, word=None, *args, **kwargs):
        super(CambridgeDictSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://dictionary.cambridge.org/dictionary/english/{self.word}']
        self.word=word

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept-Language": "en-US,en;q=0.5"})

    def parse(self, response):
        if response.status == 302:
            location = response.headers['Location'].decode('utf-8')
            yield scrapy.Request(location, callback=self.parse)
        else:
            results=[]
            for block in response.css('div.entry'): 
                for definition in block.css('div.pr.dsense'):
                    result = {
                        'word': block.css('span.hw::text').get(),
                        'part_of_speech': definition.css('span.pos.dsense_pos::text').get(),
                        'synonym': definition.css('span.guideword span::text').get(),
                        'definition': definition.css('div.def.ddef_d.db').xpath('string()').get(),
                        'examples': definition.css('span.eg.deg').xpath('string()').getall()
                    }
                    results.append(result)
            for block in response.css('div.idiom-block'):
                result = {
                     'word': block.css('b').xpath('string()').get(),
                     'part_of_speech': 'idiom',
                     'definition': block.css('div.def.ddef_d.db').xpath('string()').get(),
                     'examples': block.css('span.eg.deg').xpath('string()').getall()
                }
                results.append(result)
            return results