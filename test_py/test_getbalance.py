import time
import pyupbit
import datetime

access = "knD3ukPYXNxA8cxFJ5KQQFRXOaslshHxby1tGaG9"
secret = "BeOCZy2PkxhAg5x9xotMqSqijRK5YSYdHyyx5TxE"


def get_target_price(ticker, k):  # ticker => what coin?
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    # 전날 마감 가격 == 다음날 싯가
    target_price = df.iloc[0]['close'] + \
        (df.iloc[0]['high'] - df.iloc[0]['low']) * k  # 변동폭 *k랑 싯가에 더해줌
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    # upbit api 일봉 조회시 시작시간 9:00
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]  # 가장 첫번째 값이 시간 값
    return start_time


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


krw = get_balance("KRW")
btc = get_balance("BTC")

print(krw)
print(btc)
