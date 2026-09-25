# -*- coding: utf-8 -*-
"""
buggy_4.py  ―  총 매출액 집계 (에러 없이 '조용히' 틀리는 스크립트)

이 스크립트는 에러 없이 잘 돌아가고, 그럴듯한 숫자를 출력한다.
하지만 그 숫자는 '틀렸다'.

[과제] 이 스크립트는 예외를 던지지 않는다. 대신
       (1) info()/describe()로 데이터 상태를 먼저 세어 보고
       (2) '무엇이 틀렸는지 어떻게 알아챘는지'를 서술한 뒤
       (3) 결측 규모를 보고하고 처리 방법을 선택·적용하여
           올바른 총매출을 산출하라.
       (힌트: 가격 결측은 몇 건인가? 음수 가격과 9999999 같은 값은 정상인가?)
"""


"""
1. 에러 확인 (무엇이) [결측치 확인]

 #   Column    Non-Null Count  Dtype  
---  ------    --------------  -----  
 0   date      500 non-null    str    
 1   product   500 non-null    str    
 2   category  490 non-null    str    
 3   price     498 non-null    float64
 4   quantity  500 non-null    int64  
 5   stock     485 non-null    float64
ㄴ 결측치가 price 2건, category 10건, stock 15건 존재한다.



price 컬럼의 결측치를 살펴보면 다음과 같다.
           date product category  price  quantity  stock
399  2026-01-13   아메리카노       음료    NaN        86  124.0
468  2026-05-17     마들렌     베이커리    NaN       181  117.0

              price      quantity       stock
count  4.980000e+02  5.000000e+02  485.000000
mean   2.834237e+04  2.010569e+04  249.995876
std    4.477810e+05  4.472088e+05  141.211450
min   -4.500000e+03  1.000000e+00    1.000000
25%    3.800000e+03  5.375000e+01  128.000000
50%    5.000000e+03  1.120000e+02  250.000000
75%    1.200000e+04  1.610000e+02  363.000000
max    9.999999e+06  9.999999e+06  500.000000
ㄴ describe() 결과를 보면 price, quantity 컬럼에 음수(-4500)와 극단값(9999999)이 섞여 있다.


2. 에러 위치 (어디서)

코드 상의 문제가 아니다. dirty_sales.csv 파일에 데이터가 결측치, 이상치등이 섞여 들어가있다.

3. 원인 (왜)    

데이터에 결측치와 이상치가 섞여 있어 총매출 계산 결과가 틀리게 된다.
특히 이상치의 경우 총매출에 극심한 영향을 주게 된다(최대값이 9999999)

4. 해결방법

price의 경우 결측치 2건, 음수 1건, 극단값 1건이 존재한다. 따라서 이를 모두 제거하고 계산한다.
quantity의 경우 결측치가 없으므로 이상치만 제거한다.
category 컬럼과 stock 컬럼의 결측치는 집계에 영향을 주지 않으므로 그대로 두어도 된다.
따라서 price 컬럼의 결측치와 이상치, quantity 컬럼의 이상치를 제거한 뒤 총매출을 계산하면 된다.

[처리 후 descrtibe() 결과]
count    495.000000  495.000000  480.000000
mean    8290.909091  105.828283  251.504167
std     6068.413791   59.631262  141.153568
min     2800.000000    1.000000    1.000000
25%     3800.000000   53.000000  129.750000
50%     5000.000000  112.000000  252.500000
75%    12000.000000  160.500000  364.250000
max    21000.000000  200.000000  500.000000
ㄴ price는 10만이상, quantity는 1000이상인 값이 존재하지 않으므로 이상치 제거 후 총매출을 계산하면 된다. (카페 메뉴상 10만 이상, 수량 1000 이상은 상식적이지 않다)
ㄴ 그결과 총 매출액: 438,939,400원 라는 정상적 결과를 얻을 수 있다.

5. 결과 

dirty_sales.csv
------------------
총 매출액: 438,939,400원
평균 단가: 8,291원
ㄴ 정상적으로 출력되는 걸 볼 수 있다.

sales.csv
------------------
총 매출액: 3,836,000원
평균 단가: 5,194원
ㄴ 정상데이터도 정상적으로 처리되는 것을 볼 수 있다. 
"""


import pandas as pd

def main():
    df = pd.read_csv("dirty_sales.csv", encoding="utf-8")

    # price를 숫자로 바꾼다 (빈 값은 NaN이 된다 — 그런데 그 규모를 확인하지 않았다)
    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    #print(df.shape)     
    #print(df.info()) 
    #print(df.isna().sum()) 
    #print(df.describe()) 
    #print(df[df["price"].isna()].head())  #결측치와 이상치 확인

    #FIXED: 결측치와 이상치를 제거한다
    df = df.dropna(subset=["price", "quantity"])  #FIXED: 결측치 제거
    df = df[df["price"] >= 0] 
    df = df[df["quantity"] >= 0] #FIXED: 음수값 제거

    #FIXED: price의 IQR 이상치를 제거한다.
    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    df = df[df["price"].between(lower, upper)]

    #FIXED: quantity의 IQR 이상치를 제거한다.
    q1 = df["quantity"].quantile(0.25)
    q3 = df["quantity"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    df = df[df["quantity"].between(lower, upper)]

    #print(df.describe())  #describe() 결과를 확인하여 제대로 처리되었는지 확인한다.

    # 매출액 = 단가 x 수량 (NaN이 섞이면 그 행의 매출액도 NaN)
    df["revenue"] = df["price"] * df["quantity"]

    # sum()은 NaN을 조용히 건너뛰고, 음수/극단값은 그대로 더한다
    total = df["revenue"].sum()
    avg_price = df["price"].mean()

    print(f"총 매출액: {total:,.0f}원")
    print(f"평균 단가: {avg_price:,.0f}원")
    # 출력은 그럴듯하지만, 이 숫자를 그대로 믿어도 될까?

if __name__ == "__main__":
    main()
