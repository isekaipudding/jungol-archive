# 링크 : https://jungol.co.kr/problem/2071
import sys

input = sys.stdin.readline

LIMIT = 30

fact:list = [0 for _ in range(LIMIT + 1)]

# 초기값
fact[0] = 1

# 점화식
for i in range(1, LIMIT + 1, 1) :
    fact[i] = fact[i-1] * i

def coff(n:int, k:int) :
    return fact[n] // fact[k] // fact[n-k]

def make_graph_ver1() :
    for i in range(N) :
        for j in range(i + 1) :
            graph[i].append(coff(i, j))
    return

def make_graph_ver2() :
    for i in range(N) :
        for j in range(i + 1) :
            graph[N - 1 - i].append(coff(i, j))
    return

def make_graph_ver3() :
    for i in range(N-1, -1, -1) :
        for j in range(i + 1) :
            graph[N - 1 - j].append(coff(i, j))
    return

N, M = map(int, input().split())

graph:list = [[] for _ in range(N)]

if M == 1 :
    make_graph_ver1()
    for i in range(N) :
        print(*graph[i])
if M == 2 :
    make_graph_ver2()
    for i in range(N) :
        print(" " * i, end="", flush=True)
        print(*graph[i])
if M == 3 :
    make_graph_ver3()
    for i in range(N) :
        print(*graph[i])