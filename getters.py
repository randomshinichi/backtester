from datetime import datetime, timezone
import ccxt
import requests


def ccxt_getter(args):
    exchange = getattr(ccxt, args.exchange)()
    try:
        candles = exchange.fetchOhlcv(args.pair, args.timeframe, since=exchange.parse8601('2017-01-01 00:00:00'))
        candles.sort(key=lambda x: x[0])
        return candles
    except KeyError:
        print("Exchange doesn't support that timeframe. Supported timeframes: \n", exchange.timeframes)
        exit()


def bittrex_getter(args):
    def get(m, period='day'):
        url = 'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={}&tickInterval={}'
        resp = requests.get(url.format(m, period)).json()
        return resp['result']

    # Translate pair to Bittrex BASE-COIN format
    pair = args.pair.replace("/", "-")

    # Bittrex returns JSON. We need to translate to OHLCV for backtrader.
    intervals = {
        "1m": "oneMin",
        "5m": "fiveMin",
        "30m": "thirtyMin",
        "1h": "hour",
        "1d": "day"
    }
    candles_json = get(pair, period=intervals[args.timeframe])

    candles = []
    for l in candles_json:
        dt = datetime.strptime(l['T'], "%Y-%m-%dT%H:%M:%S")
        dt = dt.replace(tzinfo=timezone.utc)
        candle = [dt.timestamp() * 1000, l['O'], l['H'], l['L'], l['C'], l['V']]
        candles.append(candle)
    return candles
