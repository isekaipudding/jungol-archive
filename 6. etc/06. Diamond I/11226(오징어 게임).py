# 링크 : https://jungol.co.kr/problem/11226
import sys

input = sys.stdin.readline

# 구사과님 에디토리얼 보고 직접 코드를 작성했어요.
# 와 어떻게 저런 수학적 원리가 나올 수 있죠?
# Least Absolute Remainder(A = Bq + r) 저거 하나만으로 이런 결과가 나오다니 정말 신기합니다.

def cycle(buckets:list):
    x_value, y_value, z_value = buckets[0][0], buckets[1][0], buckets[2][0]
    x_index, y_index, z_index = buckets[0][1], buckets[1][1], buckets[2][1]
    
    q, r = y_value // x_value, y_value % x_value
    
    target = q
    if r > x_value >> 1:
        target += 1
    
    is_case_2 = r > (x_value >> 1)
    code = bin(target)[2::][::-1]
    
    for i in range(len(code)):
        # 예외 처리
        if is_case_2 and i == len(code) - 1:
            x_value -= y_value
            y_value += y_value
            result.append((x_index, y_index))
            continue
        if code[i] == "0":
            z_value -= x_value
            x_value += x_value
            result.append((z_index, x_index))
        if code[i] == "1":
            y_value -= x_value
            x_value += x_value
            result.append((y_index, x_index))
    
    return [(x_value, x_index), (y_value, y_index), (z_value, z_index)]

X, Y, Z = map(int, input().split())
L:list = [(X, 1), (Y, 2), (Z, 3)]
result:list = []

while True:
    L.sort(key=lambda x: x[0])
    
    if L[0][0] == 0:
        break
        
    # B와 C의 물 양이 같으면 한 번에 붓고 즉시 종료(예외 처리)
    if L[1][0] == L[2][0]:
        result.append((L[1][1], L[2][1]))
        break
        
    L = cycle(L)

print(len(result))
for a, b in result:
    print(a, b)