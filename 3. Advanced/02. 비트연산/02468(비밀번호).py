# 링크 : https://jungol.co.kr/problem/2468
import sys
import copy

input = sys.stdin.readline

IN:int = int(input().rstrip())
N:str = bin(IN)[2::]
size:int = len(N)

L:list = [False for _ in range(len(N))]

for i in range(size):
    if N[i] == "1":
        L[i] = True
    if N[i] == "0":
        L[i] = False

# 아 젠장 11111000000일 때 MAX 초기값을 잘못 설정했어요.
# 원래라면 111000이면 1000011로 맨 왼쪽에 1 1개, 나머지 (1의 개수 - 1)개의 1을 모두 1로 옮기는 것이 초기 MAX값입니다...
MIN, MAX = 0, 2 ** size

# MAX 초기값을 구하기 위한 소스 코드입니다.
# 뭔 놈의 반례가 계속 터지나요?
TEMP_COUNT = N.count("1") - 1
TEMP_SHIFT = 1
while TEMP_COUNT:
    MAX += TEMP_SHIFT
    TEMP_COUNT -= 1
    TEMP_SHIFT <<= 1

# 그리디 알고리즘 1 -> 10101이 있다고 가정할 때 맨 오른쪽부터 확인해서 (10)이면 (01)로 바꾼다.
# 즉, 10(10)1 -> 10011이 되어 최소값을 구한다.
status:int = -1

A:list = copy.deepcopy(L)

for i in range(size - 2, -1, -1):
    if L[i] == True and L[i+1] == False:
        status = i
        break

if status != -1:
    A[status] = False
    A[status + 1] = True
    
    # 110011일 때 1(10)011 -> 101011이 됩니다.
    # 여기서 101(011)에서 (011) 부분에 있는 모든 1들을 전부 왼쪽으로 옮깁니다.
    # 101(011) -> 101100
    count:int = 0
    for i in range(status + 2, size, 1):
        if A[i]:
            count += 1
        A[i] = False
    for i in range(status + 2, status + 2 + count, 1):
        A[i] = True
    
    shift:int = 1
    for i in range(size - 1, -1, -1):
        if A[i]:
            MIN += shift
        shift <<= 1

# 그리디 알고리즘 2 -> 10101이 있다고 가정할 때 맨 오른쪽부터 확인해서 (01)이면 (10)로 바꾼다.
# 즉, 101(01) -> 10110이 되어 최댓값을 구한다.
status = -1

B:list = copy.deepcopy(L)

for i in range(size - 1, 0, -1):
    if L[i] == True and L[i-1] == False:
        status = i
        break

if status != -1:
    MAX = 0
    B[status] = False
    B[status - 1] = True
    
    # 101100일 때 1(01)100 -> 110100이 됩니다.
    # 여기서 110(100)에서 (100)의 모든 1들을 오른쪽으로 옮깁니다.
    # 110(100) -> 110001
    count:int = 0
    for i in range(status + 1, size, 1):
        if B[i]:
            count += 1
        B[i] = False
    # 여기가 틀렸네요. 범위를 잘못 지정했어요.
    # -> 방향이 아닌 <- 방향으로 해야 하므로 아래와 같이 또 수정합니다.
    for i in range(size - 1, size - 1 - count, -1):
        B[i] = True
    
    shift:int = 1
    for i in range(size - 1, -1, -1):
        if B[i]:
            MAX += shift
        shift <<= 1

print(MIN, MAX)