#!/usr/bin/env python3
#-*- encoding: utf-8

import os
import os.path
import sys
import json
import time
import datetime
import requests
import redis
import websockets
import asyncio

MARKET_INFO_URL = "https://api.upbit.com/v1/market/all"
WSS_URL = "wss://api.upbit.com/websocket/v1"


class WsReceiever :
    def __init__(self) :
        self._nowDt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._connRedis = redis.StrictRedis( host='localhost', port=6379, db=0)

    def run( self) :
        print( "[WsReceiever.run() started] datetime : %s" % ( self._nowDt))

        marketList = self.getMarketList()
        info = [ {"ticket":"test"}
                 , {"type":"orderbook","codes": marketList}
                 , {"format" : "SIMPLE"}
        ]
        info = str( info).replace( "'" ,'"')
        asyncio.get_event_loop().run_until_complete(self.connUpbitWs( info))


    async def connUpbitWs( self, info):
        async with websockets.connect( WSS_URL) as websocket:
            await websocket.send( info)
            greeting = await websocket.recv()

            while True:
                data = await websocket.recv()
                jo = json.loads( data) 
                print( jo)
                self._connRedis.set(str( jo['cd']), json.dumps(jo))


    def getMarketList(self) :
        response = requests.request("GET", MARKET_INFO_URL)
        jsList = json.loads( response.text)
        re = []
        for js in jsList :
            if str( js['market'])[:3] != "KRW" :
                continue
            re.append( js['market'])
        return re

if __name__=="__main__" :
    WsReceiever().run()

