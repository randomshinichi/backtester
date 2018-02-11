#!/usr/bin/env python3
import csv
from datetime import datetime
import argparse
from getters import ccxt_getter, bittrex_getter

parser = argparse.ArgumentParser(description='Data fetcher for backtester')
parser.add_argument("pair", help="BTC/USD, ETH/BTC...")
parser.add_argument("exchange", help="bitfinex, binance, bittrex...")
parser.add_argument("timeframe", help="1h, 2h, 3h... exchange dependent")
args = parser.parse_args()


def write_csv(candles):
    def filename_friendly(pair):
        return pair.replace("/", "")
    filename = filename_friendly(args.pair) + '_' + args.timeframe + '.csv'
    with open(filename, 'w') as f:
        linewriter = csv.writer(f)
        for candle in candles:
            dtt = datetime.utcfromtimestamp(candle[0] / 1000)
            candle[0] = dtt.strftime('%Y-%m-%d %H:%M:%S')
            linewriter.writerow(candle)


if args.exchange == "bittrex":
    candles = bittrex_getter(args)
else:
    candles = ccxt_getter(args)

write_csv(candles)
