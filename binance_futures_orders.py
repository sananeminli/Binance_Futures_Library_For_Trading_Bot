
import hashlib
import hmac
import json
import requests



class client:
    
    
    def __init__(self,secretKey,apiKey):
        self.apiKey  = apiKey
        self.secretKey = secretKey



    def hasing(self,querystring):
        return hmac.new(self.secretKey.encode('utf-8'), querystring.encode('utf-8'), hashlib.sha256).hexdigest()

    def market_order(self, symbol, miktar, positionSide):
        if(positionSide=='LONG'):
            alim_satim='BUY'
        else: alim_satim='SELL'
        url = "https://fapi.binance.com/fapi/v1/order"

        server_time_url = 'https://api1.binance.com/api/v3/time'
        get_server_time = requests.get(server_time_url)
        server_time = json.loads(get_server_time.content)
        ts = server_time["serverTime"]

        params = 'symbol=' + symbol +'&type=MARKET&quantity=' + str(miktar) + '&side=' + alim_satim+ '&positionSide='  + positionSide+'&timestamp=' + str(ts)
        signuture = self.hasing(params)
        order = {"symbol": symbol, "type": "MARKET", "quantity": str(miktar), "side": alim_satim,"positionSide": positionSide,"timestamp": ts,
                 'signature': signuture}
        headers = {"X-MBX-APIKEY": self.apiKey}

        reponse = requests.post(url, headers=headers, params=order)
        return reponse.content

    def cancel_all_orders(self,symbol):

        url = "https://fapi.binance.com/fapi/v1/allOpenOrders"
        server_time_url = 'https://api1.binance.com/api/v3/time'
        get_server_time = requests.get(server_time_url)
        server_time = json.loads(get_server_time.content)
        ts = server_time["serverTime"]

        params = 'symbol=' + symbol +  '&timestamp=' + str(ts)
        signuture = self.hasing(params)
        order = {"symbol": symbol,  "timestamp": ts,'signature': signuture}
        headers = {"X-MBX-APIKEY": self.apiKey}

        response = requests.delete(url, headers=headers, params=order)
        print(response.content)

  

    def stop_loss(self, symbol, closed_position ,stop):
        positionSide = closed_position
        if (positionSide == 'LONG'):
            side = 'SELL'
        else:
            side = 'BUY'

        url = "https://fapi.binance.com/fapi/v1/order"
        server_time_url = 'https://api1.binance.com/api/v3/time'
        get_server_time = requests.get(server_time_url)
        server_time = json.loads(get_server_time.content)
        ts = server_time["serverTime"]
        dxc_stop = float(stop)
        dec_stop =round(dxc_stop,2)
        params = 'symbol=' + symbol + '&type=STOP_MARKET'+'&positionSide='+positionSide + '&side=' + side + '&stopPrice=' + str(dec_stop) +'&closePosition=true'+ '&timestamp=' + str(ts)
        signuture = self.hasing(params)
        order = {"symbol": symbol,
                 "type": "STOP_MARKET",
                 "positionSide": positionSide,
                 "side": side,
                 "stopPrice": dec_stop,
                 "closePosition":"true",
                 "timestamp": ts,
                 'signature': signuture
                 }
        headers = {"X-MBX-APIKEY": self.apiKey}

        post_tst = requests.post(url, headers=headers, params=order)

        print(post_tst.content)

    def take_prof_market(self, symbol,closed_position ,triger_price):
        positionSide=closed_position
        if (positionSide == 'LONG'):
            side = 'SELL'
        else:
            side = 'BUY'

        url = "https://fapi.binance.com/fapi/v1/order"
        server_time_url = 'https://api1.binance.com/api/v3/time'
        get_server_time = requests.get(server_time_url)
        server_time = json.loads(get_server_time.content)
        ts = server_time["serverTime"]
        dxc_stop = float(triger_price)
        dec_stop = round(dxc_stop,2)
        params = 'symbol=' + symbol + '&type=TAKE_PROFIT_MARKET' + '&positionSide=' + positionSide + '&side=' + side + '&stopPrice=' + str(
            dec_stop) + '&closePosition=true' + '&timestamp=' + str(ts)
        signuture = self.hasing(params)
        order = {"symbol": symbol,
                 "type": "TAKE_PROFIT_MARKET",
                 "positionSide": positionSide,
                 "side": side,
                 "stopPrice": dec_stop,
                 "closePosition": "true",
                 "timestamp": ts,
                 'signature': signuture
                 }
        headers = {"X-MBX-APIKEY": self.apiKey}

        post_tst = requests.post(url, headers=headers, params=order)

        print(post_tst.content)
        print(post_tst.url)

    def stop_market(self, symbol, closed_position ,stop,quantity):
        positionSide = closed_position
        if (positionSide == 'LONG'):
            side = 'BUY'
        else:
            side = 'SELL'

        url = "https://fapi.binance.com/fapi/v1/order"
        server_time_url = 'https://api1.binance.com/api/v3/time'
        get_server_time = requests.get(server_time_url)
        server_time = json.loads(get_server_time.content)
        ts = server_time["serverTime"]
        dxc_stop = float(stop)
        dec_stop =round(dxc_stop,2)
        params = 'symbol=' + symbol + '&type=STOP_MARKET'+'&positionSide='+positionSide +'&quantity='+str(quantity)+ '&side=' + side + '&stopPrice=' + str(dec_stop) +'&closePosition=false'+ '&timestamp=' + str(ts)
        signuture = self.hasing(params)
        order = {"symbol": symbol,
                 "type": "STOP_MARKET",
                 "positionSide": positionSide,
                 "quantity":quantity,
                 "side": side,
                 "stopPrice": dec_stop,
                 "closePosition":"false",
                 "timestamp": ts,
                 'signature': signuture
                 }
        headers = {"X-MBX-APIKEY": self.apiKey}

        post_tst = requests.post(url, headers=headers, params=order)

        print(post_tst.content)

    def trailing_stop(self,symbol,quantity,closed_position,actication_price,callBackRate):
        positionSide= closed_position
        if (positionSide == 'LONG'):
            side = 'SELL'
        else:
            side = 'BUY'
        decprc = round(float(actication_price),3)
        callbackrate = callBackRate
        url = "https://fapi.binance.com/fapi/v1/order"
        server_time_url = 'https://api1.binance.com/api/v3/time'
        get_server_time = requests.get(server_time_url)
        server_time = json.loads(get_server_time.content)
        ts = server_time["serverTime"]
        params = 'symbol=' + symbol + '&quantity='+str(quantity)+'&type=TRAILING_STOP_MARKET'+'&positionSide='+positionSide+'&activationPrice='+str(decprc)+'&side=' + side +'&callbackRate='+ str(callbackrate)+ '&timestamp=' + str(ts)
        signuture = self.hasing(params)
        order = {"symbol": symbol,
                 "quantity":quantity,
                 "type": "TRAILING_STOP_MARKET",
                 "positionSide":positionSide,
                 "activationPrice":decprc,
                 "side": side,
                 "callbackRate": callbackrate,
                 "timestamp": ts,
                 'signature': signuture}
        headers = {"X-MBX-APIKEY": self.apiKey}

        post_tst = requests.post(url, headers=headers, params=order)
        print(post_tst.content)

    def set_levarage(self,symbol,leverage):
        url = "https://fapi.binance.com/fapi/v1/leverage"
        server_time_url = 'https://api1.binance.com/api/v3/time'
        get_server_time = requests.get(server_time_url)
        server_time = json.loads(get_server_time.content)
        ts = server_time["serverTime"]
        query = 'symbol=' + str(symbol) + '&leverage=' + str(leverage)+'&timestamp=' + str(ts)
        signature  = self.hasing(query)
        params = {"symbol": symbol, "leverage":leverage, "timestamp" :ts,"signature" :signature}
        headers = {"X-MBX-APIKEY": self.apiKey}
        post = requests.post(url,headers = headers,params = params)
        print(post.text)

    def get_listen_key(self):
        url = "https://fapi.binance.com/fapi/v1/listenKey"
        headers = {"X-MBX-APIKEY": 'EQ54zk3meUzuYrawse6VQ1Z0CpgjPp5t18sWoX9yEBIh2SxpmkqSaLB6qtXyWSHr'}
        response = requests.post(url=url, headers=headers)
        content = json.loads(response.content)
        return content['listenKey']
        
    
    def get_market_price(self,symbol):
        url = 'https://fapi.binance.com/fapi/v1/premiumIndex'
        params = {'symbol': symbol}
        response = requests.get(url=url, params=params)
        c1 = json.loads(response.content)
        return c1['markPrice']

    def limit_order(self, symbol, quantity, positionSide,price):
        timeInForce = "GTC"
        if(positionSide=='LONG'):
            side='BUY'
        else: side='SELL'
        url = "https://fapi.binance.com/fapi/v1/order"

        server_time_url = 'https://api1.binance.com/api/v3/time'
        get_server_time = requests.get(server_time_url)
        server_time = json.loads(get_server_time.content)
        ts = server_time["serverTime"]

        params = 'symbol=' + symbol +'&type=LIMIT&quantity=' + str(quantity) + '&side=' + side+ '&positionSide='  + positionSide+'&price=' + str(float(price))+'&timeInForce=' +timeInForce +'&timestamp=' + str(ts)
        signuture = self.hasing(params)
        order = {"symbol": symbol, "type": "LIMIT", "quantity": str(quantity), "side": side,"positionSide": positionSide,"price":float(price),"timeInForce":timeInForce,"timestamp": ts,
                 'signature': signuture}
        headers = {"X-MBX-APIKEY": self.apiKey}

        response = requests.post(url, headers=headers, params=order)
        print(response.content)
   
            
    
