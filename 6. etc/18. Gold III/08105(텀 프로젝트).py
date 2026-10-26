# 링크 : https://jungol.co.kr/problem/8105
import sys

input = sys.stdin.readline

# 생각해보니 이 문제는 solved.ac class 5 에센셜 문제이네요.
# 이 문제 하위호환 문제가 Beginner 문제라니 에라이ㅋㅋㅋㅋ

# 재귀 깊이 한도 높이기
sys.setrecursionlimit(1 << 20)

def dfs1(u):
    if visited[u]:
        return 0
    if u in S:
        return u
    
    S.add(u)
    v:int = graph[u][0]
    return dfs1(v)

def dfs2(u):
    if u in S:
        return
    
    S.add(u)
    v:int = graph[u][0]
    dfs2(v)

N:int = int(input().rstrip())
nodes:list = [0] + list(map(int, input().split()))
graph:list = [[] for _ in range(N + 1)]

visited:list = [False for _ in range(N + 1)]
visited[0] = True

# 순열 사이클 시작 지점 리스트
start:list = []

# 그래프 정보 입력(단방향 그래프)
for u in range(1, N + 1, 1):
    v:int = nodes[u]
    graph[u].append(v)

S:set = set()
for i in range(1, N + 1, 1):
    S.clear()
    status:int = dfs1(i)
    
    if status:
        start.append(status)
        for j in S:
            visited[j] = True
    else:
        for j in S:
            visited[j] = True

L:list = []
for s in start:
    S.clear()
    dfs2(s)
    for n in S:
        L.append(n)

result:int = N - len(L)
print(result)