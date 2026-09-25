# -*- coding: utf-8 -*-
"""
buggy_3.py  ―  데이터 로드 후 카테고리별 집계

load_and_clean()으로 데이터를 읽어 정제한 뒤,
그 결과를 groupby로 집계하려 한다.
그런데 집계 단계에서 이상한 에러가 난다.

[과제] Traceback의 예외 타입을 확인하고,
       'NoneType ...' 메시지가 가리키는 '이 변수를 만든 직전 단계'를
       역추적하여 원인 함수를 찾아 수정하라.
"""


"""
1. 에러 확인 (무엇이)

AttributeError: 'NoneType' object has no attribute 'groupby'

2. 에러 위치 (어디서)

df.groupby("category")["revenue"].sum() 을 실행할 때 오류가 발생한다.

3. 원인 (왜)    

load_and_clean() 함수에서 정제된 df를 반환하지 않고 있다. (return 문이 없다)

4. 해결방법

load_and_clean() 함수에서 정제된 df를 반환하도록 return 문을 추가한다.

5. 결과 

dirty_sales.csv
------------------
category
굿즈      1.500995e+11
베이커리    6.525450e+07
원두      1.808970e+08
음료      8.410400e+08
Name: revenue, dtype: float64
ㄴ load_and_clean() 함수에서 정제된 df를 반환하도록 return 문을 추가하여 문제를 해결하였다.
하지만 NaN 과 이상치가 섞여 있어 결과가 이상하게 보인다. 따라서 전처리로 NaN과 이상치를 제거해야 한다.

sales.csv
------------------
category
바닐라라떼    374000
샌드위치     532000
스콘       312000
아메리카노    283500
치즈케이크    500500
카페라떼     400000
카푸치노     340000
크로플      564000
크루아상     306000
휘낭시에     224000
Name: revenue, dtype: int64
ㄴ 카테고리 컬럼이 없어 임의로 카테고리명을 proudct 컬럼으로 사용하였다.
df["category"] = df["product"]  #FIXED: category 컬럼 생성
그 결과 정상적으로 처리되는 것을 볼 수 있다.
그렇기에 정상데이터에서의 동작이 검증되었다.

"""

import pandas as pd

def load_and_clean(path):
    df = pd.read_csv(path, encoding="utf-8")
    # price 컬럼을 숫자로 정제
    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["revenue"] = df["price"] * df["quantity"]
    # (여기서 정제된 df를 돌려주려고 했는데...)   <-- 무언가 빠져 있다
    return df  # FIXED: 정제된 df를 반환하도록 return 추가 [return이 없어 NoneType 에러 발생]

def main():
    df = load_and_clean("dirty_sales.csv")
    result = df.groupby("category")["revenue"].sum()   #FIXED: #제거 [주석 마크가 코드 도중에 혼용].
    print(result)

if __name__ == "__main__":
    main()
