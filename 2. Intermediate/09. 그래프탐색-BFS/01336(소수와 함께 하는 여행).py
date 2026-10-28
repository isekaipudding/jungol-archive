# 링크 : https://jungol.co.kr/problem/1336
import sys
import math
from collections import deque

input = sys.stdin.readline

def eratosthenes_sieve(n:int) -> list :
    if n < 2 :
        return []
    
    is_prime:list = [True] * (n + 1)
    
    is_prime[0], is_prime[1] = False, False
    
    for i in range(4, n + 1, 2) :
        is_prime[i] = False
        
    for i in range(3, int(math.sqrt(n)) + 1, 2) :
        if is_prime[i] :
            for j in range(i * i, n + 1, 2 * i) :
                is_prime[j] = False
                
    return [index for index, value in enumerate(is_prime) if value]


def bfs(start:int, target:int, prime_set:set) -> int:
    if start == target:
        return 0

    visited:list = [False] * 10000
    visited[start] = True

    queue = deque([(start, 0)])

    while queue:
        current, distance = queue.popleft()
        current_str = list(str(current))

        # 4개 자릿수 각각에 대해 0~9 변환 시도
        for i in range(4):
            original_digit = current_str[i]

            for d in range(10):
                # 첫 번째 자리는 0이 될 수 없음(4자리 수 유지)
                if i == 0 and d == 0:
                    continue

                new_char = str(d)
                if new_char == original_digit:
                    continue

                current_str[i] = new_char
                next_number = int("".join(current_str))

                # 목표 정류장에 도달한 경우 최단 이동 횟수 반환
                if next_number == target:
                    return distance + 1

                # 4자리 소수이고 아직 방문하지 않은 정류장인 경우
                if next_number in prime_set and not visited[next_number]:
                    visited[next_number] = True
                    queue.append((next_number, distance + 1))

            # 다음 자릿수 탐색을 위해 원래 숫자로 복원
            current_str[i] = original_digit

    return -1


# 에라토스테네스의 체를 이용해 1000~9999 범위의 소수 집합 생성
primes = eratosthenes_sieve(9999)
prime_set = set(p for p in primes if p >= 1000)

start_node, target_node = map(int, input().split())

result:int = bfs(start_node, target_node, prime_set)
print(result)