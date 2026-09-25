# AI 사용 기록


## buggy_1.py
코드 작성시 AI 사용 하지 않음

### 검증

#### 프롬포트

현재 csv파일의 데이터를 csv라이브러리를 사용하여 불러오고 price 의 컬럼을 통해 total을 계산하려고 하고있어. / 이 함수의 price = int(row["price"]) 부분에서 error가 발생해 
```Python
def calc_total(path):
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # 사전타입으로 데이터를 읽음.
        for i, row in enumerate(reader):
            price = int(row["price"])        # <-- 여기가 문제의 줄
            qty = int(row["quantity"])
            total += price * qty
    return total
```
또한 이러한 ValueError 가 발생하고있어
```
ValueError: invalid literal for int() with base 10: '5,200'
ValueError: invalid literal for int() with base 10: '4200원'
ValueError: invalid literal for int() with base 10: ''
```
내가 확인한 결과 ,(콤마) 와 단위(원) 그리고 공백이 섞여 들어가서 int 형변환에 실패하는 것 같아.

그래서 이러한 Traceback 에러들을 잡기 위해 사용가능한 method , 그리고
이 외에의 어떠한 다른 비정제된 형식이 있을지 확인하는 방법을 알려줘

#### 답변

> 1. Traceback 에러를 잡기 위한 전처리 메서드문자열에 섞인 불순물을 걸러내려면 replace()와 strip() 메서드를 연속으로 사용(Chaining)하면 된다. 빈 문자열의 경우 삼항 연산자를 써서 0으로 둔갑시키면 아주 우아하게 해결되지.Python# 콤마와 '원'을 빈 문자열로 교체하고, 양끝 띄어쓰기나 줄바꿈을 제거한다.
```Python
raw_price = row["price"].replace(",", "").replace("원", "").strip()
```

> 정제된 문자열이 비어있지 않으면 int로 변환하고, 비어있으면 0을 넣는다.
```Python
price = int(raw_price) if raw_price else 0 
```

> 2. 숨겨진 비정제 데이터를 찾아내는 방법 (print 변수 추적)

내가 알려준 전처리를 거쳤는데도 또 에러가 터진다면, 우리가 예상치 못한 또 다른 형태의 불순물 데이터가 들어있다는 뜻이다. try-except 구문을 활용하면 정상 데이터는 통과시키고, 에러를 일으키는 녀석들만 쏙쏙 뽑아서 정체를 밝힐 수 있다.   
```Python
raw_price = row["price"].replace(",", "").replace("원", "").strip()
try:
    price = int(raw_price) if raw_price else 0 
except ValueError:
    # repr()을 쓰면 문자열 양끝의 보이지 않는 띄어쓰기나 특수문자 기호까지 적나라하게 보여준다.
    print(f"[DEBUG] 변환 실패 데이터: {repr(row['price'])}")
    price = 0 # 프로그램이 멈추지 않도록 일단 0으로 처리하고 다음 행으로 넘어감
```
이렇게 try-except로 덫을 쳐두고 스크립트를 실행해 보면 터미널에 변환을 거부하는 괘씸한 데이터들의 진짜 모습이 줄줄이 뜰 거다. 그걸 보고 전처리 코드(replace 등)를 추가로 붙여주면 완벽해지는 거지.

## buggy_2.py
코드 작성시 AI 사용 하지 않음

## buggy_3.py
코드 작성시 AI 사용 하지 않음

## buggy_4.py
코드 작성시 AI 사용 하지 않음

## buggy_5.py
코드 작성시 AI 사용 하지 않음

## 그외
usage_log.md 파일의 파일명을 AI_usage.md 로 두고 원격 레피지스토리에 push해버려 이를 처리할때 사용하였다.


프롬포트 - 원격레피스토리에 기준에 맞지않는 이름의 md 파일 AI_usage.md를 삭제하고 싶은데 어떻게함?


답변 - 원격 저장소에서 삭제하려면 로컬 Git 추적 목록에서 AI_usage.md를 삭제 커밋한 뒤 push하면 됩니다. AI_usage.md는 이미 로컬에서 삭제되어 있고, 아직 삭제 내용만 커밋되지 않은 상태입니다. 다른 미추적 파일은 건드리지 않고 이 삭제만 stage해서 커밋한 뒤 main에 push하면 됩니다.


```
git add -u -- AI_usage.md; 
git commit -m "chore: remove AI_usage documentation"; git push origin main
```
