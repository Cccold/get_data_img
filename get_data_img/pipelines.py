'''
@Author: MengHan
@Go big or Go home
@Date: 2020-09-29 15:48:11
@LastEditTime: 2020-09-29 15:53:26
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql as pq

class GetDataImgPipeline:
    def __init__(self):
        # self.conn = pq.connect(
        #     host='39.106.48.216',
        #     port=3306,
        #     user='root',
        #     passwd='MyNewPass4!',
        #     db='test',
        #     charset='utf8'
        # )
        self.conn = pq.connect(
            host='10.80.81.254',
            port=3306,
            user='baimeng_media',
            passwd='baimeng_media',
            db='baimeng_media',
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):

        sql = 'INSERT INTO media_covers(mid,day,url,image_url,plate,uuid) VALUES ("{mid}","{day}","{url}","{image_url}","{plate}","{uuid}")'.format(
            **item)
        print(sql)

        self.cursor.execute(sql)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
