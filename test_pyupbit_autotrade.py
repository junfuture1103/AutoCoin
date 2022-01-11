'''
=======================================================================
=======================================================================
=======================================================================
=======================================================================
============================= for test ================================
=======================================================================
=======================================================================
=======================================================================
=======================================================================
=======================================================================
=======================================================================

'''
import os
import time
import pyupbit
import datetime
import logging

access = "knD3ukPYXNxA8cxFJ5KQQFRXOaslshHxby1tGaG9"
secret = "BeOCZy2PkxhAg5x9xotMqSqijRK5YSYdHyyx5TxE"

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter(
    '%(asctime)s %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
logfile_path = './log/test.log'
# 몇 번째 로그파일?
file_num = len(os.listdir('./log'))
logfile_path += str(file_num)

# 로그 파일 생성
file_handler = logging.FileHandler(logfile_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_now_time_jun():
    tm = time.localtime(time.time())
    return print("Trading.. %d/%d/%d %d:%d:%d" % (
                 tm.tm_year,
                 tm.tm_mon,
                 tm.tm_mday,
                 tm.tm_hour,
                 tm.tm_min,
                 tm.tm_sec))


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

# for test KRW & BTC balance
test_krw = 10000000000
test_btc = 0

time1 = time.time()
# 자동매매 시작
while True:
    try:
        # get time
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)  # 다음날 9시 => 9:00+1일

        # 9:00 < 현재 < 20:59:50
        # 매수 목표가 설정
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            # get_target_price => 매수 목표가 설정
            target_price = get_target_price("KRW-BTC", 0.5)
            # 현재가 조회
            current_price = get_current_price("KRW-BTC")

            # 매수 조건 설정
            # 매수 목표가가 지금 가격보다 싸다면 구매
            if target_price < current_price:
                # test_krw = get_balance("KRW")
                if test_krw > 5000:
                    print("[Buy] target_price : ", target_price,
                          "current_price : ", current_price)
                    # buy_market_order함수 분석
                    # upbit.buy_market_order("KRW-BTC", krw*0.9995)
                    test_krw -= 5000
        else:
            # test_btc = get_balance("BTC")
            if test_btc > 0.00008:  # 5000에 따른 btc가격으로 바꿔줘야함
                print("[Sell] target_price : ", target_price,
                      "current_price : ", current_price)
                # upbit.sell_market_order("KRW-BTC", btc*0.9995)
                test_btc += 0.00008
        time.sleep(1)
        time2 = time.time()
        if (time2-time1 > 5):
            time1 = time2
            logger.info(
                f'current_price : {current_price} target_price : {target_price} test_KRW : {test_krw} test_BTC : {test_btc}')
    except Exception as e:
        print(e)
        time.sleep(1)
