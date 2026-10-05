# 링크 : https://jungol.co.kr/problem/10408
import sys
from collections import Counter
from itertools import product

input = sys.stdin.readline

# 이게 백트래킹 없이도 수학적 애드혹으로 해결되는구나

T:int = int(input().rstrip())

for number in range(1, T + 1, 1):
    code:str = input().rstrip()
    N:int = len(code)
    
    digits:list = [int(c) for c in code]
    digits.sort()
    
    if N & 1:
        # 첫 번째 숫자가 0이 되지 않도록 가장 작은 자연수를 찾습니다.
        first_nonzero_index = digits.count(0)
        
        long_first = digits[first_nonzero_index]
        remainder_digits = digits[:first_nonzero_index] + digits[first_nonzero_index + 1:]
        
        N >>= 1
        # 긴 숫자의 꼬리는 남은 것 중 가장 작은 k개를 오름차순으로 이어 붙임
        long_rest = remainder_digits[:N]
        # 짧은 숫자는 남은 k개를 내림차순으로 이어 붙임
        short_digits = remainder_digits[N:][::-1]
        
        A = int(str(long_first) + "".join(map(str, long_rest)))
        B = int("".join(map(str, short_digits)))
        print(f"Case #{number}: {A - B}")
    else:
        counter = Counter(digits)
        frequency = [counter[i] for i in range(10)]
        
        # 예외 처리
        # 1. 모든 숫자가 짝수 개인지 확인
        is_all_even = True
        for f in frequency:
            if f & 1:
                is_all_even = False
                break

        # 2. 0이 아닌 숫자(1~9)가 하나라도 존재하는지 확인
        has_non_zero = False
        for i in range(1, 10):
            if frequency[i] > 0:
                has_non_zero = True
                break

        # 3. 두 조건을 모두 만족하면 차이는 0이 됨
        if is_all_even and has_non_zero:
            print(f"Case #{number}: 0")
            continue
        
        result = float('inf')

        for dA in range(1, 10):
            for dB in range(0, dA):
                if frequency[dA] > 0 and frequency[dB] > 0:
                    remainder_frequency = frequency.copy()
                    remainder_frequency[dA] -= 1
                    remainder_frequency[dB] -= 1
                    
                    # 각 숫자(0~9)별로 온전한 쌍(Pair)이 몇 개인지 확인
                    pairs = [remainder_frequency[i] >> 1 for i in range(10)]
                    
                    # itertools.product를 활용한 쌍 분배 브루트 포스
                    # 각 숫자별로 0개부터 pairs[i]개까지 꼬리(Tail)로 내릴 개수를 조합합니다.
                    # 여기가 문제네요. 여기를 수정합니다.
                    # 0(인덱스 0)은 제한을 해제하고, 1~9(인덱스 1 이상)는 최대 1쌍으로 제한합니다.
                    ranges = [range(pairs[0] + 1)] + [range(min(p, 1) + 1) for p in pairs[1:]]
                    
                    for tail_pairs in product(*ranges):
                        # 접두사(Prefix)에 남게 될 쌍의 개수
                        prefix_pairs = [pairs[i] - tail_pairs[i] for i in range(10)]
                        total_prefix_pairs = sum(prefix_pairs)
                        
                        # 접두사가 오직 0으로만 이루어지는 경우(앞자리가 0이 되므로 무효)
                        if total_prefix_pairs > 0 and sum(prefix_pairs[1:]) == 0:
                            continue
                            
                        # 접두사가 아예 없는데 dB가 0인 경우(B의 앞자리가 0이 되므로 무효)
                        if total_prefix_pairs == 0 and dB == 0:
                            continue
                        
                        # 이거 그냥 그리디 때려넣으면 될 줄 알았는데 백트래킹 강요하는 반례가 터지네요
                        # 하지만 이것조차 결국 백트래킹 없이 구현됩니다
                        current_tail = []
                        for i in range(10):
                            count = tail_pairs[i] * 2 + (remainder_frequency[i] % 2)
                            current_tail.extend([i] * count)
                        
                        k = len(current_tail) // 2
                        
                        A_remainder_digits = current_tail[:k]
                        B_remainder_digits = current_tail[k:][::-1]
                        
                        A_remainder = int("".join(map(str, A_remainder_digits))) if A_remainder_digits else 0
                        B_remainder = int("".join(map(str, B_remainder_digits))) if B_remainder_digits else 0
                        
                        TEMP = (dA - dB) * (10 ** k) + A_remainder - B_remainder
                        result = min(result, TEMP)
                        
        print(f"Case #{number}: {result}")