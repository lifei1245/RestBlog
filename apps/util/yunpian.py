# coding=utf-8
# @Time : 2018/1/5 16:44
# @Author : 李飞
import requests
from RestBlog.settings import SMS_APIKEY


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_single_sms(self, code, mobile):
        postdata = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '%s' % code,
        }
        result_dict = requests.post(url=self.url, data=postdata)
        return result_dict


if __name__ == '__main__':
    yunpian = YunPian(SMS_APIKEY)
    result = yunpian.send_single_sms('1234', 1838565456)
    print(result)
