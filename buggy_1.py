# -*- coding: utf-8 -*-
"""
buggy_1.py  ―  판매 데이터 매출 집계 (csv 모듈 버전)

dirty_sales.csv를 한 줄씩 읽어 '매출액 = 단가 x 수량'을 누적한다.
잘 돌아가는 것처럼 보이지만, 어떤 행에서 갑자기 멈춘다.

[과제] 이 스크립트를 실행해 Traceback을 얻고,
       진단 3단계 루틴(무엇이 / 어디서 / 왜)으로 원인을 특정한 뒤
       전처리로 해결하라. (힌트: 예외 타입은 무엇인가?)
"""

"""


1. 에러 확인 (무엇이)

ValueError: invalid literal for int() with base 10: '5,200'
ValueError: invalid literal for int() with base 10: '4200원'
ValueError: invalid literal for int() with base 10: ''

2. 에러 위치 (어디서)

39번째 줄에서 int 형 변환을 시도할 때 오류가 발생한다.
price = int(row["price"]) <-- 문제 부분

3. 원인 (왜)    

price에 콤마(,)와 단위(원), 공백이 섞여 있어 int() 변환이 실패한다.

4. 해결방법

replace method로 콤마, 단위를 제거하고 strip()으로 앞뒤 공백을 제거한 후
공백 문자열은 0으로 변환하여 int() 변환을 시도한다.

5. 결과 

dirty_sales.csv
------------------
총 매출액: 151,198,388,824원
ㄴ int 변환문제는 해결했으나 이상치로 인한 값 이상을 확인할 수 있다.

sales.csv
------------------
총 매출액: 3,836,000원
ㄴ 정상적으로 출력되는 걸 볼 수 있다. 기존의 정상데이터로도 정상 동작한다.
"""
import csv

def calc_total(path):
    total = 0
    with open(path, "r", encoding="UTF-8") as f:
        reader = csv.DictReader(f)  # 사전타입으로 데이터를 읽음.
        for i, row in enumerate(reader):
            # price = int(row["price"])        # <-- 여기가 문제의 줄
            raw_price = row["price"].replace(",", "").replace("원", "").strip()  #FIXED : 콤마와 단위(원) 제거 [int변환시 오류발생]
            price = int(raw_price) if raw_price else 0  #FIXED : 빈 문자열은 0으로 처리 [int변환시 오류발생]
            qty = int(row["quantity"])
            total += price * qty
    return total

if __name__ == "__main__":
    total = calc_total("dirty_sales.csv")
    print(f"총 매출액: {total:,}원")
