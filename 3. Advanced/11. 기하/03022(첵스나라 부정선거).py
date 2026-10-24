# 링크 : https://jungol.co.kr/problem/3022
import sys

input = sys.stdin.readline
        
N:int = int(input().rstrip())

M_array = []
S_array = []
delta_array = []

for _ in range(N):
    A, B = map(int, input().split())
    
    M_array.append(max(A, B))
    S_array.append(A + B)
    delta_array.append(A - B) # 체키 표 - 차카 표(양수면 체키 우세)
    
# 좌표 압축을 위해 필요한 경계값(임계점) 추출
# X, Y는 1부터 100,000까지 가능하므로 범위 양끝인 1과 100001을 고정 포함
X_set = {1, 100001}
Y_set = {1, 100001}

for M in M_array:
    X_set.add(min(100001, M + 1))
for S in S_array:
    Y_set.add(min(100001, S + 1))
    
X_pts = sorted(list(X_set))
Y_pts = sorted(list(Y_set))

X_index = {v: i for i, v in enumerate(X_pts)}
Y_index = {v: i for i, v in enumerate(Y_pts)}

R, C = len(X_pts), len(Y_pts)

# 2차원 차분 배열 트릭
diff = [[0] * C for _ in range(R)]

for i in range(N):
    # i번째 유권자가 유효표로 인정받기 시작하는 X, Y 좌표의 인덱스
    ix = X_index[min(100001, M_array[i] + 1)]
    iy = Y_index[min(100001, S_array[i] + 1)]
    
    # 해당 좌표부터 오른쪽 아래 전체 구역으로 체키/차카의 표 격차 누적
    diff[ix][iy] += delta_array[i]
    
result = 0
P = [[0] * C for _ in range(R)]

# 2차원 누적 합 계산 및 유효 사각형 영역 넓이 합산
for i in range(R - 1):
    for j in range(C - 1):
        v = diff[i][j]
        if i > 0: v += P[i-1][j]
        if j > 0: v += P[i][j-1]
        if i > 0 and j > 0: v -= P[i-1][j-1]
        
        P[i][j] = v
        
        # 체키가 이기는(누적 표 차이 > 0) 경우, 해당 압축 좌표에 대응하는 실제 넓이 추가
        if P[i][j] > 0:
            width = X_pts[i+1] - X_pts[i]
            height = Y_pts[j+1] - Y_pts[j]
            result += width * height
            
print(result)