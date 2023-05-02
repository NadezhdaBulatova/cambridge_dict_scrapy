import scrapy
from lxml import etree

class MWBDictSpider(scrapy.Spider):
    name = "mwb_dict_spider"
    handle_httpstatus_list = [302]
    allowed_domains = ['mijnwoordenboek.nl']

    def __init__(self, word=None, *args, **kwargs):
        super(MWBDictSpider, self).__init__(word, *args, **kwargs)
        self.word=word
        self.start_urls = [f'https://www.mijnwoordenboek.nl/vertaal/NL/EN/{self.word}']
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, headers={"Accept-Language": "en-US,en;q=0.5"})
            
    def parse(self, response):
        
        if response.status == 302:
            location = response.headers['Location'].decode('utf-8')
            yield scrapy.Request(location, callback=self.parse)
        
        else: 
            if response.css('h2.inline'):
                word_item={
                    'word': None,
                    'part_of_speech': None,
                    'en_definition': None,
                    'nl_definition': None,
                    'examples': [],
                    'idioms': []
                }
                word_item['word'] = response.css('h2.inline::text').get()
                word_item['part_of_speech'] = response.xpath('//h2[@class="inline"]/following-sibling::text()').get()
                for ind, definition in enumerate(response.xpath('//table[@cellspacing="0"]')):
                    if ind > 0: 
                        word_item['examples'] = []
                        word_item['idioms'] = []
                        word_item['word'] = response.css('h2.inline::text').get()
                        word_item['part_of_speech'] = response.xpath('//h2[@class="inline"]/following-sibling::text()').get()
                        word_item['en_definition'] = definition.root.getprevious().xpath("string()")
                        word_item['nl_definition'] = definition.root.getprevious().getprevious().xpath("string()")
                        for example in definition.xpath('.//td[@colspan="2"]'):
                            if example.xpath('./*[1]').xpath("name()").get() == 'i':
                                for item in example.xpath('.//font[@style="color:navy"]'):
                                    word_item['examples'].append({'en': item.xpath('string()').get(), 'nl': item.root.getprevious().xpath('string()')})
                            if example.xpath('./*[1]').xpath("name()").get() == 'a':
                                for item in example.xpath('.//div[contains(@id, "xi")]'):
                                    idiom = {
                                        'expression': item.root.getprevious().xpath('string()'),
                                        'en_definition': item.xpath('.//font[@style="color:navy"]').xpath('string()').get(),
                                        'nl_definition': item.xpath('.//font[@style="color:darkgreen"]').xpath('string()').get(),
                                    }
                                    if len(item.xpath('.//font[@style="color:#444"]')) > 0:
                                        idiom['en_example']=item.xpath('.//font[@style="color:navy"]')[1].xpath('string()').get()
                                        idiom['nl_example']=item.xpath('.//font[@style="color:navy"]')[1].xpath('string()').get()
                                    word_item['idioms'].append(idiom)
                        yield word_item