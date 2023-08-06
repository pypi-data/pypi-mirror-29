# -*- coding: utf-8 -*-

import requests
from cryptotik.common import (headers, ExchangeWrapper,
                              NormalizedExchangeWrapper)
from cryptotik.exceptions import (InvalidBaseCurrencyError,
                                  InvalidDelimiterError,
                                  APIError,
                                  OutdatedBaseCurrenciesError)
from cryptotik.common import is_sale
import time
import hmac
import hashlib
from datetime import datetime
from decimal import Decimal


class BitMEX:

    name = 'bitmex'
    api_url = 'https://www.bitmex.com/api/v1'
    delimiter = ""
    headers = headers
    taker_fee, maker_fee = 0, 0
    base_currencies = ['xbt']
    quote_order = 1

    def __init__(self, apikey=None, timeout=None, proxy=None):

        if apikey:
            self._apikey = apikey

        if proxy:
            assert proxy.startswith('https'), {'Error': 'Only https proxies supported.'}
        self.proxy = {'https': proxy}

        if not timeout:
            self.timeout = (8, 15)
        else:
            self.timeout = timeout

        self.api_session = requests.Session()

    def _verify_reponse(response):
        raise NotImplementedError

    def api(self, command, params={}):
        """call remote API"""

        try:
            result = self.api_session.get(self.api_url + command, params=params,
                                          headers=self.headers, timeout=self.timeout,
                                          proxies=self.proxy)

            result.raise_for_status()

        except requests.exceptions.HTTPError as e:
            print(e)

        #self._verify_reponse(result)
        return result.json()

    def get_markets(self):
        '''get avaliable markets'''

        m = self.api('/instrument/active')

        return [i['symbol'] for i in m if not i['state'] == "Unlisted"]

    def get_market_ticker(self, market):
        '''get market ticker'''

        t = self.api('/instrument', params={'symbol': market})[0]

        return {'volume': t['volume24h'],
                'vwap': t['vwap'],
                'bidPrice': t['bidPrice'],
                'askPrice': t['askPrice'],
                'lastPrice': t['lastPrice']
                }

    '''

    def generate_signature(self, secret, verb, url, nonce, data):
        """Generate a request signature compatible with BitMEX."""
        # Parse the url so we can remove the base and extract just the path.
        parsedURL = urllib.parse.urlparse(url)
        path = parsedURL.path
        if parsedURL.query:
            path = path + '?' + parsedURL.query

        message = bytes(verb + path + str(nonce) + data, 'utf-8')
        # print("Computing HMAC: %s" % message)

        signature = hmac.new(bytes(secret, 'utf-8'), message, digestmod=hashlib.sha256).hexdigest()
        
        return signature

    def apply(self, r):
        # 5s grace period in case of clock skew
        expires = int(round(time.time()) + 5)
        r.headers['api-expires'] = str(expires)
        r.headers['api-key'] = self.api_key
        prepared = r.prepare()
        body = prepared.body or ''
        url = prepared.path_url
        # print(json.dumps(r.data,  separators=(',',':')))
        r.headers['api-signature'] = self.generate_signature(self.api_secret, r.method, url, expires, body)
        return r

'''