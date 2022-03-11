# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxtpro.base.exchange import Exchange
import ccxt.async_support as ccxt
from ccxtpro.base.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired


class huobi(Exchange, ccxt.huobi):

    def describe(self):
        return self.deep_extend(super(huobi, self).describe(), {
            'has': {
                'ws': True,
                'watchOrderBook': True,
                'watchTickers': False,  # for now
                'watchTicker': True,
                'watchTrades': True,
                'watchMyTrades': True,
                'watchBalance': False,  # for now
                'watchOHLCV': True,
            },
            'urls': {
                'api': {
                    'ws': {
                        'api': {
                            'spot': {
                                'public': 'wss://{hostname}/ws',
                                'private': 'wss://{hostname}/ws/v2',
                            },
                            'future': {
                                'linear': {
                                    'public': 'wss://api.hbdm.com/linear-swap-ws',
                                    'private': 'wss://api.hbdm.com/linear-swap-notification',
                                },
                                'inverse': {
                                    'public': 'wss://api.hbdm.com/ws',
                                    'private': 'wss://api.hbdm.com/notification',
                                },
                            },
                            'swap': {
                                'inverse': {
                                    'public': 'wss://api.hbdm.com/swap-ws',
                                    'private': 'wss://api.hbdm.com/swap-notification',
                                },
                                'linear': {
                                    'public': 'wss://api.hbdm.com/linear-swap-ws',
                                    'private': 'wss://api.hbdm.com/linear-swap-notification',
                                },
                            },
                        },
                        # these settings work faster for clients hosted on AWS
                        'api-aws': {
                            'public': 'wss://api-aws.huobi.pro/ws',
                            'private': 'wss://api-aws.huobi.pro/ws/v2',
                        },
                    },
                },
            },
            'options': {
                'tradesLimit': 1000,
                'OHLCVLimit': 1000,
                'api': 'api',  # or api-aws for clients hosted on AWS
                'watchOrderBookSnapshot': {
                    'delay': 1000,
                },
                'ws': {
                    'gunzip': True,
                },
            },
        })

    def request_id(self):
        requestId = self.sum(self.safe_integer(self.options, 'requestId', 0), 1)
        self.options['requestId'] = requestId
        return str(requestId)

    async def watch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        messageHash = 'market.' + market['id'] + '.detail'
        url = self.get_url_by_market_type(market['type'], market['linear'])
        return await self.subscribe_public(url, symbol, messageHash, None, params)

    def handle_ticker(self, client, message):
        #
        #     {
        #         ch: 'market.btcusdt.detail',
        #         ts: 1583494163784,
        #         tick: {
        #             id: 209988464418,
        #             low: 8988,
        #             high: 9155.41,
        #             open: 9078.91,
        #             close: 9136.46,
        #             vol: 237813910.5928412,
        #             amount: 26184.202558551195,
        #             version: 209988464418,
        #             count: 265673
        #         }
        #     }
        #
        tick = self.safe_value(message, 'tick', {})
        ch = self.safe_string(message, 'ch')
        parts = ch.split('.')
        marketId = self.safe_string(parts, 1)
        market = self.safe_market(marketId)
        ticker = self.parse_ticker(tick, market)
        timestamp = self.safe_value(message, 'ts')
        ticker['timestamp'] = timestamp
        ticker['datetime'] = self.iso8601(timestamp)
        symbol = ticker['symbol']
        self.tickers[symbol] = ticker
        client.resolve(ticker, ch)
        return message

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        messageHash = 'market.' + market['id'] + '.trade.detail'
        url = self.get_url_by_market_type(market['type'], market['linear'])
        trades = await self.subscribe_public(url, symbol, messageHash, None, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message):
        #
        #     {
        #         ch: "market.btcusdt.trade.detail",
        #         ts: 1583495834011,
        #         tick: {
        #             id: 105004645372,
        #             ts: 1583495833751,
        #             data: [
        #                 {
        #                     id: 1.050046453727319e+22,
        #                     ts: 1583495833751,
        #                     tradeId: 102090727790,
        #                     amount: 0.003893,
        #                     price: 9150.01,
        #                     direction: "sell"
        #                 }
        #             ]
        #         }
        #     }
        #
        tick = self.safe_value(message, 'tick', {})
        data = self.safe_value(tick, 'data', {})
        ch = self.safe_string(message, 'ch')
        parts = ch.split('.')
        marketId = self.safe_string(parts, 1)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        tradesCache = self.safe_value(self.trades, symbol)
        if tradesCache is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            tradesCache = ArrayCache(limit)
            self.trades[symbol] = tradesCache
        for i in range(0, len(data)):
            trade = self.parse_trade(data[i], market)
            tradesCache.append(trade)
        client.resolve(tradesCache, ch)
        return message

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        interval = self.timeframes[timeframe]
        messageHash = 'market.' + market['id'] + '.kline.' + interval
        url = self.get_url_by_market_type(market['type'], market['linear'])
        ohlcv = await self.subscribe_public(url, symbol, messageHash, None, params)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message):
        #
        #     {
        #         ch: 'market.btcusdt.kline.1min',
        #         ts: 1583501786794,
        #         tick: {
        #             id: 1583501760,
        #             open: 9094.5,
        #             close: 9094.51,
        #             low: 9094.5,
        #             high: 9094.51,
        #             amount: 0.44639786263800907,
        #             vol: 4059.76919054,
        #             count: 16
        #         }
        #     }
        #
        ch = self.safe_string(message, 'ch')
        parts = ch.split('.')
        marketId = self.safe_string(parts, 1)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        interval = self.safe_string(parts, 3)
        timeframe = self.find_timeframe(interval)
        self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
        stored = self.safe_value(self.ohlcvs[symbol], timeframe)
        if stored is None:
            limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
            stored = ArrayCacheByTimestamp(limit)
            self.ohlcvs[symbol][timeframe] = stored
        tick = self.safe_value(message, 'tick')
        parsed = self.parse_ohlcv(tick, market)
        stored.append(parsed)
        client.resolve(stored, ch)

    async def watch_order_book(self, symbol, limit=None, params={}):
        if (limit is not None) and (limit != 150):
            raise ExchangeError(self.id + ' watchOrderBook accepts limit = 150 only')
        await self.load_markets()
        market = self.market(symbol)
        # only supports a limit of 150 at self time
        limit = 150 if (limit is None) else limit
        messageHash = None
        if market['spot']:
            messageHash = 'market.' + market['id'] + '.mbp.' + str(limit)
        else:
            messageHash = 'market.' + market['id'] + '.depth.size_' + str(limit) + '.high_freq'
        url = self.get_url_by_market_type(market['type'], market['linear'])
        if not market['spot']:
            params['data_type'] = 'incremental'
        orderbook = await self.subscribe_public(url, symbol, messageHash, self.handle_order_book_subscription, params)
        return orderbook.limit(limit)

    def handle_order_book_snapshot(self, client, message, subscription):
        #
        #     {
        #         id: 1583473663565,
        #         rep: 'market.btcusdt.mbp.150',
        #         status: 'ok',
        #         data: {
        #             seqNum: 104999417756,
        #             bids: [
        #                 [9058.27, 0],
        #                 [9058.43, 0],
        #                 [9058.99, 0],
        #             ],
        #             asks: [
        #                 [9084.27, 0.2],
        #                 [9085.69, 0],
        #                 [9085.81, 0],
        #             ]
        #         }
        #     }
        #
        symbol = self.safe_string(subscription, 'symbol')
        messageHash = self.safe_string(subscription, 'messageHash')
        orderbook = self.orderbooks[symbol]
        data = self.safe_value(message, 'data')
        snapshot = self.parse_order_book(data, symbol)
        snapshot['nonce'] = self.safe_integer(data, 'seqNum')
        orderbook.reset(snapshot)
        # unroll the accumulated deltas
        messages = orderbook.cache
        for i in range(0, len(messages)):
            message = messages[i]
            self.handle_order_book_message(client, message, orderbook)
        self.orderbooks[symbol] = orderbook
        client.resolve(orderbook, messageHash)

    async def watch_order_book_snapshot(self, client, message, subscription):
        # quick-fix to avoid getting outdated snapshots
        options = self.safe_value(self.options, 'watchOrderBookSnapshot', {})
        delay = self.safe_integer(options, 'delay')
        if delay is not None:
            await self.sleep(delay)
        symbol = self.safe_string(subscription, 'symbol')
        limit = self.safe_integer(subscription, 'limit')
        params = self.safe_value(subscription, 'params')
        messageHash = self.safe_string(subscription, 'messageHash')
        market = self.market(symbol)
        url = self.get_url_by_market_type(market['type'], market['linear'])
        requestId = self.request_id()
        request = {
            'req': messageHash,
            'id': requestId,
        }
        # self is a temporary subscription by a specific requestId
        # it has a very short lifetime until the snapshot is received over ws
        snapshotSubscription = {
            'id': requestId,
            'messageHash': messageHash,
            'symbol': symbol,
            'limit': limit,
            'params': params,
            'method': self.handle_order_book_snapshot,
        }
        orderbook = await self.watch(url, requestId, request, requestId, snapshotSubscription)
        return orderbook.limit(limit)

    async def fetch_order_book_snapshot(self, client, message, subscription):
        symbol = self.safe_string(subscription, 'symbol')
        limit = self.safe_integer(subscription, 'limit')
        params = self.safe_value(subscription, 'params')
        messageHash = self.safe_string(subscription, 'messageHash')
        snapshot = await self.fetch_order_book(symbol, limit, params)
        orderbook = self.safe_value(self.orderbooks, symbol)
        if orderbook is not None:
            orderbook.reset(snapshot)
            # unroll the accumulated deltas
            messages = orderbook.cache
            for i in range(0, len(messages)):
                message = messages[i]
                self.handle_order_book_message(client, message, orderbook)
            self.orderbooks[symbol] = orderbook
            client.resolve(orderbook, messageHash)

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_order_book_message(self, client, message, orderbook):
        # spot markets
        #     {
        #         ch: "market.btcusdt.mbp.150",
        #         ts: 1583472025885,
        #         tick: {
        #             seqNum: 104998984994,
        #             prevSeqNum: 104998984977,
        #             bids: [
        #                 [9058.27, 0],
        #                 [9058.43, 0],
        #                 [9058.99, 0],
        #             ],
        #             asks: [
        #                 [9084.27, 0.2],
        #                 [9085.69, 0],
        #                 [9085.81, 0],
        #             ]
        #         }
        #     }
        # non-spot market
        #     {
        #         "ch":"market.BTC220218.depth.size_150.high_freq",
        #         "tick":{
        #            "asks":[
        #            ],
        #            "bids":[
        #               [43445.74,1],
        #               [43444.48,0],
        #               [40593.92,9]
        #             ],
        #            "ch":"market.BTC220218.depth.size_150.high_freq",
        #            "event":"update",
        #            "id":152727500274,
        #            "mrid":152727500274,
        #            "ts":1645023376098,
        #            "version":37536690
        #         },
        #         "ts":1645023376098
        #      }
        tick = self.safe_value(message, 'tick', {})
        seqNum = self.safe_integer_2(tick, 'seqNum', 'id')
        prevSeqNum = self.safe_integer(tick, 'prevSeqNum')
        if (prevSeqNum is None or prevSeqNum <= orderbook['nonce']) and (seqNum > orderbook['nonce']):
            asks = self.safe_value(tick, 'asks', [])
            bids = self.safe_value(tick, 'bids', [])
            self.handle_deltas(orderbook['asks'], asks)
            self.handle_deltas(orderbook['bids'], bids)
            orderbook['nonce'] = seqNum
            timestamp = self.safe_integer(message, 'ts')
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
        return orderbook

    def handle_order_book(self, client, message):
        #
        # deltas
        #
        # spot markets
        #     {
        #         ch: "market.btcusdt.mbp.150",
        #         ts: 1583472025885,
        #         tick: {
        #             seqNum: 104998984994,
        #             prevSeqNum: 104998984977,
        #             bids: [
        #                 [9058.27, 0],
        #                 [9058.43, 0],
        #                 [9058.99, 0],
        #             ],
        #             asks: [
        #                 [9084.27, 0.2],
        #                 [9085.69, 0],
        #                 [9085.81, 0],
        #             ]
        #         }
        #     }
        #
        # non spot markets
        #     {
        #         "ch":"market.BTC220218.depth.size_150.high_freq",
        #         "tick":{
        #            "asks":[
        #            ],
        #            "bids":[
        #               [43445.74,1],
        #               [43444.48,0],
        #               [40593.92,9]
        #             ],
        #            "ch":"market.BTC220218.depth.size_150.high_freq",
        #            "event":"update",
        #            "id":152727500274,
        #            "mrid":152727500274,
        #            "ts":1645023376098,
        #            "version":37536690
        #         },
        #         "ts":1645023376098
        #      }
        messageHash = self.safe_string(message, 'ch')
        ch = self.safe_value(message, 'ch')
        parts = ch.split('.')
        marketId = self.safe_string(parts, 1)
        symbol = self.safe_symbol(marketId)
        orderbook = self.safe_value(self.orderbooks, symbol)
        if orderbook is None:
            size = self.safe_string(parts, 3)
            sizeParts = size.split('_')
            limit = self.safe_number(sizeParts, 1)
            orderbook = self.order_book({}, limit)
        if orderbook['nonce'] is None:
            orderbook.cache.append(message)
        else:
            self.handle_order_book_message(client, message, orderbook)
            client.resolve(orderbook, messageHash)

    def handle_order_book_subscription(self, client, message, subscription):
        symbol = self.safe_string(subscription, 'symbol')
        limit = self.safe_integer(subscription, 'limit')
        if symbol in self.orderbooks:
            del self.orderbooks[symbol]
        self.orderbooks[symbol] = self.order_book({}, limit)
        if self.markets[symbol]['spot'] is True:
            self.spawn(self.watch_order_book_snapshot, client, message, subscription)
        else:
            self.spawn(self.fetch_order_book_snapshot, client, message, subscription)

    async def watch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.check_required_credentials()
        type = None
        marketId = '*'  # wildcard
        if symbol is not None:
            await self.load_markets()
            market = self.market(symbol)
            type = market['type']
            marketId = market['id'].lower()
        else:
            type, params = self.handle_market_type_and_params('watchMyTrades', None, params)
        if type != 'spot':
            raise ArgumentsRequired(self.id + ' watchMyTrades supports spot markets only')
        mode = None
        if mode is None:
            mode = self.safe_string_2(self.options, 'watchMyTrades', 'mode', 0)
            mode = self.safe_string(params, 'mode', mode)
        messageHash = 'trade.clearing' + '#' + marketId + '#' + mode
        trades = await self.subscribe_private(messageHash, type, 'linear', params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit)

    def handle_subscription_status(self, client, message):
        #
        #     {
        #         "id": 1583414227,
        #         "status": "ok",
        #         "subbed": "market.btcusdt.mbp.150",
        #         "ts": 1583414229143
        #     }
        #
        id = self.safe_string(message, 'id')
        subscriptionsById = self.index_by(client.subscriptions, 'id')
        subscription = self.safe_value(subscriptionsById, id)
        if subscription is not None:
            method = self.safe_value(subscription, 'method')
            if method is not None:
                return method(client, message, subscription)
            # clean up
            if id in client.subscriptions:
                del client.subscriptions[id]
        return message

    def handle_system_status(self, client, message):
        #
        # todo: answer the question whether handleSystemStatus should be renamed
        # and unified as handleStatus for any usage pattern that
        # involves system status and maintenance updates
        #
        #     {
        #         id: '1578090234088',  # connectId
        #         type: 'welcome',
        #     }
        #
        return message

    def handle_subject(self, client, message):
        # spot
        #     {
        #         ch: "market.btcusdt.mbp.150",
        #         ts: 1583472025885,
        #         tick: {
        #             seqNum: 104998984994,
        #             prevSeqNum: 104998984977,
        #             bids: [
        #                 [9058.27, 0],
        #                 [9058.43, 0],
        #                 [9058.99, 0],
        #             ],
        #             asks: [
        #                 [9084.27, 0.2],
        #                 [9085.69, 0],
        #                 [9085.81, 0],
        #             ]
        #         }
        #     }
        # non spot
        #     {
        #         "ch":"market.BTC220218.depth.size_150.high_freq",
        #         "tick":{
        #            "asks":[
        #            ],
        #            "bids":[
        #               [43445.74,1],
        #               [43444.48,0],
        #               [40593.92,9]
        #             ],
        #            "ch":"market.BTC220218.depth.size_150.high_freq",
        #            "event":"update",
        #            "id":152727500274,
        #            "mrid":152727500274,
        #            "ts":1645023376098,
        #            "version":37536690
        #         },
        #         "ts":1645023376098
        #      }
        # spot private trade
        #
        #  {
        #      "action":"push",
        #      "ch":"trade.clearing#ltcusdt#1",
        #      "data":{
        #         "eventType":"trade",
        #         "symbol":"ltcusdt",
        #           (...)
        #  }
        #
        ch = self.safe_value(message, 'ch')
        parts = ch.split('.')
        type = self.safe_string(parts, 0)
        if type == 'market':
            methodName = self.safe_string(parts, 2)
            methods = {
                'depth': self.handle_order_book,
                'mbp': self.handle_order_book,
                'detail': self.handle_ticker,
                'trade': self.handle_trades,
                'kline': self.handle_ohlcv,
                # ...
            }
            method = self.safe_value(methods, methodName)
            if method is None:
                return message
            else:
                return method(client, message)
        # private subjects
        privateParts = ch.split('#')
        privateType = self.safe_string(privateParts, 0)
        if privateType == 'trade.clearing':
            self.handle_my_trade(client, message)

    async def pong(self, client, message):
        #
        #     {ping: 1583491673714}
        #
        # or
        #     {action: 'ping', data: {ts: 1645108204665}}
        #
        # or
        #     {op: 'ping', ts: '1645202800015'}
        #
        ping = self.safe_integer(message, 'ping')
        if ping is not None:
            await client.send({'pong': ping})
            return
        action = self.safe_string(message, 'action')
        if action == 'ping':
            data = self.safe_value(message, 'data')
            ping = self.safe_integer(data, 'ts')
            await client.send({'action': 'pong', 'data': {'ts': ping}})
            return
        op = self.safe_string(message, 'op')
        if op == 'ping':
            ping = self.safe_integer(message, 'ts')
            await client.send({'op': 'pong', 'ts': ping})

    def handle_ping(self, client, message):
        self.spawn(self.pong, client, message)

    def handle_authenticate(self, client, message):
        # spot
        # {
        #     "action": "req",
        #     "code": 200,
        #     "ch": "auth",
        #     "data": {}
        # }
        # non spot
        #    {
        #        op: 'auth',
        #        type: 'api',
        #        'err-code': 0,
        #        ts: 1645200307319,
        #        data: {'user-id': '35930539'}
        #    }
        #
        client.resolve(message, 'auth')
        return message

    def handle_error_message(self, client, message):
        #
        #     {
        #         ts: 1586323747018,
        #         status: 'error',
        #         'err-code': 'bad-request',
        #         'err-msg': 'invalid mbp.150.symbol linkusdt',
        #         id: '2'
        #     }
        #
        status = self.safe_string(message, 'status')
        if status == 'error':
            id = self.safe_string(message, 'id')
            subscriptionsById = self.index_by(client.subscriptions, 'id')
            subscription = self.safe_value(subscriptionsById, id)
            if subscription is not None:
                errorCode = self.safe_string(message, 'err-code')
                try:
                    self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, self.json(message))
                except Exception as e:
                    messageHash = self.safe_string(subscription, 'messageHash')
                    client.reject(e, messageHash)
                    client.reject(e, id)
                    if id in client.subscriptions:
                        del client.subscriptions[id]
            return False
        return message

    def handle_message(self, client, message):
        if self.handle_error_message(client, message):
            #
            #     {"id":1583414227,"status":"ok","subbed":"market.btcusdt.mbp.150","ts":1583414229143}
            #
            # first ping format
            #
            #    {'ping': 1645106821667}
            #
            # second ping format
            #
            #    {"action":"ping","data":{"ts":1645106821667}}
            #
            # third pong format
            #
            #
            # auth spot
            #     {
            #         "action": "req",
            #         "code": 200,
            #         "ch": "auth",
            #         "data": {}
            #     }
            # auth non spot
            #    {
            #        op: 'auth',
            #        type: 'api',
            #        'err-code': 0,
            #        ts: 1645200307319,
            #        data: {'user-id': '35930539'}
            #    }
            # trade
            # {
            #     "action":"push",
            #     "ch":"trade.clearing#ltcusdt#1",
            #     "data":{
            #        "eventType":"trade",
            #          (...)
            #     }
            #  }
            #
            if 'id' in message:
                self.handle_subscription_status(client, message)
                return
            if 'action' in message:
                action = self.safe_string(message, 'action')
                if action == 'ping':
                    self.handle_ping(client, message)
                    return
                if action == 'sub':
                    self.handle_subscription_status(client, message)
                    return
            if 'ch' in message:
                if message['ch'] == 'auth':
                    self.handle_authenticate(client, message)
                    return
                else:
                    # route by channel aka topic aka subject
                    self.handle_subject(client, message)
                    return
            if 'ping' in message:
                self.handle_ping(client, message)

    def handle_my_trade(self, client, message):
        #
        # spot
        #
        # {
        #     "action":"push",
        #     "ch":"trade.clearing#ltcusdt#1",
        #     "data":{
        #        "eventType":"trade",
        #        "symbol":"ltcusdt",
        #        "orderId":"478862728954426",
        #        "orderSide":"buy",
        #        "orderType":"buy-market",
        #        "accountId":44234548,
        #        "source":"spot-web",
        #        "orderValue":"5.01724137",
        #        "orderCreateTime":1645124660365,
        #        "orderStatus":"filled",
        #        "feeCurrency":"ltc",
        #        "tradePrice":"118.89",
        #        "tradeVolume":"0.042200701236437042",
        #        "aggressor":true,
        #        "tradeId":101539740584,
        #        "tradeTime":1645124660368,
        #        "transactFee":"0.000041778694224073",
        #        "feeDeduct":"0",
        #        "feeDeductType":""
        #     }
        #  }
        #
        if self.myTrades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            self.myTrades = ArrayCacheBySymbolById(limit)
        cachedTrades = self.myTrades
        messageHash = self.safe_string(message, 'ch')
        if messageHash is not None:
            data = self.safe_value(message, 'data')
            parsed = self.parse_ws_trade(data)
            symbol = self.safe_string(parsed, 'symbol')
            if symbol is not None:
                cachedTrades.append(parsed)
            client.resolve(self.myTrades, messageHash)

    def parse_ws_trade(self, trade):
        # spot private
        #
        #   {
        #        "eventType":"trade",
        #        "symbol":"ltcusdt",
        #        "orderId":"478862728954426",
        #        "orderSide":"buy",
        #        "orderType":"buy-market",
        #        "accountId":44234548,
        #        "source":"spot-web",
        #        "orderValue":"5.01724137",
        #        "orderCreateTime":1645124660365,
        #        "orderStatus":"filled",
        #        "feeCurrency":"ltc",
        #        "tradePrice":"118.89",
        #        "tradeVolume":"0.042200701236437042",
        #        "aggressor":true,
        #        "tradeId":101539740584,
        #        "tradeTime":1645124660368,
        #        "transactFee":"0.000041778694224073",
        #        "feeDeduct":"0",
        #        "feeDeductType":""
        #  }
        symbol = self.safe_symbol(self.safe_string(trade, 'symbol'))
        side = self.safe_string_2(trade, 'side', 'orderSide')
        tradeId = self.safe_string(trade, 'tradeId')
        price = self.safe_string(trade, 'tradePrice')
        amount = self.safe_string(trade, 'tradeVolume')
        order = self.safe_string(trade, 'orderId')
        timestamp = self.safe_integer(trade, 'tradeTime')
        market = self.market(symbol)
        orderType = self.safe_string(trade, 'orderType')
        aggressor = self.safe_value(trade, 'aggressor')
        takerOrMaker = None
        if aggressor is not None:
            takerOrMaker = 'taker' if aggressor else 'maker'
        type = None
        if orderType is not None:
            orderType = orderType.split('-')
            type = self.safe_string(orderType, 1)
        fee = None
        feeCurrency = self.safe_currency_code(self.safe_string(trade, 'feeCurrency'))
        if feeCurrency is not None:
            fee = {
                'cost': self.safe_string(trade, 'transactFee'),
                'currency': feeCurrency,
            }
        return self.safe_trade({
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': tradeId,
            'order': order,
            'type': type,
            'takerOrMaker': takerOrMaker,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': None,
            'fee': fee,
        }, market)

    def get_url_by_market_type(self, type, isLinear=True, isPrivate=False):
        api = self.safe_string(self.options, 'api', 'api')
        hostname = {'hostname': self.hostname}
        hostnameURL = None
        url = None
        if type == 'spot':
            if isPrivate:
                hostnameURL = self.urls['api']['ws'][api]['spot']['private']
            else:
                hostnameURL = self.urls['api']['ws'][api]['spot']['public']
            url = self.implode_params(hostnameURL, hostname)
        else:
            baseUrl = self.urls['api']['ws'][api][type]
            subTypeUrl = baseUrl['linear'] if isLinear else baseUrl['inverse']
            url = subTypeUrl['private'] if isPrivate else subTypeUrl['public']
        return url

    async def subscribe_public(self, url, symbol, messageHash, method=None, params={}):
        requestId = self.request_id()
        request = {
            'sub': messageHash,
            'id': requestId,
        }
        subscription = {
            'id': requestId,
            'messageHash': messageHash,
            'symbol': symbol,
            'params': params,
        }
        if method is not None:
            subscription['method'] = method
        return await self.watch(url, messageHash, self.extend(request, params), messageHash, subscription)

    async def subscribe_private(self, messageHash, type, subtype, params={}):
        requestId = self.nonce()
        subscription = {
            'id': requestId,
            'messageHash': messageHash,
            'params': params,
        }
        request = None
        if type == 'spot':
            request = {
                'action': 'sub',
                'ch': messageHash,
            }
        else:
            request = {
                'op': 'sub',
                'topic': messageHash,
                'cid': requestId,
            }
        isLinear = subtype == 'linear'
        url = self.get_url_by_market_type(type, isLinear, True)
        hostname = self.urls['hostnames']['spot'] if (type == 'spot') else self.urls['hostnames']['contract']
        authParams = {
            'type': type,
            'url': url,
            'hostname': hostname,
        }
        if type == 'spot':
            self.options['ws']['gunzip'] = False
        await self.authenticate(authParams)
        return await self.watch(url, messageHash, self.extend(request, params), messageHash, subscription)

    async def authenticate(self, params={}):
        url = self.safe_string(params, 'url')
        hostname = self.safe_string(params, 'hostname')
        type = self.safe_string(params, 'type')
        if url is None or hostname is None or type is None:
            raise ArgumentsRequired(self.id + ' authenticate requires a url, hostname and type argument')
        self.check_required_credentials()
        messageHash = 'auth'
        relativePath = url.replace('wss://' + hostname, '')
        client = self.client(url)
        future = self.safe_value(client.subscriptions, messageHash)
        if future is None:
            future = client.future(messageHash)
            timestamp = self.ymdhms(self.milliseconds(), 'T')
            signatureParams = None
            if type == 'spot':
                signatureParams = {
                    'accessKey': self.apiKey,
                    'signatureMethod': 'HmacSHA256',
                    'signatureVersion': '2.1',
                    'timestamp': timestamp,
                }
            else:
                signatureParams = {
                    'AccessKeyId': self.apiKey,
                    'SignatureMethod': 'HmacSHA256',
                    'SignatureVersion': '2',
                    'Timestamp': timestamp,
                }
            signatureParams = self.keysort(signatureParams)
            auth = self.urlencode(signatureParams)
            payload = "\n".join(['GET', hostname, relativePath, auth])  # eslint-disable-line quotes
            signature = self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha256, 'base64')
            request = None
            if type == 'spot':
                params = {
                    'authType': 'api',
                    'accessKey': self.apiKey,
                    'signatureMethod': 'HmacSHA256',
                    'signatureVersion': '2.1',
                    'timestamp': timestamp,
                    'signature': signature,
                }
                request = {
                    'params': params,
                    'action': 'req',
                    'ch': messageHash,
                }
            else:
                request = {
                    'op': messageHash,
                    'type': 'api',
                    'AccessKeyId': self.apiKey,
                    'SignatureMethod': 'HmacSHA256',
                    'SignatureVersion': '2',
                    'Timestamp': timestamp,
                    'Signature': signature,
                }
            await self.watch(url, messageHash, request, messageHash, future)
        return await future
