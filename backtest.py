import pyupbit
import numpy as np

# OHLCV(Open, high, low, close, volume) => 당일 시가 고가 저가 종가 거래량 불러오기
df = pyupbit.get_ohlcv("KRW-BTC", count=7)  # count 는 몇일 간 OHLCV?

# 변동폭*k값(range)는 (고가 - 저가) * K
df['range'] = (df['high'] - df['low']) * 0.5
# 매수가(target)은 시가(오늘 장 열릴떄 시작 값) + 변동폭*k 값
df['target'] = df['open'] + df['range'].shift(1)  # shift(1)은 다음날 정보니까 컬럼 한칸내림

#fee = 0.0032
# ror은 수익률 계산
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     # df['close'] / df['target'] - fee, #업비트 수수료?
                     1)

# 누적곱 계산(cumprod) => 누적 수익률 계산
df['hpr'] = df['ror'].cumprod()
# Draw Down 계산
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
# MDD 계산
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")
