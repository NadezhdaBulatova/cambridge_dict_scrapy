from itemadapter import ItemAdapter
import psycopg2
import os

class CambridgeDictScraperPipeline:
    def open_spider(self, spider):
        hostname=os.getenv('DB_HOST')
        username=os.getenv('DB_USER')
        password=os.getenv('DB_PASSWORD')
        database=os.getenv('DB_NAME')
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password, dbname=database
        )
        self.cur = self.connection.cursor()
        #create table if none exists 

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        adapter=ItemAdapter(item)
        try: 
            if (adapter.get('part_of_speech') == 'idiom'):
                spider.word = spider.word.replace('+', ' ')
            self.cur.execute(f"insert into language_train_en_dict(word) values('{spider.word}')")
            self.connection.commit()
        except:
            self.connection.rollback()
            raise
        return item
