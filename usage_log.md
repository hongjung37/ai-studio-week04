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

- 전처리 코드 검증 (replace 및 strip)

발견된 에러의 주원인인 콤마(,)와 화폐 단위('원'), 그리고 공백을 제거하기 위해 문자열 메서드를 연속으로 사용(Method Chaining)한 것은 매우 적절한 접근이다. 
```Python
row["price"].replace(",", "").replace("원", "").strip()
```
를 통해 숫자가 아닌 불순물들을 1차적으로 걷어내어 순수한 숫자 형태의 문자열로 만드는 목적을 완벽하게 달성했다.

- 빈 문자열 처리 로직 검증 (삼항 연산자)

특히 칭찬할 만한 부분은 빈 문자열('')에 대한 처리다. 빈 문자열을 int()로 강제 변환하려 하면 즉시 ValueError가 발생한다. 여기서 파이썬은 빈 문자열을 논리 연산에서 False로 취급한다는 특성을 이용해,  
```Python 
price = int(raw_price) if raw_price else 0
```
와 같이 삼항 연산자를 구성한 것은 아주 똑똑한 방법이다. 이 한 줄의 코드로 인해, 텅 빈 데이터가 들어오더라도 에러를 뿜는 대신 안전하게 0으로 치환되어 연산이 중단되는 것을 완벽히 방지해 준다. 네가 짠 이 코드라면 현재 파악된 3가지 에러 케이스를 100% 방어할 수 있다.

- 미처 파악하지 못한 비정제 데이터 색출 방법 (디버깅)

하지만 실제 데이터에는 네가 예상치 못한 또 다른 오염 데이터(예: 알파벳 'O' 혼입, 달러 기호 '$', 탭 공백 \t 등)가 숨어있을 수 있다. 이런 녀석들을 샅샅이 찾아내려면 파이썬의 예외 처리(try-except)와 repr() 함수를 조합해야 한다.

아래처럼 코드를 감싸서 테스트해 보는 것을 권장한다.

```Python
raw_price = row["price"].replace(",", "").replace("원", "").strip()
try:
    price = int(raw_price) if raw_price else 0 
except ValueError:
    # 에러가 발생한 행의 원본 데이터를 적나라하게 출력
    print(f"[디버깅] 변환 실패 원본 데이터: {repr(row['price'])}")
    price = 0 
```
이렇게 try-except로 덫을 놓으면, 네 전처리 로직을 뚫고 들어오는 알 수 없는 불순물이 있을 때 프로그램이 죽는 대신 터미널에 그 정체를 고발하게 된다. 여기서 핵심은 repr() 함수를 썼다는 것이다. 단순 print()는 눈에 보이지 않는 공백문자를 숨겨버리지만, repr()은 문자열의 양끝 띄어쓰기나 줄바꿈 문자(\n) 같은 보이지 않는 특수 기호까지 따옴표로 묶어 날것 그대로 보여준다. 이 출력 결과를 확인하면 "아, 이번엔 이런 기호가 섞여서 에러가 났구나" 하고 추가적인 replace 로직을 쉽게 덧붙일 수 있다.


#### 채택/기각 판단
채택✅
스스로 생각한 로직에 대한 검증을 받을 수 있었고
추가로 이외의 비정제된 데이터에 대한 대처방법을 알 수 있었다.

## buggy_2.py
코드 작성시 AI 사용 하지 않음

## buggy_3.py
코드 작성시 AI 사용 하지 않음

## buggy_4.py
코드 작성시 AI 사용 하지 않음

## buggy_5.py
코드 작성시 AI 사용 하지 않음
### 검증

#### 프롬포트

---

현재 csv파일의 데이터를 pandas라이브러리를 사용하여 불러오고 price 의 컬럼을 순회하여 값이 급격하게 변하는 지점을 찾아내려고 하고 있어./
근데 아래 함수에서 diff = prices[i+1] - prices[i] 부분에서 에러가 발생하고 있어.
```Python
def find_big_jumps(prices, threshold=100000):
    jumps = []
    for i in range(len(prices)):
        diff = prices[i + 1] - prices[i]      # <-- 여기가 문제의 줄
        if abs(diff) >= threshold:
            jumps.append((i, prices[i], prices[i + 1], diff))
    return jumps
```
이러한 IndexValue 가 발생하고있어
```
Traceback (most recent call last):
  File "F:\desk\Week04\buggy_5.py", line 69, in <module>
    jumps = find_big_jumps(prices)
  File "F:\desk\Week04\buggy_5.py", line 62, in find_big_jumps
    diff = prices[i + 1] - prices[i]      # <-- 여기가 문제의 줄
           ~~~~~~^^^^^^^
IndexError: list index out of range
```
내가 확인한 결과 for loop의 순회 범위에 문제가 있어서 index 범위를 초과하는 것 같아.

그래서 index 범위가 어디서 초과하고 있는지 알려주고
나는 이 에러를 고치기 위해 반복문을 for i in range(len(prices) - 1):로 수정하려고 해. 
이러한 수정이 정확하게 동작할지 아니면 오작동할지 알려주고 전체코드가 아니라 해당 부분만 발췌해서 알려줘.

#### 답변

---

파이썬에서 리스트의 전체 길이가 N이라고 할 때, 인덱스는 0부터 시작해서 N-1까지만 존재한다.

네 녀석이 처음에 짠 코드인 for i in range(len(prices)):는 i가 마지막 인덱스인 N-1까지 도달하게 만들지. 그런데 그 아래 코드를 봐라. prices[i + 1]이라는 수식이 있지? i가 마지막 값인 N-1이 되었을 때 i + 1을 하면 인덱스는 N이 되어버린다. 당연히 리스트에는 N번째 방이 없으니 IndexError: list index out of range가 터지며 비명을 지르는 거다!

[수정할 코드]

```Python
for i in range(len(prices) - 1):
    diff = prices[i + 1] - prices[i]
```
네 녀석이 제안한 대로 반복문의 범위를 len(prices) - 1로 줄이면, i는 최대 N-2까지만 순회하게 된다. 그러면 i + 1을 하더라도 최대 N-1이 되기 때문에, 정확히 리스트의 마지막 원소까지만 접근하고 에러 없이 무사히 반복문이 종료되는 원리다!

#### 채택/기각 판단

---

채택✅

스스로 생각한 index 범위가 이탈하는 구간이 for loop라는 가설을 
AI에게 성공적으로 검증받았기 때문에 채택한다.

## 그외
usage_log.md 파일의 파일명을 AI_usage.md 로 두고 원격 레피지스토리에 push해버려 이를 처리할때 사용하였다.


프롬포트 - 원격레피스토리에 기준에 맞지않는 이름의 md 파일 AI_usage.md를 삭제하고 싶은데 어떻게함?


답변 - 원격 저장소에서 삭제하려면 로컬 Git 추적 목록에서 AI_usage.md를 삭제 커밋한 뒤 push하면 됩니다. AI_usage.md는 이미 로컬에서 삭제되어 있고, 아직 삭제 내용만 커밋되지 않은 상태입니다. 다른 미추적 파일은 건드리지 않고 이 삭제만 stage해서 커밋한 뒤 main에 push하면 됩니다.


```
git add -u -- AI_usage.md; 
git commit -m "chore: remove AI_usage documentation"; git push origin main
```
