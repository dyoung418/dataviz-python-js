# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class NobelWinnersPipeline(object):
    def process_item(self, item, spider):
        return item

class DropNonPersons(object):
    def process_item(self, item, spider):
        if not item['gender']:
            raise DropItem("No gender for {}".format(item['name']))
        return item

class NobelImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        '''Chains a request to go get the media'''
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        '''Called when the media request returns a result and is
        process by the pipeline'''
        # the result is a list of tuples of [(True, Image), (False, Image), ...] format
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            # these image_paths will be relative to IMAGES_STORE defined in settings.py
            item['bio_image'] = image_paths[0]
        return item
