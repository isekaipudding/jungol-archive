# 링크 : https://jungol.co.kr/problem/8895
import sys

input = sys.stdin.readline

def is_prime(N:int) -> bool :
    if N < 2:
        return False
    if N == 2 or N == 3:
        return True  # 2와 3은 소수
    if N % 2 == 0 or N % 3 == 0:
        return False # 2나 3의 배수는 모두 제외

    # 5부터 시작해서 6씩 건너뜁니다. (i는 6k-1, i+2는 6k+1에 대응)
    i:int = 5
    while i * i <= N :
        if N % i == 0 or N % (i + 2) == 0:
            return False
        i += 6
        
    return True

N:int = int(input().rstrip())

# 예외 처리
if N == 3:
    print("10")
    sys.exit(0)

if N & 1:
    N -= 2
else:
    N -= 1

while N:
    if is_prime(N):
        break
    N -= 2

print(bin(N)[2::])