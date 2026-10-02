# 링크 : https://jungol.co.kr/problem/4977
import sys

input = sys.stdin.readline

# 아예 처음부터 int가 아닌 str로 해서 size = len(B)에서 "0815"로 제대로 입력되도록 합니다.
A, B = map(str, input().rstrip().split("."))
# 정수 부분(2진수)
X:str = bin(int(A))[2::]

# 소수 부분(2진수)
size:int = len(B) # 반례 : 17.0815인 경우 B가 "0815"가 아닌 "815"로 잘못 입력될 수 있습니다.
B = int(B) # size를 먼저 할당한 뒤 그 다음에 정수로 변환합니다.
B *= 16 # 소수 4째 자리까지 내림하라고 했으니 16 곱해줍니다.
Y:str = bin(B // (10 ** size))[2::]
Y =  "0" * (4 - len(Y)) + Y

# 정수 부분과 소수 부분을 합쳐서 출력합니다.
result:str = X + "." + Y
print(result)