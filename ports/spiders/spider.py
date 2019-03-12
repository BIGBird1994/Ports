from scrapy import Request,Spider,FormRequest
from ports.items import PortsItem
from re import findall
from json import loads


class spider(Spider):
      name = 'ports'
      start_urls = [
          'http://www.ports-intl.com/zh/product/plist/cid/73',
          'http://www.ports-intl.com/zh/product/plist/cid/209',
          'http://www.ports-intl.com/zh/product/plist/cid/162',
          'http://www.ports-intl.com/zh/product/plist/cid/74' ,
          'http://www.ports-intl.com/zh/product/plist/cid/225',
          'http://www.ports-intl.com/zh/product/plist/cid/236',
          'http://www.ports-intl.com/zh/product/plist/cid/447',
          'http://www.ports-intl.com/zh/product/plist/cid/448'

      ]
      api = 'http://www.ports-intl.com/api/product/getProduct'
      detail_api = 'http://www.ports-intl.com/api/product/getProductDetail'

      def start_requests(self):
          for url in self.start_urls:
              url_path = findall(r'(/zh/product/plist/cid/\d+)',url)[0]
              cid = findall(r'(\d+)',url)[0]
              page = 1
              meta = {'cid':cid,'url_path':url_path,'page':page}
              yield FormRequest(
                  url=self.api,
                  formdata={
                      'cid': cid,
                      'page': '1',
                      'url_path': url_path
                  },meta=meta,callback=self.parse_list,dont_filter=True
              )
              
      def parse_list(self, response):
          resp = loads(response.text)
          if len(resp['data']['plist']) > 0:
              for data in resp['data']['plist']:
                  pid = data['pid']
                  print('<===== fetch detail =====>')
                  yield FormRequest(
                      url=self.detail_api,
                      formdata={
                          'pid': str(pid),
                      },callback=self.parse_detail
                  )
              meta = response.meta
              page = meta['page'] + 1
              url_path = meta['url_path']
              cid = meta['cid']
              print('<===== fetch next =====>')
              yield FormRequest(
                  url=self.api,
                  formdata={
                      'cid': cid,
                      'page': str(page),
                      'url_path': url_path
                  },meta={'cid':cid,'url_path':url_path,'page':page}, callback=self.parse_list
              )
          else:
              print(resp)
              
              
      def parse_detail(self, response):
          resp = loads(response.text)
          item = PortsItem()
          item['product_detail'] = resp['data']
          yield item
          
from scrapy import cmdline
cmdline.execute('scrapy crawl ports'.split())