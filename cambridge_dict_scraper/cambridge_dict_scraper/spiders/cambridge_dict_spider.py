import scrapy
from cambridge_dict_scraper.items import CambridgeDictScraperItem
import random

class CambridgeDictSpider(scrapy.Spider):
    name = "cambridge_dict_spider"
    handle_httpstatus_list = [302]
    allowed_domains = ['dictionary.cambridge.org']
    # user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    #             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    #             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    #             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    #             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    #             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    #             'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15']

    def __init__(self, word=None, *args, **kwargs):
        super(CambridgeDictSpider, self).__init__(word, *args, **kwargs)
        self.word=word
        self.start_urls = [f'https://dictionary.cambridge.org/dictionary/english/{self.word}']
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, headers={"Accept-Language": "en-US,en;q=0.5"})
            


    def parse(self, response):
        
        if response.status == 302:
            location = response.headers['Location'].decode('utf-8')
            print('////////////////////', location)
            yield scrapy.Request(location, callback=self.parse)
        else:
            for block in response.css('div.entry'): 
                for definition in block.css('div.pr.dsense'): 

                    word_item = {
                        'word': block.css('span.hw::text').get(),
                        'part_of_speech': definition.css('span.pos.dsense_pos::text').get(),
                        'synonym': definition.css('span.guideword span::text').get(),
                        'definition': definition.css('div.def.ddef_d.db').xpath('string()').get(),
                        'examples': definition.css('span.eg.deg').xpath('string()').getall()
                    }
                    yield CambridgeDictScraperItem(word_item)
            for block in response.css('div.idiom-block'):
                word_item = {
                    'word': block.css('b').xpath('string()').get(),
                    'part_of_speech': 'idiom',
                    'definition': block.css('div.def.ddef_d.db').xpath('string()').get(),
                    'examples': block.css('span.eg.deg').xpath('string()').getall()
                }
                yield CambridgeDictScraperItem(word_item)