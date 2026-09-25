# -*- coding: utf-8 -*-
"""
buggy_5.py  ―  '앞 행 대비 가격 변화'가 큰 행 찾기

정제한 price를 앞뒤로 비교하며 급변 지점을 찾으려 한다.
데이터에는 이상치(-4500, 9999999)도 섞여 있어 변화폭이 튀는 구간이 있다.
그런데 반복문이 끝까지 가지 못하고 죽는다.

[과제] Traceback으로 예외 타입을 확인하라(힌트: 반복문 경계).
       print 디버깅이 500줄 출력을 뒤져야 한다면,
       디버거의 '조건부 중단점'(예: 조건식  i >= len(prices) - 2)을 걸어
       문제의 반복 지점에서 곧바로 멈춰 원인을 관찰한 뒤 수정하라.
"""



"""
1. 에러 확인 (무엇이)

Traceback (most recent call last):
  File "F:\desk\Week04\buggy_5.py", line 69, in <module>
    jumps = find_big_jumps(prices)
  File "F:\desk\Week04\buggy_5.py", line 62, in find_big_jumps
    diff = prices[i + 1] - prices[i]      # <-- 여기가 문제의 줄
           ~~~~~~^^^^^^^
IndexError: list index out of range

2. 에러 위치 (어디서)

diff = prices[i + 1] - prices[i] 줄에서 IndexError: list index out of range 에러가 발생한다.

3. 원인 (왜)    

디버깅을 통해 확인한다.
가장 의심스러운 부분으로 i =499일 때를 breakpoint조건으로 설정하여 디버깅하였다.
 diff = prices[i + 1] - prices[i]에서 i+1이 500이 되어 범위를 벗어나 IndexError가 발생한다.


4. 해결방법

반복문 범위를 len(prices)-1로 수정하여 문제를 해결한다.

5. 결과 

dirty_sales.csv
------------------
급변 지점 2건
(249, 21000.0, 9999999.0, 9978999.0)
(250, 9999999.0, 3500.0, -9996499.0)
ㄴ 반복문 범위를 len(prices)-1로 수정하여 문제를 해결하였다.

sales.csv
------------------
급변 지점 0건
ㄴ 정제된 데이터에서도 정상 처리 되는 것을 볼 수 있다.


"""
import pandas as pd

def load_prices(path):
    df = pd.read_csv(path, encoding="utf-8")
    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    # 결측은 0으로 두고, 리스트로 변환해 순회한다
    return df["price"].fillna(0).tolist()

def find_big_jumps(prices, threshold=100000):
    jumps = []
    for i in range(len(prices)-1): # <-- 반복문 범위를 len(prices)-1로 수정
        diff = prices[i + 1] - prices[i]      # <-- 여기가 문제의 줄
        if abs(diff) >= threshold:
            jumps.append((i, prices[i], prices[i + 1], diff))
    return jumps

if __name__ == "__main__":
    prices = load_prices("dirty_sales.csv")
    jumps = find_big_jumps(prices)
    print(f"급변 지점 {len(jumps)}건")
    for row in jumps[:10]:
        print(row)
