# 링크 : https://jungol.co.kr/problem/2251
import sys
from bisect import bisect_left

input = sys.stdin.readline

N:int = int(input().rstrip())

# 스위치와 전구의 배치 순서(위에서부터 차례대로)
switches:list = list(map(int, input().split()))
bulbs:list = list(map(int, input().split()))

# 각 전구 번호가 몇 번째 높이(0-based)에 있는지 매핑
bulb_position:list = [0] * (N + 1)
for index, b_number in enumerate(bulbs):
    bulb_position[b_number] = index

# 스위치 순서대로 대응되는 전구의 인덱스 수열 생성
# mapped_position[i] = switches[i]번 스위치에 연결된 전구의 높이
mapped_position:list = [bulb_position[s_number] for s_number in switches]

# O(N log N) LIS
lis_tails:list = []            # LIS 길이를 유지하기 위한 최소 끝값 배열
position_record:list = [0] * N # 각 스위치가 LIS의 몇 번째 위치에 들어갔는지 기록

for i in range(N):
    value = mapped_position[i]
    index = bisect_left(lis_tails, value)
    if index == len(lis_tails):
        lis_tails.append(value)
    else:
        lis_tails[index] = value
    position_record[i] = index

max_count:int = len(lis_tails)

# 뒤에서부터 역추적하여 LIS에 포함된 스위치 복원
target_index:int = max_count - 1
selected_switches:list = []

for i in range(N - 1, -1, -1):
    if position_record[i] == target_index:
        selected_switches.append(switches[i])
        target_index -= 1
        if target_index < 0:
            break

# 스위치 번호를 오름차순으로 출력
selected_switches.sort()

print(max_count)
print(*(selected_switches))