# 링크 : https://jungol.co.kr/problem/2007
import heapq
import sys

input = sys.stdin.readline

N, K = map(int, input().split()) # N : 건물의 수, K : 설치해야 하는 케이블의 수

MAX_RANGE = 10**9 # 10억km는 (지구-목성 거리)와 (지구-토성 거리) 사이의 거리를 의미합니다.
# 만약 일론 머스크가 화성으로 가는데 성공하여 테라포밍까지 완료했다면 이 문제는 현실성 있는 문제로 변경됩니다.

# 거리, 왼쪽, 오른쪽 인덱스를 저장할 배열 초기화 해줍니다.
distance = [0 for _ in range(N+2)]
left = [0 for _ in range(N+2)]
right = [0 for _ in range(N+2)]
visited = [False for _ in range(N+2)]  # 방문한 점의 상태를 저장하는 배열
priority_queue = []  # 거리 기반 우선순위 큐 초기화

distance[N + 1] = MAX_RANGE # 마지막 건물의 위치는 최대 거리로 가정합니다.
distance[1] = distance[N + 1] # 아직 입력 안 되었으니 1번째 건물은 최대 거리로 가정합니다.
right[1] = 2  # 첫 번째 점의 오른쪽 점은 두 번째 점입니다.
left[N + 1] = N  # 마지막 점의 왼쪽 점은 N번째 점입니다.

# 우선순위 큐에 첫 번째와 마지막 가상의 점의 거리 추가
heapq.heappush(priority_queue, (MAX_RANGE, 1))
heapq.heappush(priority_queue, (MAX_RANGE, N + 1))

# 자, 그럼 지금부터 정보통신회사 업무를 시작해볼까요?
# 저 탐욕스러운 사장 놈이 재료비를 줄이기 위해 오늘도 인건비 저렴한 직원을 굴려먹는군요.

# 지금부터 제가 직접 현장 조사를 해서 각 건물의 위치 정보를 파악하겠습니다.
# 10억km까지 있어서 우주선을 많이 타야겠군요.
LeftPoint = int(input().rstrip()) # 1번째 건물의 위치를 파악해 볼까요?
for i in range(2, N + 1):
    RightPoint = int(input().rstrip()) # 각 건물의 위치 정보를 파악해봅니다.
    distance[i] = RightPoint - LeftPoint # 그런데 견적 내는 놈들이 거리 정보를 안 내놓았네요.
    # 제가 현장 조사를 해봐야 뭐합니까 사무실에 있는 직장 동료들이 월급 루팡인데.
    # 어쩔 수 없죠. 제가 직접 계산할 수 밖에.
    
    # 해당 거리와 인덱스를 우선순위 큐에 추가합니다.
    heapq.heappush(priority_queue, (distance[i], i))
    left[i] = i - 1  # i번째 점의 왼쪽 인덱스는 i-1
    right[i] = i + 1  # i번째 점의 오른쪽 인덱스는 i+1
    LeftPoint = RightPoint  # 현재 위치를 업데이트하여 다음 건물의 위치로 설정합니다.
    # 그래야 나중에 다음 건물의 거리 견적을 제가 직접할 수 있으니까요.

# 지금 최소 비용이 얼마인지 모르니 일단 0으로 가정해볼까요?
least_cost = 0

# K개의 점을 선택할 때까지 반복합니다.
# 이 업무는 굉장히 힘드니 에너지 드링크를 마셔서 야근 열심히 해야죠 뭐...
while K:
    # 이미 방문한 노드는 큐에서 제거해줍니다. 두 번 일하면 비효율적이니까요.
    while visited[priority_queue[0][1]]:
        heapq.heappop(priority_queue)
    
    # 우선순위 큐에서 가장 작은 거리 값을 가진 점을 선택해주고 pop()에 의해 삭제됩니다.
    # 삭제하지 않으면 다음 while문 실행할 때 이미 검사했던 거리가 중복 검사되는 문제가 발생합니다.
    # 여기가 바로 그리디 알고리즘
    distance_of_present_index, index = heapq.heappop(priority_queue)
    
    # 선택된 점의 거리 값을 총 비용에 더합니다. 내 월급도 같이 더해줬으면 좋겠는데...
    least_cost += distance_of_present_index
    
    # 선택된 점을 제거하고, 이웃 점들의 새로운 거리 값들을 계산해줍니다.
    # 여기도 그리디 알고리즘
    distance[index] = distance[left[index]] + distance[right[index]] - distance[index]
    # 업데이트된 거리를 큐에 다시 추가해줍니다.
    heapq.heappush(priority_queue, (distance[index], index))

    # 이 건물은 조사 완료했습니다. 그러므로 해당 건물 및 그의 인접한 건물들은 "이미 방문함"으로 처리합니다.
    visited[left[index]] = visited[right[index]] = True
    
    # 인덱스 업데이트: 선택된 점을 제거 후 인접 점들의 포인터를 갱신합니다.
    left[index] = left[left[index]]  # 현재 점의 새로운 왼쪽 점으로 업데이트
    right[index] = right[right[index]]  # 현재 점의 새로운 오른쪽 점으로 업데이트
    right[left[index]] = index  # 새로운 왼쪽 점의 오른쪽 인덱스를 현재 점으로 설정
    left[right[index]] = index  # 새로운 오른쪽 점의 왼쪽 인덱스를 현재 점으로 설정

    K -= 1  # 선택한 점의 수 줄여줍니다.
    # 그런데 오늘 업무를 보니 케이블의 수를 10000개 정도 설치해야 한다고요?
    # 그러면 협력 업체한테 케이블 발주할려면... 아 퇴사하고 싶다.
    
print(least_cost) # 오늘의 업무 끝! 이번에 재료비를 획기적으로 줄이는 성과 한 번 냈으니 월급 좀 주세요 사장님!