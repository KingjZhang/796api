#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import urllib
import requests
import hmac
import hashlib
import base64

class API796(object):
    def __init__(self, appid, key, secret):
        self.appid = appid
        self.key = key
        self.secret = secret
        self.access_token = None

    def get_sig(self):
        msg = 'apikey=%s&appid=%s&secretkey=%s&timestamp=%d' % ( \
                urllib.parse.quote_plus(self.key), self.appid, urllib.parse.quote_plus(self.secret), int(time.time()))
        return base64.b64encode(bytes(hmac.new(bytes(self.secret,'utf-8'), msg.encode('utf-8'), hashlib.sha1).hexdigest().lower(),"utf-8"))

    def update_token(self):
        params = {'appid': self.appid, 'apikey': self.key, 'timestamp': int(time.time()), 'sig': self.get_sig()}
        r =requests.get('https://796.com/oauth/token', params=params)
        result = r.json()
        assert(int(result['errno']) == 0)
        self.access_token = urllib.parse.unquote(result['data']['access_token'])
        self.access_token_update_time = time.time()
        return self.access_token

    def get_token(self):
        if self.access_token:
            if (time.time() - self.access_token_update_time) < 3600:
                return self.access_token
            else:
                self.delete_token()
        return self.update_token()

    def call(self, api_type, method, params={}):
        params.update({'access_token': self.get_token()})
        r = requests.get('https://796.com/v1/%s/%s' % (api_type, method), params=params)
        return r.json()

    def get_info(self):
        return self.call('user', 'get_info')

    def get_balance(self):
        return self.call('user', 'get_balance')

    def delete_token(self):
        self.call('user', 'delete_token')
        self.access_token = None
        self.access_token_update_time = 0

    def btc_orders(self):
        return self.call('weeklyfutures', 'orders')

    def btc_records(self):
        return self.call('weeklyfutures', 'records')

    def btc_position(self):
        return self.call('weeklyfutures', 'position')

    def btc_open_buy(self, margin, num, price):
        return self.call('weeklyfutures', 'open_buy', {'times': margin, 'buy_num': num, 'buy_price': price})
    
    def btc_close_buy(self, margin, num, price):
        return self.call('weeklyfutures', 'close_buy', {'times': margin, 'buy_num': num, 'buy_price': price})

    def btc_open_sell(self, margin, num, price):
        return self.call('weeklyfutures', 'open_sell', {'times': margin, 'buy_num': num, 'buy_price': price})

    def btc_close_sell(self, margin, num, price):
        return self.call('weeklyfutures', 'close_sell', {'times': margin, 'buy_num': num, 'buy_price': price})

    def btc_cancel_order(self, bs, no):
        return self.call('weeklyfutures', 'cancel_order', {'bs': bs, 'no': no})

    def btc_cancel_all(self, bs):
        return self.call('weeklyfutures', 'cancel_all', {'bs': bs})


    def ltc_orders(self):
        return self.call('ltcfutures', 'orders')

    def ltc_records(self):
        return self.call('ltcfutures', 'records')

    def ltc_position(self):
        return self.call('ltcfutures', 'position')

    def ltc_open_buy(self, margin, num, price):
        return self.call('ltcfutures', 'open_buy', {'times': margin, 'buy_num': num, 'buy_price': price})
    
    def ltc_close_buy(self, margin, num, price):
        return self.call('ltcfutures', 'close_buy', {'times': margin, 'buy_num': num, 'buy_price': price})

    def ltc_open_sell(self, margin, num, price):
        return self.call('ltcfutures', 'open_sell', {'times': margin, 'buy_num': num, 'buy_price': price})

    def ltc_close_sell(self, margin, num, price):
        return self.call('ltcfutures', 'close_sell', {'times': margin, 'buy_num': num, 'buy_price': price})

    def ltc_cancel_order(self, bs, no):
        return self.call('ltcfutures', 'cancel_order', {'bs': bs, 'no': no})

    def ltc_cancel_all(self, bs):
        return self.call('ltcfutures', 'cancel_all', {'bs': bs})
