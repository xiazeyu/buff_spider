import scrapy
import json
import time
from pathlib import Path

watch_list = json.loads(open('watch_list.json').read())


class SellOrderSpider(scrapy.Spider):
    name = 'buy_order'
    allowed_domains = ['buff.163.com']

    def start_requests(self):
        for goods_id in watch_list:
            yield scrapy.Request(url=f'https://buff.163.com/api/market/goods/buy_order?game=csgo&goods_id={goods_id}', callback=self.parse)

    def parse(self, response):
        body = json.loads(response.body)
        goods_id = response.url.split('goods_id=')[-1]
        i_total_count = body['data']['total_count']
        items = body['data']['items']
        highest_price = items[0]['price']

        current_timestamp = int(time.time())
        current_date = time.strftime("%Y%m%d", time.localtime())
        Path(
            f'saved/pay_order/{current_date}').mkdir(parents=True, exist_ok=True)
        filename = f'saved/pay_order/{current_date}/{goods_id}_{current_timestamp}.json'

        with open(filename, 'wb') as f:
            f.write(json.dumps(body, ensure_ascii=False, indent=2).encode('utf-8'))
        self.log(f'Saved file {filename}.')
        yield {
            'goods_id': goods_id,
            'highest_price': highest_price,
            'total_count': i_total_count,
        }
