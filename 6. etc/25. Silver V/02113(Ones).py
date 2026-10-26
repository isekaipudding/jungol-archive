# 링크 : https://jungol.co.kr/problem/2113
import sys

input = sys.stdin.readline

# 백준 링크 : https://www.acmicpc.net/problem/4375

# 정수 -> 문자열 변환 과정에서 제한 설정에 의해 85% 반례 발생
# 따라서 문자열 제한을 해제합니다.
sys.set_int_max_str_digits(0) 

N:int = int(input().rstrip())

result:int = 1
shift:int = 1

while True :
    if result % N == 0 :
        break
    shift *= 10
    result += shift

print(len(str(result)))